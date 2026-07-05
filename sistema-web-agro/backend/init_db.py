import os
import time
import sys
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from models import SessionLocal, init_tables, Usuario, OperacionAlerta, DecisionAuditoria, ExplicacionSHAP, SecurityLog, DocumentoNormativo, ConfiguracionPipeline, engine

# Machine learning libraries for dynamic compilation
import joblib
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.ecod import ECOD

def wait_for_db(max_retries=15, delay=2):
    print("Esperando a que PostgreSQL esté listo...")
    retries = 0
    while retries < max_retries:
        try:
            # Intentar conectar
            connection = engine.connect()
            connection.close()
            print("PostgreSQL está conectado y listo.")
            return True
        except OperationalError as e:
            retries += 1
            print(f"PostgreSQL no está listo aún ({retries}/{max_retries}). Reintentando en {delay}s...")
            time.sleep(delay)
    print("Error: No se pudo conectar a PostgreSQL.")
    sys.exit(1)

def compile_and_save_mock_models():
    print("Compilando y entrenando modelos analíticos en caliente...")
    os.makedirs('models_weights', exist_ok=True)
    
    # 1. Generar datos sintéticos de entrenamiento (1000 muestras, 4 variables)
    # Variables: valor_fob_declarado, peso_neto, temp_contenedor, dias_retraso
    np.random.seed(42)
    X = np.random.rand(1000, 4)
    # Scale variables so they represent realistic figures
    X[:, 0] = X[:, 0] * 120000 + 40000  # FOB Declarado: $40K - $160K
    X[:, 1] = X[:, 0] / (2.0 + np.random.rand(1000) * 1.5)  # Peso Neto
    X[:, 2] = X[:, 2] * 12.0  # Temp Contenedor: 0°C - 12°C
    X[:, 3] = np.random.randint(0, 12, 1000)  # Dias Retraso: 0 - 11
    
    # El valor FOB real/esperado correlaciona fuertemente con las variables
    y = X[:, 0] * 1.08 + X[:, 1] * 0.05 + np.random.normal(0, 3000, 1000)
    
    # 2. Entrenar y guardar el Scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, 'models_weights/scaler_fob.bin')
    
    # 3. Entrenar y guardar XGBoost Regressor (Capa 1)
    xgb_reg = xgb.XGBRegressor(n_estimators=10, max_depth=3, random_state=42)
    xgb_reg.fit(X, y)
    xgb_reg.save_model('models_weights/xgboost_fob_predictor.json')
    
    # 4. Entrenar y guardar modelos de detección de outliers de PyOD (Capa 2)
    iforest = IForest(random_state=42)
    iforest.fit(X_scaled)
    joblib.dump(iforest, 'models_weights/iforest_model.pkl')
    
    # Entrenar LOF
    lof = LOF()
    lof.fit(X_scaled)
    joblib.dump(lof, 'models_weights/lof_model.pkl')
    
    # Entrenar ECOD
    ecod = ECOD()
    ecod.fit(X_scaled)
    joblib.dump(ecod, 'models_weights/ecod_model.pkl')
    
    print("Modelos analíticos serializados correctamente en 'models_weights/'.")

