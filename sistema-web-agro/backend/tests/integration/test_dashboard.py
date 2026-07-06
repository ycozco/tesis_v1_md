import pytest
from fastapi.testclient import TestClient

from app_fastapi.main import app

client = TestClient(app)

def test_dashboard_stats_format():
    # If endpoint is protected, we'd need a token, but for now we left it open 
    # to match the current open behavior in Flask or it can be mocked.
    response = client.get("/api/dashboard/stats")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that it returns exactly what Flask used to return
    assert "active_alerts_count" in data
    assert "total_alerts_count" in data
    assert "avg_decision_time_s" in data
    assert "priority_alerts" in data
    assert "recent_logs" in data
    assert "trends_14_days" in data
    
    # Validate types
    assert isinstance(data["active_alerts_count"], int)
    assert isinstance(data["total_alerts_count"], int)
    assert isinstance(data["avg_decision_time_s"], float)
    assert isinstance(data["priority_alerts"], list)
    assert isinstance(data["recent_logs"], list)
    assert isinstance(data["trends_14_days"], list)
    
    # For trends_14_days, it should have 15 elements (14 to 0)
    assert len(data["trends_14_days"]) == 15
    assert "fecha" in data["trends_14_days"][0]
    assert "cantidad" in data["trends_14_days"][0]
