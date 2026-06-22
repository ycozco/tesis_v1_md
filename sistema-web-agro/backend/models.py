import os
from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pgvector.sqlalchemy import Vector
from datetime import datetime

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/agro_audit')

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

    decisiones = relationship("DecisionAuditoria", back_populates="alerta")
    explicaciones = relationship("ExplicacionSHAP", back_populates="alerta")

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
            'estado': self.estado
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
    embedding = Column(Vector(384)) # 384 dimensions for BGE-small-en-v1.5
    
    def to_dict(self):
        return {
            'id_doc': self.id_doc,
            'titulo': self.titulo,
            'categoria': self.categoria,
            'contenido': self.contenido
        }

def init_tables():
    Base.metadata.create_all(bind=engine)
