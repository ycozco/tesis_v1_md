import random
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app_fastapi.api.deps import get_db, get_current_user
from app_fastapi.schemas.dashboard import DashboardStatsResponse
from models import OperacionAlerta, DecisionAuditoria, SecurityLog, Usuario

router = APIRouter()

@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    # Descomentar para asegurar que el endpoint esté protegido
    # current_user: Usuario = Depends(get_current_user)
):
    # Alertas activas (PENDIENTE / EN_REVISION)
    active_count = db.query(OperacionAlerta).filter(
        OperacionAlerta.estado.in_(['PENDIENTE', 'EN_REVISION'])
    ).count()

    # Operaciones totales analizadas
    total_count = db.query(OperacionAlerta).count()

    # Tiempo promedio de decisión (segundos)
    avg_ms = db.query(func.avg(DecisionAuditoria.time_to_decision_ms)).scalar()
    avg_s = round((float(avg_ms) / 1000.0), 1) if avg_ms is not None else 0.0

    # Alertas prioritarias (límite 5)
    priority_alerts = db.query(OperacionAlerta).filter(
        OperacionAlerta.estado.in_(['PENDIENTE', 'EN_REVISION'])
    ).order_by(OperacionAlerta.score_anomalia.desc()).limit(5).all()

    priority_list = [a.to_dict() for a in priority_alerts]

    # Logs de telemetría recientes
    logs = db.query(SecurityLog).order_by(SecurityLog.fecha.desc()).limit(8).all()
    logs_list = [l.to_dict() for l in logs]

    # Simular serie de tendencias de alertas (últimos 14 días)
    trends = []
    today = datetime.now()
    for i in range(14, -1, -1):
        date_str = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        random.seed(date_str)
        count = random.randint(3, 18)
        trends.append({'fecha': date_str, 'cantidad': count})

    return {
        'active_alerts_count': active_count,
        'total_alerts_count': total_count,
        'avg_decision_time_s': avg_s,
        'priority_alerts': priority_list,
        'recent_logs': logs_list,
        'trends_14_days': trends
    }
