import os
from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    Vector = None
from datetime import datetime

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/agro_audit')

if DATABASE_URL.startswith("sqlite") or "sqlite" in DATABASE_URL or Vector is None:
    from sqlalchemy import Text as SqliteText
    embedding_type = SqliteText
    # Asegurar que la ruta de SQLite sea absoluta relativa a la raíz de la tesis
    if DATABASE_URL.startswith("sqlite:///"):
        rel_path = DATABASE_URL.replace("sqlite:///", "")
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(backend_dir))
        # Quitar prefijo redundante si existe
        if rel_path.startswith("sistema-web-agro/"):
            rel_path = rel_path.replace("sistema-web-agro/", "")
        abs_db_path = os.path.abspath(os.path.join(root_dir, "sistema-web-agro", rel_path))
        DATABASE_URL = f"sqlite:///{abs_db_path}"
else:
    embedding_type = Vector(384)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)  # 'ADMIN' or 'AUDITOR'
    nombre = Column(String(100), nullable=False)

    decisiones = relationship("DecisionAuditoria", back_populates="usuario")

    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'username': self.username,
            'email': self.email,
            'rol': self.rol,
            'nombre': self.nombre
        }

class OperacionAlerta(Base):
    __tablename__ = 'operaciones_alertas'
    
    id_alerta = Column(String(50), primary_key=True)
    numero_dam = Column(String(50), nullable=False)
    fecha_operacion = Column(Date, nullable=False)
    ruc_exportador = Column(String(11), nullable=False)
    razon_social = Column(String(100), nullable=False)
    producto = Column(String(50), nullable=False)
    valor_fob_declarado = Column(Numeric(12, 2), nullable=False)
    valor_fob_esperado = Column(Numeric(12, 2), nullable=False)
    score_anomalia = Column(Numeric(5, 4), nullable=False)
    alertado = Column(Boolean, nullable=False)
    estado = Column(String(20), nullable=False) # 'PENDIENTE', 'EN_REVISION', 'CONFIRMADA', 'FALSA_ALARMA', 'REFIERE_INSPECCION'
    
    # Nuevos campos de variables persistidas del pipeline real
    peso_neto = Column(Numeric(12, 2), nullable=True)
    temperatura = Column(Numeric(5, 2), nullable=True)
    retraso_dias = Column(Integer, nullable=True)
    residuos_fob = Column(Numeric(12, 4), nullable=True)
    residuos_volumen = Column(Numeric(12, 4), nullable=True)
    run_id = Column(String(50), nullable=True)
    if_score = Column(Numeric(5, 4), nullable=True)
    lof_score = Column(Numeric(5, 4), nullable=True)
    ecod_score = Column(Numeric(5, 4), nullable=True)

    decisiones = relationship("DecisionAuditoria", back_populates="alerta")
    explicaciones = relationship("ExplicacionSHAP", back_populates="alerta")
    reporte = relationship("GeneratedReport", back_populates="alerta", uselist=False)

    def to_dict(self):
        return {
            'id_alerta': self.id_alerta,
            'numero_dam': self.numero_dam,
            'fecha_operacion': self.fecha_operacion.isoformat() if self.fecha_operacion else None,
            'ruc_exportador': self.ruc_exportador,
            'razon_social': self.razon_social,
            'producto': self.producto,
            'valor_fob_declarado': float(self.valor_fob_declarado),
            'valor_fob_esperado': float(self.valor_fob_esperado),
            'score_anomalia': float(self.score_anomalia),
            'alertado': self.alertado,
            'estado': self.estado,
            'peso_neto': float(self.peso_neto) if self.peso_neto is not None else 0.0,
            'temperatura': float(self.temperatura) if self.temperatura is not None else 0.0,
            'retraso_dias': int(self.retraso_dias) if self.retraso_dias is not None else 0,
            'residuos_fob': float(self.residuos_fob) if self.residuos_fob is not None else 0.0,
            'residuos_volumen': float(self.residuos_volumen) if self.residuos_volumen is not None else 0.0,
            'run_id': self.run_id or '',
            'if_score': float(self.if_score) if self.if_score is not None else 0.0,
            'lof_score': float(self.lof_score) if self.lof_score is not None else 0.0,
            'ecod_score': float(self.ecod_score) if self.ecod_score is not None else 0.0
        }

