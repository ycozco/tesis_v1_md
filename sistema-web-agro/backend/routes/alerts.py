import os
import re
import random
import csv
import io
from flask import Blueprint, request, jsonify, make_response
from models import SessionLocal, OperacionAlerta, ExplicacionSHAP, DecisionAuditoria, DocumentoNormativo, GeneratedReport, Usuario, SecurityLog
import services.ml_service as ml_service
import services.rag_service as rag_service
from services.common import CONFIG_STATE

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/api/alerts', methods=['GET'])
def get_alerts():
    db = SessionLocal()
    try:
        producto = request.args.get('producto')
        estado = request.args.get('estado')
        search = request.args.get('search')

        query = db.query(OperacionAlerta)

        if producto:
            query = query.filter(OperacionAlerta.producto.ilike(f'%{producto}%'))
        if estado:
            query = query.filter(OperacionAlerta.estado == estado)
        if search:
            query = query.filter(
                (OperacionAlerta.id_alerta.ilike(f'%{search}%')) |
                (OperacionAlerta.numero_dam.ilike(f'%{search}%')) |
                (OperacionAlerta.ruc_exportador.ilike(f'%{search}%')) |
                (OperacionAlerta.razon_social.ilike(f'%{search}%'))
            )

        alerts = query.order_by(OperacionAlerta.score_anomalia.desc()).all()
        return jsonify([a.to_dict() for a in alerts]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()

@alerts_bp.route('/api/alerts/<id_alerta>', methods=['GET'])
def get_alert_detail(id_alerta):
    db = SessionLocal()
    try:
        alert = db.query(OperacionAlerta).filter_by(id_alerta=id_alerta).first()
        if not alert:
            return jsonify({'message': 'Alerta no encontrada.'}), 404

        app_mode = os.getenv('APP_MODE', 'DEMO')
        allow_mock = os.getenv('ALLOW_MOCK_MODE', 'true').lower() == 'true'

        if app_mode == 'EXPERIMENT' or not allow_mock:
            explanations = db.query(ExplicacionSHAP).filter_by(id_alerta=id_alerta).all()
            decision = db.query(DecisionAuditoria).filter_by(id_alerta=id_alerta).first()
            docs = db.query(DocumentoNormativo).limit(3).all()

            stored_report = db.query(GeneratedReport).filter_by(id_alerta=id_alerta).first()
            if stored_report:
                rag_report = stored_report.report_text
            else:
                desvio_fob = float(alert.valor_fob_esperado) - float(alert.valor_fob_declarado)
                desvio_fob_pct = (desvio_fob / float(alert.valor_fob_esperado) * 100) if float(alert.valor_fob_esperado) > 0 else 0
                mock_features = [[0, 0, 7.6, 13]]
                rag_report = rag_service.generate_offline_report(alert, mock_features, docs, desvio_fob, desvio_fob_pct)

            alert_dict = alert.to_dict()
            
            for e in explanations:
                val_str = str(e.variable_valor)
                if e.variable_nombre == 'Peso Neto':
                    nums = re.findall(r"[-+]?\d*\.\d+|\d+", val_str.replace(',', ''))
                    if nums: alert_dict['peso_neto'] = float(nums[0])
                elif e.variable_nombre == 'Desviación Temp.':
                    nums = re.findall(r"[-+]?\d*\.\d+|\d+", val_str.replace(',', ''))
                    if nums: alert_dict['temperatura'] = float(nums[0])
                elif e.variable_nombre == 'Retraso Logístico':
                    nums = re.findall(r"[-+]?\d*\.\d+|\d+", val_str.replace(',', ''))
                    if nums: alert_dict['retraso_dias'] = int(float(nums[0]))
            
            if alert_dict.get('peso_neto', 0) == 0:
                alert_dict['peso_neto'] = float(alert.valor_fob_esperado) / 2.5
            if alert_dict.get('temperatura', 0) == 0:
                alert_dict['temperatura'] = 2.4
            if alert_dict.get('retraso_dias', 0) == 0:
                alert_dict['retraso_dias'] = 3

            return jsonify({
                'alert': alert_dict,
                'explanations': [e.to_dict() for e in explanations],
                'decision': decision.to_dict() if decision else None,
                'rag_report': rag_report,
                'rag_documents': [d.to_dict() for d in docs]
            }), 200

        # MODO DEMOSTRACIÓN TRADICIONAL (DYNAMIC/MOCK)
        ml_service.load_ml_models()
        features = ml_service.get_feature_vector(alert)

        fob_esperado = float(alert.valor_fob_esperado)
        if ml_service.xgb_model is not None:
            try:
                import xgboost as xgb
                if isinstance(ml_service.xgb_model, xgb.Booster):
                    dtrain = xgb.DMatrix(features)
                    pred_fob = float(ml_service.xgb_model.predict(dtrain)[0])
                else:
                    pred_fob = float(ml_service.xgb_model.predict(features)[0])
                
                if pred_fob <= float(alert.valor_fob_declarado):
                    pred_fob = max(pred_fob, float(alert.valor_fob_declarado) * random.uniform(1.05, 1.30))
                
                fob_esperado = round(pred_fob, 2)
            except Exception as e:
                print(f"Error prediciendo FOB con XGBoost: {e}")

        score_anomalia = float(alert.score_anomalia)
        if ml_service.iforest is not None and ml_service.lof is not None and ml_service.ecod is not None and ml_service.scaler is not None:
            try:
                features_scaled = ml_service.scaler.transform(features)
                p_iforest = float(ml_service.iforest.predict_proba(features_scaled)[0][1])
                p_lof = float(ml_service.lof.predict_proba(features_scaled)[0][1])
                p_ecod = float(ml_service.ecod.predict_proba(features_scaled)[0][1])

                w_if = CONFIG_STATE['weights'].get('isolation_forest', 0.45)
                w_lof = CONFIG_STATE['weights'].get('lof', 0.30)
                w_ecod = CONFIG_STATE['weights'].get('ecod', 0.25)
                total_w = w_if + w_lof + w_ecod
                if total_w > 0:
                    w_if /= total_w
                    w_lof /= total_w
                    w_ecod /= total_w

                score_anomalia = round((p_iforest * w_if) + (p_lof * w_lof) + (p_ecod * w_ecod), 4)
            except Exception as e:
                print(f"Error prediciendo anomalía con PyOD: {e}")

        shap_items = []
        if ml_service.xgb_model is not None:
            try:
                import shap
                explainer = shap.TreeExplainer(ml_service.xgb_model)
                shap_values = explainer.shap_values(features)

                shap_items = [
                    {
                        'variable_nombre': 'Precio Declarado',
                        'shap_value': float(shap_values[0][0]),
                        'variable_valor': f"${float(features[0][0]):,.2f} USD"
                    },
                    {
                        'variable_nombre': 'Peso Neto',
                        'shap_value': float(shap_values[0][1]),
                        'variable_valor': f"{float(features[0][1]):,.1f} kg"
                    },
                    {
                        'variable_nombre': 'Desviación Temp.',
                        'shap_value': float(shap_values[0][2]),
                        'variable_valor': f"{float(features[0][2]):.1f}°C"
                    },
                    {
                        'variable_nombre': 'Retraso Logístico',
                        'shap_value': float(shap_values[0][3]),
                        'variable_valor': f"+{int(features[0][3])} días"
                    }
                ]
            except Exception as e:
                print(f"Error calculando TreeSHAP: {e}")

        rag_report, docs = rag_service.generate_rag_report(db, alert, features, fob_esperado, score_anomalia)

        alert.valor_fob_esperado = fob_esperado
        alert.score_anomalia = score_anomalia
        
        global_threshold = CONFIG_STATE.get('global_threshold', 0.65)
        alert.alertado = (score_anomalia >= global_threshold)

        if shap_items:
            db.query(ExplicacionSHAP).filter_by(id_alerta=id_alerta).delete()
            for item in shap_items:
                ex = ExplicacionSHAP(
                    id_alerta=id_alerta,
                    variable_nombre=item['variable_nombre'],
                    shap_value=item['shap_value'],
                    variable_valor=item['variable_valor']
                )
                db.add(ex)
        
        db.commit()

        explanations = db.query(ExplicacionSHAP).filter_by(id_alerta=id_alerta).all()
        decision = db.query(DecisionAuditoria).filter_by(id_alerta=id_alerta).first()

        alert_dict = alert.to_dict()
        alert_dict['peso_neto'] = float(features[0][1])
        alert_dict['temperatura'] = float(features[0][2])
        alert_dict['retraso_dias'] = int(features[0][3])

        return jsonify({
            'alert': alert_dict,
            'explanations': [e.to_dict() for e in explanations],
            'decision': decision.to_dict() if decision else None,
            'rag_report': rag_report,
            'rag_documents': [d.to_dict() for d in docs]
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({'message': f"Error en el servidor: {str(e)}"}), 500
    finally:
        db.close()

@alerts_bp.route('/api/alerts/<id_alerta>/adjudicate', methods=['POST'])
def adjudicate_alert(id_alerta):
    data = request.get_json() or {}
    user_decision = data.get('user_decision')
    justification_text = data.get('justification_text', '')
    likert_comprehension = data.get('likert_comprehension')
    time_to_decision_ms = data.get('time_to_decision_ms')
    username = data.get('username')
    condicion = data.get('condicion')

    if user_decision is None or likert_comprehension is None or time_to_decision_ms is None or not username:
        return jsonify({'message': 'Faltan parámetros de adjudicación obligatorios.'}), 400

    db = SessionLocal()
    try:
        alert = db.query(OperacionAlerta).filter_by(id_alerta=id_alerta).first()
        if not alert:
            return jsonify({'message': 'Alerta no encontrada.'}), 404

        user = db.query(Usuario).filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'Usuario no encontrado.'}), 404

        if user_decision == 0:
            nuevo_estado = 'FALSA_ALARMA'
        elif user_decision == 1:
            nuevo_estado = 'CONFIRMADA'
        else:
            nuevo_estado = 'REFIERE_INSPECCION'

        alert.estado = nuevo_estado

        decision = DecisionAuditoria(
            id_alerta=id_alerta,
            id_usuario=user.id_usuario,
            condicion_experimento=condicion,
            user_decision=user_decision,
            justification_text=justification_text,
            likert_comprehension=int(likert_comprehension),
            time_to_decision_ms=int(time_to_decision_ms)
        )
        db.add(decision)

        ip_addr = request.remote_addr or '127.0.0.1'
        sec_log = SecurityLog(
            usuario=username,
            evento=f'ALERT_ADJUDICATED: {id_alerta} -> {nuevo_estado}',
            ip_address=ip_addr
        )
        db.add(sec_log)

        db.commit()
        return jsonify({'message': 'Decisión registrada correctamente en telemetría.', 'alerta': alert.to_dict()}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'message': f'Error al adjudicar alerta: {str(e)}'}), 500
    finally:
        db.close()

