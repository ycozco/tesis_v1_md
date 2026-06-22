import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

DB_PATH = 'agro_audit.db'

def init_db():
    print(f"Creando base de datos en: {os.path.abspath(DB_PATH)}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Tabla de Usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        rol VARCHAR(20) NOT NULL,
        nombre VARCHAR(100) NOT NULL
    )
    ''')
    
    # 2. Tabla de Operaciones y Alertas (Capas 1 y 2)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS OperacionesAlertas (
        id_alerta VARCHAR(50) PRIMARY KEY,
        numero_dam VARCHAR(50) NOT NULL,
        fecha_operacion DATE NOT NULL,
        ruc_exportador VARCHAR(11) NOT NULL,
        razon_social VARCHAR(100) NOT NULL,
        producto VARCHAR(50) NOT NULL,
        valor_fob_declarado DECIMAL(12,2) NOT NULL,
        valor_fob_esperado DECIMAL(12,2) NOT NULL,
        score_anomalia DECIMAL(5,4) NOT NULL,
        alertado BOOLEAN NOT NULL,
        estado VARCHAR(20) NOT NULL
    )
    ''')
    
    # 3. Tabla de Decisiones de Auditoría (Telemetría Usabilidad - Anexo A)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS DecisionesAuditoria (
        id_decision INTEGER PRIMARY KEY AUTOINCREMENT,
        id_alerta VARCHAR(50) NOT NULL,
        id_usuario INTEGER NOT NULL,
        condicion_experimento VARCHAR(15) NOT NULL,
        user_decision INTEGER NOT NULL,
        justification_text VARCHAR(250) NOT NULL,
        likert_comprehension INTEGER NOT NULL,
        time_to_decision_ms INTEGER NOT NULL,
        creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_alerta) REFERENCES OperacionesAlertas(id_alerta),
        FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
    )
    ''')
    
    # 4. Tabla de Explicaciones SHAP (Capa 3)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ExplicacionesSHAP (
        id_explicacion INTEGER PRIMARY KEY AUTOINCREMENT,
        id_alerta VARCHAR(50) NOT NULL,
        variable_nombre VARCHAR(50) NOT NULL,
        shap_value DECIMAL(8,6) NOT NULL,
        variable_valor VARCHAR(100) NOT NULL,
        FOREIGN KEY (id_alerta) REFERENCES OperacionesAlertas(id_alerta)
    )
    ''')
    
    # 5. Tabla de Logs de Seguridad (SBS N° 053-2023)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SecurityLogs (
        id_log INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario VARCHAR(50) NOT NULL,
        evento VARCHAR(100) NOT NULL,
        ip_address VARCHAR(40) NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Limpiar datos antiguos
    cursor.execute("DELETE FROM Usuarios")
    cursor.execute("DELETE FROM OperacionesAlertas")
    cursor.execute("DELETE FROM DecisionesAuditoria")
    cursor.execute("DELETE FROM ExplicacionesSHAP")
    cursor.execute("DELETE FROM SecurityLogs")
    
    # Insertar Usuarios Mock
    users = [
        ('auditor1', 'ycozco@unsa.edu.pe', generate_password_hash('correct'), 'AUDITOR', 'Yoset Cozco Mauri'),
        ('auditor2', 'auditor_fito@agro.gob.pe', generate_password_hash('correct'), 'AUDITOR', 'Ing. Carlos Mendoza'),
        ('admin', 'vcornejo@unsa.edu.pe', generate_password_hash('correct'), 'ADMIN', 'Dr. Víctor Cornejo Aparicio')
    ]
    cursor.executemany("INSERT INTO Usuarios (username, email, password_hash, rol, nombre) VALUES (?, ?, ?, ?, ?)", users)
    
    # Insertar Alertas Mock
    alerts = [
        # Alertas Pendientes
        ('AL-2026-0012', '118-2026-10-012345', '2026-06-21', '20123456789', 'Agroworld S.A.C.', 'Palta', 120000.00, 135000.00, 0.9500, 1, 'PENDIENTE'),
        ('AL-2026-0011', '118-2026-10-012346', '2026-06-20', '20556677889', 'Valles del Norte EIRL', 'Uva', 85000.00, 110000.00, 0.7200, 1, 'PENDIENTE'),
        ('AL-2026-0010', '118-2026-10-012347', '2026-06-20', '20998877665', 'BerryCorp Andina', 'Arándano', 145000.00, 160000.00, 0.6500, 1, 'PENDIENTE'),
        ('AL-2026-0013', '118-2026-10-012348', '2026-06-21', '20334455667', 'Campos de Ica S.A.', 'Palta', 95000.00, 112000.00, 0.7800, 1, 'PENDIENTE'),
        ('AL-2026-0014', '118-2026-10-012349', '2026-06-21', '20778899001', 'Frutas del Pedregal S.A.', 'Mango', 60000.00, 75000.00, 0.8200, 1, 'PENDIENTE'),
        
        # Alertas En Revisión
        ('AL-2026-0008', '118-2026-10-012340', '2026-06-18', '20556677889', 'Valles del Norte EIRL', 'Uva', 98000.00, 105000.00, 0.5800, 1, 'EN_REVISION'),
        ('AL-2026-0007', '118-2026-10-012339', '2026-06-17', '20123456789', 'Agroworld S.A.C.', 'Palta', 130000.00, 133000.00, 0.3500, 0, 'EN_REVISION'),
        
        # Alertas Históricas Auditadas
        ('AL-2026-0009', '118-2026-10-012341', '2026-06-19', '20123456789', 'Agroworld S.A.C.', 'Palta', 110000.00, 130000.00, 0.8800, 1, 'CONFIRMADA'),
        ('AL-2026-0006', '118-2026-10-012338', '2026-06-16', '20998877665', 'BerryCorp Andina', 'Arándano', 150000.00, 152000.00, 0.4200, 0, 'FALSA_ALARMA'),
        ('AL-2026-0005', '118-2026-10-012337', '2026-06-15', '20778899001', 'Frutas del Pedregal S.A.', 'Mango', 55000.00, 68000.00, 0.7600, 1, 'REFIERE_INSPECCION'),
        ('AL-2026-0004', '118-2026-10-012336', '2026-06-14', '20334455667', 'Campos de Ica S.A.', 'Palta', 105000.00, 108000.00, 0.3100, 0, 'FALSA_ALARMA')
    ]
    cursor.executemany("""
    INSERT INTO OperacionesAlertas (
        id_alerta, numero_dam, fecha_operacion, ruc_exportador, razon_social, 
        producto, valor_fob_declarado, valor_fob_esperado, score_anomalia, alertado, estado
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", alerts)
    
    # Insertar Decisiones de Auditoría Históricas
    # Para simular las métricas de usabilidad en el dashboard experimental
    # auditor1 (id_usuario=1) completó algunas tareas
    # auditor2 (id_usuario=2) completó otras
    decisions = [
        # id_decision, id_alerta, id_usuario, condicion_experimento, user_decision, justification_text, likert_comprehension, time_to_decision_ms, creado_en
        (1, 'AL-2026-0009', 1, 'INTEGRADO', 1, 'Subvaluación severa del FOB y desvío de temperatura de envío detectada.', 5, 25600, (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')),
        (2, 'AL-2026-0006', 1, 'AISLADO', 0, 'Desviación de precio marginal, comportamiento dentro de límites históricos.', 3, 49200, (datetime.now() - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')),
        (3, 'AL-2026-0005', 2, 'INTEGRADO', 2, 'Riesgo de retraso aduanero y variación climática del lote ameritan inspección física.', 4, 31200, (datetime.now() - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')),
        (4, 'AL-2026-0004', 2, 'AISLADO', 0, 'No se aprecian justificaciones de riesgo contundentes.', 2, 65400, (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'))
    ]
    cursor.executemany("""
    INSERT INTO DecisionesAuditoria (
        id_decision, id_alerta, id_usuario, condicion_experimento, user_decision, 
        justification_text, likert_comprehension, time_to_decision_ms, creado_en
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", decisions)
    
    # Insertar Explicaciones SHAP (Capa 3)
    shap_vals = [
        # AL-2026-0012 (Palta - Alta anomalía)
        ('AL-2026-0012', 'Precio Residual', 0.3200, 'Desvío: -$15,000'),
        ('AL-2026-0012', 'Desviación Temp.', 0.2100, '+2.4°C en contenedor'),
        ('AL-2026-0012', 'Lluvias Origen', 0.1200, '350mm acumulado'),
        ('AL-2026-0012', 'Retraso Logístico', 0.0800, '+3 días en puerto'),
        ('AL-2026-0012', 'Perfil de Historial', -0.1500, 'Favorable (bajo riesgo)'),
        
        # AL-2026-0011 (Uva)
        ('AL-2026-0011', 'Precio Residual', 0.2400, 'Desvío: -$25,000'),
        ('AL-2026-0011', 'Perfil de Historial', 0.1800, 'Frecuente (12 alertas previas)'),
        ('AL-2026-0011', 'Desviación Temp.', 0.1500, '+1.8°C'),
        ('AL-2026-0011', 'Lluvias Origen', -0.0500, 'Normal'),
        ('AL-2026-0011', 'Retraso Logístico', 0.0200, '+1 día'),

        # AL-2026-0010 (Arándano)
        ('AL-2026-0010', 'Precio Residual', 0.1900, 'Desvío: -$15,000'),
        ('AL-2026-0010', 'Retraso Logístico', 0.1400, '+4 días'),
        ('AL-2026-0010', 'Perfil de Historial', 0.1100, 'Moderado'),
        ('AL-2026-0010', 'Desviación Temp.', -0.0400, 'Normal'),
        ('AL-2026-0010', 'Lluvias Origen', -0.0100, 'Normal')
    ]
    cursor.executemany("""
    INSERT INTO ExplicacionesSHAP (id_alerta, variable_nombre, shap_value, variable_valor) 
    VALUES (?, ?, ?, ?)""", shap_vals)
    
    # Insertar Logs de Seguridad Mock
    logs = [
        ('auditor1', 'LOGIN_SUCCESS', '192.168.1.15', (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')),
        ('auditor2', 'LOGIN_SUCCESS', '192.168.1.22', (datetime.now() - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')),
        ('admin', 'LOGIN_SUCCESS', '192.168.1.100', (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')),
        ('auditor1', 'UNAUTHORIZED_ACCESS', '192.168.1.15', (datetime.now() - timedelta(hours=1, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'))
    ]
    cursor.executemany("INSERT INTO SecurityLogs (usuario, evento, ip_address, fecha) VALUES (?, ?, ?, ?)", logs)
    
    conn.commit()
    conn.close()
    print("Base de datos inicializada exitosamente.")

if __name__ == '__main__':
    init_db()