class DecisionAuditoria(Base):
    __tablename__ = 'decisiones_auditoria'
    
    id_decision = Column(Integer, primary_key=True, autoincrement=True)
    id_alerta = Column(String(50), ForeignKey('operaciones_alertas.id_alerta'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    condicion_experimento = Column(String(15), nullable=False) # 'INTEGRADO' or 'AISLADO'
    user_decision = Column(Integer, nullable=False) # 0=Normal, 1=Anomalía, 2=Dudoso
    justification_text = Column(String(250), nullable=False)
    likert_comprehension = Column(Integer, nullable=False)
    time_to_decision_ms = Column(Integer, nullable=False)
    creado_en = Column(DateTime, default=datetime.utcnow)

    alerta = relationship("OperacionAlerta", back_populates="decisiones")
    usuario = relationship("Usuario", back_populates="decisiones")

    def to_dict(self):
        return {
            'id_decision': self.id_decision,
            'id_alerta': self.id_alerta,
            'id_usuario': self.id_usuario,
            'usuario_nombre': self.usuario.nombre if self.usuario else '',
            'condicion_experimento': self.condicion_experimento,
            'user_decision': self.user_decision,
            'justification_text': self.justification_text,
            'likert_comprehension': self.likert_comprehension,
            'time_to_decision_ms': self.time_to_decision_ms,
            'creado_en': self.creado_en.isoformat() if self.creado_en else None
        }

class ExplicacionSHAP(Base):
    __tablename__ = 'explicaciones_shap'
    
    id_explicacion = Column(Integer, primary_key=True, autoincrement=True)
    id_alerta = Column(String(50), ForeignKey('operaciones_alertas.id_alerta'), nullable=False)
    variable_nombre = Column(String(50), nullable=False)
    shap_value = Column(Numeric(16, 6), nullable=False)
    variable_valor = Column(String(100), nullable=False)

    alerta = relationship("OperacionAlerta", back_populates="explicaciones")

    def to_dict(self):
        return {
            'id_explicacion': self.id_explicacion,
            'id_alerta': self.id_alerta,
            'variable_nombre': self.variable_nombre,
            'shap_value': float(self.shap_value),
            'variable_valor': self.variable_valor
        }

class SecurityLog(Base):
    __tablename__ = 'security_logs'
    
    id_log = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(50), nullable=False)
    evento = Column(String(100), nullable=False)
    ip_address = Column(String(40), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id_log': self.id_log,
            'usuario': self.usuario,
            'evento': self.evento,
            'ip_address': self.ip_address,
            'fecha': self.fecha.isoformat() if self.fecha else None
        }

class DocumentoNormativo(Base):
    __tablename__ = 'documentos_normativos'
    
    id_doc = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(150), nullable=False)
    categoria = Column(String(50), nullable=False) # 'FDA', 'SENASA', 'LEY_IA'
    contenido = Column(Text, nullable=False)
    embedding = Column(embedding_type) # 384 dimensions for BGE-small-en-v1.5
    
    def to_dict(self):
        return {
            'id_doc': self.id_doc,
            'titulo': self.titulo,
            'categoria': self.categoria,
            'contenido': self.contenido
        }

class ConfiguracionPipeline(Base):
    __tablename__ = 'configuraciones_pipeline'
    
    id_config = Column(Integer, primary_key=True, autoincrement=True)
    active_model = Column(String(50), default='xgboost', nullable=False)
    weight_if = Column(Numeric(5, 4), default=0.4500, nullable=False)
    weight_lof = Column(Numeric(5, 4), default=0.3000, nullable=False)
    weight_ecod = Column(Numeric(5, 4), default=0.2500, nullable=False)
    global_threshold = Column(Numeric(5, 4), default=0.6500, nullable=False)
    llm_engine = Column(String(50), default='Google Gemini 1.5 Flash', nullable=False)
    llm_temperature = Column(Numeric(3, 2), default=0.10, nullable=False)
    llm_similarity_threshold = Column(Numeric(3, 2), default=0.75, nullable=False)
    
    def to_dict(self):
        return {
            'id_config': self.id_config,
            'active_model': self.active_model,
            'weight_if': float(self.weight_if),
            'weight_lof': float(self.weight_lof),
            'weight_ecod': float(self.weight_ecod),
            'global_threshold': float(self.global_threshold),
            'llm_engine': self.llm_engine,
            'llm_temperature': float(self.llm_temperature),
            'llm_similarity_threshold': float(self.llm_similarity_threshold)
        }

# Nuevas Tablas de Consolidacion Cientifica y Trazabilidad

class PipelineRun(Base):
    __tablename__ = 'pipeline_runs'
    
    run_id = Column(String(50), primary_key=True)
    execution_date = Column(DateTime, default=datetime.utcnow)
    dataset_version = Column(String(50), nullable=False)
    dataset_hash = Column(String(64), nullable=False)
    model_xgb_price_hash = Column(String(64), nullable=True)
    model_lgb_price_hash = Column(String(64), nullable=True)
    model_if_hash = Column(String(64), nullable=True)
    status = Column(String(20), nullable=False)

    def to_dict(self):
        return {
            'run_id': self.run_id,
            'execution_date': self.execution_date.isoformat() if self.execution_date else None,
            'dataset_version': self.dataset_version,
            'dataset_hash': self.dataset_hash,
            'model_xgb_price_hash': self.model_xgb_price_hash,
            'model_lgb_price_hash': self.model_lgb_price_hash,
            'model_if_hash': self.model_if_hash,
            'status': self.status
        }

class GeneratedReport(Base):
    __tablename__ = 'generated_reports'
    
    id_alerta = Column(String(50), ForeignKey('operaciones_alertas.id_alerta'), primary_key=True)
    report_text = Column(Text, nullable=False)
    fidelity_score = Column(Numeric(5, 4), nullable=True)
    completeness_score = Column(Numeric(5, 4), nullable=True)
    validation_status = Column(String(20), nullable=False)
    numeric_checks = Column(Integer, default=0)
    unsupported_claims = Column(Integer, default=0)
    report_hash = Column(String(64), nullable=False)
    report_uuid = Column(String(50), nullable=False)

    alerta = relationship("OperacionAlerta", back_populates="reporte")

    def to_dict(self):
        return {
            'id_alerta': self.id_alerta,
            'report_text': self.report_text,
            'fidelity_score': float(self.fidelity_score) if self.fidelity_score is not None else 0.0,
            'completeness_score': float(self.completeness_score) if self.completeness_score is not None else 0.0,
            'validation_status': self.validation_status,
            'numeric_checks': self.numeric_checks,
            'unsupported_claims': self.unsupported_claims,
            'report_hash': self.report_hash,
            'report_uuid': self.report_uuid
        }

class ArtifactLineage(Base):
    __tablename__ = 'artifact_lineage'
    
    id_artifact = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(50), ForeignKey('pipeline_runs.run_id'), nullable=False)
    name = Column(String(100), nullable=False)
    filepath = Column(String(255), nullable=False)
    hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id_artifact': self.id_artifact,
            'run_id': self.run_id,
            'name': self.name,
            'filepath': self.filepath,
            'hash': self.hash,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

def init_tables():
    Base.metadata.create_all(bind=engine)