@alerts_bp.route('/api/alerts/<id_alerta>/company-history', methods=['GET'])
def get_company_history(id_alerta):
    db = SessionLocal()
    try:
        alert = db.query(OperacionAlerta).filter_by(id_alerta=id_alerta).first()
        if not alert:
            return jsonify({'message': 'Alerta no encontrada.'}), 404
        
        history = db.query(OperacionAlerta)\
            .filter(OperacionAlerta.ruc_exportador == alert.ruc_exportador)\
            .filter(OperacionAlerta.id_alerta != id_alerta)\
            .order_by(OperacionAlerta.fecha_operacion.desc())\
            .limit(5).all()
            
        return jsonify([h.to_dict() for h in history]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()

@alerts_bp.route('/api/alerts/export/csv', methods=['GET'])
def export_alerts_csv():
    db = SessionLocal()
    try:
        alerts = db.query(OperacionAlerta).all()
        dest = io.StringIO()
        writer = csv.writer(dest)
        
        writer.writerow([
            'id_alerta', 'numero_dam', 'fecha_operacion', 'ruc_exportador', 
            'razon_social', 'producto', 'valor_fob_declarado', 'valor_fob_esperado', 
            'score_anomalia', 'estado', 'decision_auditor', 'justificacion', 
            'latencia_ms', 'comprension_likert', 'condicion_experimento'
        ])
        
        for a in alerts:
            dec = db.query(DecisionAuditoria).filter_by(id_alerta=a.id_alerta).first()
            dec_val = dec.user_decision if dec else ''
            just = dec.justification_text if dec else ''
            time_ms = dec.time_to_decision_ms if dec else ''
            comp = dec.likert_comprehension if dec else ''
            cond = dec.condicion_experimento if dec else ''
            
            writer.writerow([
                a.id_alerta, a.numero_dam, a.fecha_operacion.isoformat() if a.fecha_operacion else '',
                a.ruc_exportador, a.razon_social, a.producto, float(a.valor_fob_declarado),
                float(a.valor_fob_esperado), float(a.score_anomalia), a.estado,
                dec_val, just, time_ms, comp, cond
            ])
            
        output = make_response(dest.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=agro_alerts_export.csv"
        output.headers["Content-type"] = "text/csv"
        return output
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()
