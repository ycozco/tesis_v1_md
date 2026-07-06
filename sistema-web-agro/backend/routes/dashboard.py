import random
from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from sqlalchemy import func
from models import SessionLocal, OperacionAlerta, DecisionAuditoria, SecurityLog
from services.common import USER_CONDITIONS

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    db = SessionLocal()
    try:
        active_count = db.query(OperacionAlerta).filter(
            OperacionAlerta.estado.in_(['PENDIENTE', 'EN_REVISION'])
        ).count()

        total_count = db.query(OperacionAlerta).count()

        avg_ms = db.query(func.avg(DecisionAuditoria.time_to_decision_ms)).scalar()
        avg_s = round((float(avg_ms) / 1000.0), 1) if avg_ms is not None else 0.0

        priority_alerts = db.query(OperacionAlerta).filter(
            OperacionAlerta.estado.in_(['PENDIENTE', 'EN_REVISION'])
        ).order_by(OperacionAlerta.score_anomalia.desc()).limit(5).all()

        priority_list = [a.to_dict() for a in priority_alerts]

        logs = db.query(SecurityLog).order_by(SecurityLog.fecha.desc()).limit(8).all()
        logs_list = [l.to_dict() for l in logs]

        trends = []
        today = datetime.now()
        for i in range(14, -1, -1):
            date_str = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            random.seed(date_str)
            count = random.randint(3, 18)
            trends.append({'fecha': date_str, 'cantidad': count})

        return jsonify({
            'active_alerts_count': active_count,
            'total_alerts_count': total_count,
            'avg_decision_time_s': avg_s,
            'priority_alerts': priority_list,
            'recent_logs': logs_list,
            'trends_14_days': trends
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()

@dashboard_bp.route('/api/dashboard/fob-scatter', methods=['GET'])
def get_fob_scatter():
    db = SessionLocal()
    try:
        alerts = db.query(OperacionAlerta).all()
        scatter_data = []
        for a in alerts:
            fob_dec = float(a.valor_fob_declarado)
            fob_esp = float(a.valor_fob_esperado)
            desv = abs(fob_dec - fob_esp) / fob_esp if fob_esp > 0 else 0.0
            scatter_data.append({
                'id_alerta': a.id_alerta,
                'producto': a.producto,
                'valor_fob_declarado': fob_dec,
                'valor_fob_esperado': fob_esp,
                'desviacion_pct': round(desv * 100, 2),
                'score_anomalia': float(a.score_anomalia),
                'severidad': 'Alta' if a.score_anomalia >= 0.85 else 'Media' if a.score_anomalia >= 0.6 else 'Baja'
            })
        return jsonify(scatter_data), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()

@dashboard_bp.route('/api/dashboard/fob-distribution', methods=['GET'])
def get_fob_distribution():
    db = SessionLocal()
    try:
        alerts = db.query(OperacionAlerta).all()
        counts = {'0-5%': 0, '5-10%': 0, '10-15%': 0, '>15%': 0}
        for a in alerts:
            fob_dec = float(a.valor_fob_declarado)
            fob_esp = float(a.valor_fob_esperado)
            desv = abs(fob_dec - fob_esp) / fob_esp if fob_esp > 0 else 0.0
            desv_pct = desv * 100
            if desv_pct <= 5:
                counts['0-5%'] += 1
            elif desv_pct <= 10:
                counts['5-10%'] += 1
            elif desv_pct <= 15:
                counts['10-15%'] += 1
            else:
                counts['>15%'] += 1
        
        distribution = [
            {'rango': '0-5%', 'cantidad': counts['0-5%']},
            {'rango': '5-10%', 'cantidad': counts['5-10%']},
            {'rango': '10-15%', 'cantidad': counts['10-15%']},
            {'rango': '>15%', 'cantidad': counts['>15%']}
        ]
        return jsonify(distribution), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()