def seed_normatives(db):
    print("Vectorizando y sembrando biblioteca de normativas RAG...")
    
    normativas = [
        {
            'titulo': 'FDA CFR Title 21 - Importación de Perecederos (Capítulo 1)',
            'categoria': 'FDA',
            'contenido': 'Sección 21.341 de la FDA: Todos los despachos agroindustriales con una desviación en valor FOB superior al 15% o que muestren proxies de riesgo logístico deben ser retenidos para inspección física sensorial de temperatura y calidad del empaque. Se debe verificar el contrato y la factura comercial contra la DAM.'
        },
        {
            'titulo': 'SENASA Directiva de Control Fitosanitario Agroexportador N° 04-2026',
            'categoria': 'SENASA',
            'contenido': 'Directiva SENASA: Estipula inspecciones aleatorias obligatorias en puerto de origen (ej. Paita, Callao) para productos de palta Hass y uva que sufran retrasos mayores a 48 horas en zona primaria de embarque. Esto previene la propagación de plagas por pérdida de cadena de frío.'
        },
        {
            'titulo': 'Reglamento de la Ley de IA del Perú (D.S. N° 115-2025-PCM)',
            'categoria': 'LEY_IA',
            'contenido': 'El reglamento estipula la obligación de los sistemas de IA de alto riesgo que operan en aduanas peruanas de proveer interfaces explicables a los operadores humanos para evitar sesgos discriminatorios algorítmicos. Las explicaciones locales (SHAP) y resúmenes narrativos RAG son obligatorios para validar anomalías.'
        }
    ]
    
    # Intentar cargar sentence-transformers para generar vectores reales
    try:
        from sentence_transformers import SentenceTransformer
        print("Cargando modelo sentence-transformers (BAAI/bge-small-en-v1.5) localmente...")
        model = SentenceTransformer('BAAI/bge-small-en-v1.5')
        has_transformer = True
    except Exception as e:
        print(f"Advertencia: No se pudo cargar sentence-transformers para indexación real ({e}). Usando vectores semilla.")
        has_transformer = False
        
    for norm in normativas:
        if has_transformer:
            emb = model.encode(norm['contenido']).tolist()
        else:
            emb = [0.1] * 384
            
        if engine.dialect.name == "sqlite":
            import json
            emb_val = json.dumps(emb)
        else:
            emb_val = emb
            
        doc = DocumentoNormativo(
            titulo=norm['titulo'],
            categoria=norm['categoria'],
            contenido=norm['contenido'],
            embedding=emb_val
        )
        db.add(doc)
        
    db.commit()
    print("Biblioteca de normativas RAG indexada exitosamente en pgvector.")

