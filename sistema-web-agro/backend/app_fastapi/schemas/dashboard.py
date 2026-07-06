from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DashboardStatsResponse(BaseModel):
    active_alerts_count: int
    total_alerts_count: int
    avg_decision_time_s: float
    priority_alerts: List[Dict[str, Any]]
    recent_logs: List[Dict[str, Any]]
    trends_14_days: List[Dict[str, Any]]