def seed_db():
    db = SessionLocal()
    try:
        # Re-crear tablas (limpieza completa)
        print("Re-creando tablas de la base de datos...")
        from models import Base
        
        # Habilitar extensión pgvector si es PostgreSQL
        if engine.dialect.name == "postgresql":
            # Usar CASCADE para eliminar tablas con restricciones de clave foránea
            db.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO public;"))
            db.commit()
            db.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            db.commit()
        else:
            Base.metadata.drop_all(bind=engine)
        
        init_tables()
        
        print("Insertando datos semilla (seed)...")
        
        # 1. Insertar Usuarios
        usuarios = [
            Usuario(username='auditor1', email='ycozco@unsa.edu.pe', password_hash=generate_password_hash('correct'), rol='AUDITOR', nombre='Yoset Cozco Mauri'),
            Usuario(username='auditor2', email='auditor_fito@agro.gob.pe', password_hash=generate_password_hash('correct'), rol='AUDITOR', nombre='Ing. Carlos Mendoza'),
            Usuario(username='admin', email='vcornejo@unsa.edu.pe', password_hash=generate_password_hash('correct'), rol='ADMIN', nombre='Dr. Víctor Cornejo Aparicio')
        ]
        db.add_all(usuarios)
        db.commit() # Confirmar usuarios para obtener IDs
        
        # 2. Insertar Alertas
        alertas = [
            # Alertas Pendientes
            OperacionAlerta(id_alerta='AL-2026-0012', numero_dam='118-2026-10-012345', fecha_operacion=datetime.strptime('2026-06-21', '%Y-%m-%d').date(), ruc_exportador='20123456789', razon_social='Agroworld S.A.C.', producto='Palta', valor_fob_declarado=120000.00, valor_fob_esperado=135000.00, score_anomalia=0.9500, alertado=True, estado='PENDIENTE'),
            OperacionAlerta(id_alerta='AL-2026-0011', numero_dam='118-2026-10-012346', fecha_operacion=datetime.strptime('2026-06-20', '%Y-%m-%d').date(), ruc_exportador='20556677889', razon_social='Valles del Norte EIRL', producto='Uva', valor_fob_declarado=85000.00, valor_fob_esperado=110000.00, score_anomalia=0.7200, alertado=True, estado='PENDIENTE'),
            OperacionAlerta(id_alerta='AL-2026-0010', numero_dam='118-2026-10-012347', fecha_operacion=datetime.strptime('2026-06-20', '%Y-%m-%d').date(), ruc_exportador='20998877665', razon_social='BerryCorp Andina', producto='Arándano', valor_fob_declarado=145000.00, valor_fob_esperado=160000.00, score_anomalia=0.6500, alertado=True, estado='PENDIENTE'),
            OperacionAlerta(id_alerta='AL-2026-0013', numero_dam='118-2026-10-012348', fecha_operacion=datetime.strptime('2026-06-21', '%Y-%m-%d').date(), ruc_exportador='20334455667', razon_social='Campos de Ica S.A.', producto='Palta', valor_fob_declarado=95000.00, valor_fob_esperado=112000.00, score_anomalia=0.7800, alertado=True, estado='PENDIENTE'),
            OperacionAlerta(id_alerta='AL-2026-0014', numero_dam='118-2026-10-012349', fecha_operacion=datetime.strptime('2026-06-21', '%Y-%m-%d').date(), ruc_exportador='20778899001', razon_social='Frutas del Pedregal S.A.', producto='Mango', valor_fob_declarado=60000.00, valor_fob_esperado=75000.00, score_anomalia=0.8200, alertado=True, estado='PENDIENTE'),
            
            # Alertas En Revisión
            OperacionAlerta(id_alerta='AL-2026-0008', numero_dam='118-2026-10-012340', fecha_operacion=datetime.strptime('2026-06-18', '%Y-%m-%d').date(), ruc_exportador='20556677889', razon_social='Valles del Norte EIRL', producto='Uva', valor_fob_declarado=98000.00, valor_fob_esperado=105000.00, score_anomalia=0.5800, alertado=True, estado='EN_REVISION'),
            OperacionAlerta(id_alerta='AL-2026-0007', numero_dam='118-2026-10-012339', fecha_operacion=datetime.strptime('2026-06-17', '%Y-%m-%d').date(), ruc_exportador='20123456789', razon_social='Agroworld S.A.C.', producto='Palta', valor_fob_declarado=130000.00, valor_fob_esperado=133000.00, score_anomalia=0.3500, alertado=False, estado='EN_REVISION'),
            
            # Alertas Históricas Auditadas
            OperacionAlerta(id_alerta='AL-2026-0009', numero_dam='118-2026-10-012341', fecha_operacion=datetime.strptime('2026-06-19', '%Y-%m-%d').date(), ruc_exportador='20123456789', razon_social='Agroworld S.A.C.', producto='Palta', valor_fob_declarado=110000.00, valor_fob_esperado=130000.00, score_anomalia=0.8800, alertado=True, estado='CONFIRMADA'),
            OperacionAlerta(id_alerta='AL-2026-0006', numero_dam='118-2026-10-012338', fecha_operacion=datetime.strptime('2026-06-16', '%Y-%m-%d').date(), ruc_exportador='20998877665', razon_social='BerryCorp Andina', producto='Arándano', valor_fob_declarado=150000.00, valor_fob_esperado=152000.00, score_anomalia=0.4200, alertado=False, estado='FALSA_ALARMA'),
            OperacionAlerta(id_alerta='AL-2026-0005', numero_dam='118-2026-10-012337', fecha_operacion=datetime.strptime('2026-06-15', '%Y-%m-%d').date(), ruc_exportador='20778899001', razon_social='Frutas del Pedregal S.A.', producto='Mango', valor_fob_declarado=55000.00, valor_fob_esperado=68000.00, score_anomalia=0.7600, alertado=True, estado='REFIERE_INSPECCION'),
            OperacionAlerta(id_alerta='AL-2026-0004', numero_dam='118-2026-10-012336', fecha_operacion=datetime.strptime('2026-06-14', '%Y-%m-%d').date(), ruc_exportador='20334455667', razon_social='Campos de Ica S.A.', producto='Palta', valor_fob_declarado=105000.00, valor_fob_esperado=108000.00, score_anomalia=0.3100, alertado=False, estado='FALSA_ALARMA')
        ]
        db.add_all(alertas)
        db.commit()
 
        # Obtener IDs de usuarios para relacionar las decisiones
        aud1 = db.query(Usuario).filter_by(username='auditor1').first()
        aud2 = db.query(Usuario).filter_by(username='auditor2').first()
        
        # 3. Insertar Decisiones de Auditoría
        decisiones = [
            DecisionAuditoria(id_alerta='AL-2026-0009', id_usuario=aud1.id_usuario, condicion_experimento='INTEGRADO', user_decision=1, justification_text='Subvaluación severa del FOB y desvío de temperatura de envío detectada.', likert_comprehension=5, time_to_decision_ms=25600, creado_en=datetime.now() - timedelta(hours=2)),
            DecisionAuditoria(id_alerta='AL-2026-0006', id_usuario=aud1.id_usuario, condicion_experimento='AISLADO', user_decision=0, justification_text='Desviación de precio marginal, comportamiento dentro de límites históricos.', likert_comprehension=3, time_to_decision_ms=49200, creado_en=datetime.now() - timedelta(hours=5)),
            DecisionAuditoria(id_alerta='AL-2026-0005', id_usuario=aud2.id_usuario, condicion_experimento='INTEGRADO', user_decision=2, justification_text='Riesgo de retraso aduanero y variación climática del lote ameritan inspección física.', likert_comprehension=4, time_to_decision_ms=31200, creado_en=datetime.now() - timedelta(hours=8)),
            DecisionAuditoria(id_alerta='AL-2026-0004', id_usuario=aud2.id_usuario, condicion_experimento='AISLADO', user_decision=0, justification_text='No se aprecian justificaciones de riesgo contundentes.', likert_comprehension=2, time_to_decision_ms=65400, creado_en=datetime.now() - timedelta(days=1))
        ]
        db.add_all(decisiones)
        
        # 4. Insertar Explicaciones SHAP
        shap_vals = [
            # AL-2026-0012 (Palta - Alta anomalía)
            ExplicacionSHAP(id_alerta='AL-2026-0012', variable_nombre='Precio Residual', shap_value=0.3200, variable_valor='Desvío: -$15,000'),
            ExplicacionSHAP(id_alerta='AL-2026-0012', variable_nombre='Desviación Temp.', shap_value=0.2100, variable_valor='+2.4°C en contenedor'),
            ExplicacionSHAP(id_alerta='AL-2026-0012', variable_nombre='Lluvias Origen', shap_value=0.1200, variable_valor='350mm acumulado'),
            ExplicacionSHAP(id_alerta='AL-2026-0012', variable_nombre='Retraso Logístico', shap_value=0.0800, variable_valor='+3 días en puerto'),
            ExplicacionSHAP(id_alerta='AL-2026-0012', variable_nombre='Perfil de Historial', shap_value=-0.1500, variable_valor='Favorable (bajo riesgo)'),
            
            # AL-2026-0011 (Uva)
            ExplicacionSHAP(id_alerta='AL-2026-0011', variable_nombre='Precio Residual', shap_value=0.2400, variable_valor='Desvío: -$25,000'),
            ExplicacionSHAP(id_alerta='AL-2026-0011', variable_nombre='Perfil de Historial', shap_value=0.1800, variable_valor='Frecuente (12 alertas previas)'),
            ExplicacionSHAP(id_alerta='AL-2026-0011', variable_nombre='Desviación Temp.', shap_value=0.1500, variable_valor='+1.8°C'),
            ExplicacionSHAP(id_alerta='AL-2026-0011', variable_nombre='Lluvias Origen', shap_value=-0.0500, variable_valor='Normal'),
            ExplicacionSHAP(id_alerta='AL-2026-0011', variable_nombre='Retraso Logístico', shap_value=0.0200, variable_valor='+1 día'),
            
            # AL-2026-0010 (Arándano)
            ExplicacionSHAP(id_alerta='AL-2026-0010', variable_nombre='Precio Residual', shap_value=0.1900, variable_valor='Desvío: -$15,000'),
            ExplicacionSHAP(id_alerta='AL-2026-0010', variable_nombre='Retraso Logístico', shap_value=0.1400, variable_valor='+4 días'),
            ExplicacionSHAP(id_alerta='AL-2026-0010', variable_nombre='Perfil de Historial', shap_value=0.1100, variable_valor='Moderado'),
            ExplicacionSHAP(id_alerta='AL-2026-0010', variable_nombre='Desviación Temp.', shap_value=-0.0400, variable_valor='Normal'),
            ExplicacionSHAP(id_alerta='AL-2026-0010', variable_nombre='Lluvias Origen', shap_value=-0.0100, variable_valor='Normal'),
 
            # AL-2026-0013 (Palta)
            ExplicacionSHAP(id_alerta='AL-2026-0013', variable_nombre='Precio Residual', shap_value=0.2000, variable_valor='Desvío: -$17,000'),
            ExplicacionSHAP(id_alerta='AL-2026-0013', variable_nombre='Desviación Temp.', shap_value=0.1200, variable_valor='+1.2°C'),
            ExplicacionSHAP(id_alerta='AL-2026-0013', variable_nombre='Perfil de Historial', shap_value=0.1000, variable_valor='Moderado'),
            
            # AL-2026-0014 (Mango)
            ExplicacionSHAP(id_alerta='AL-2026-0014', variable_nombre='Precio Residual', shap_value=0.2500, variable_valor='Desvío: -$15,000'),
            ExplicacionSHAP(id_alerta='AL-2026-0014', variable_nombre='Retraso Logístico', shap_value=0.1800, variable_valor='+5 días')
        ]
        db.add_all(shap_vals)
        
        # 5. Insertar Logs de Seguridad
        logs = [
            SecurityLog(usuario='auditor1', evento='LOGIN_SUCCESS', ip_address='192.168.1.15', fecha=datetime.now() - timedelta(hours=2)),
            SecurityLog(usuario='auditor2', evento='LOGIN_SUCCESS', ip_address='192.168.1.22', fecha=datetime.now() - timedelta(hours=8)),
            SecurityLog(usuario='admin', evento='LOGIN_SUCCESS', ip_address='192.168.1.100', fecha=datetime.now() - timedelta(hours=24)),
            SecurityLog(usuario='auditor1', evento='UNAUTHORIZED_ACCESS', ip_address='192.168.1.15', fecha=datetime.now() - timedelta(hours=1, minutes=30))
        ]
        db.add_all(logs)
        
        db.commit()
        print("Base de datos de PostgreSQL inicializada y sembrada exitosamente.")
        
        # 6. Sembrar Biblioteca RAG
        seed_normatives(db)
        
        # 7. Compilar y entrenar modelos analíticos
        compile_and_save_mock_models()
        
        # 8. Sembrar Configuración del Pipeline
        print("Sembrando configuración inicial del pipeline...")
        config_inicial = ConfiguracionPipeline(
            active_model='xgboost',
            weight_if=0.4500,
            weight_lof=0.3000,
            weight_ecod=0.2500,
            global_threshold=0.6500,
            llm_engine='Google Gemini 1.5 Flash',
            llm_temperature=0.10,
            llm_similarity_threshold=0.75
        )
        db.add(config_inicial)
        db.commit()
        print("Configuración sembrada exitosamente.")
        
        # Iniciar la migración e ingesta de datos reales y simulación de usabilidad
        try:
            import migrate_real_data
            print("Iniciando migración de datos reales de SUNAT y simulación de telemetría...")
            migrate_real_data.main()
        except Exception as err_mig:
            print(f"Advertencia: No se completó la migración de datos reales ({err_mig})")
        
    except Exception as e:
        db.rollback()
        print(f"Error al sembrar la base de datos: {e}")
        sys.exit(1)
    finally:
        db.close()
 
if __name__ == '__main__':
    wait_for_db()
    seed_db()
