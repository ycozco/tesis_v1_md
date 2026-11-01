from datetime import date, timedelta


def test_dashboard_rejects_anonymous_requests(api_client):
    assert api_client.get('/api/dashboard/stats').status_code == 401


def test_dashboard_counts_actual_records(api_client, database_factory):
    import models
    today = date.today()
    with database_factory() as db:
        for index, day in enumerate([today, today, today-timedelta(days=1), today-timedelta(days=20)]):
            db.add(models.OperacionAlerta(id_alerta=f'fixture-{index}',numero_dam=f'TEST-{index}',
                fecha_operacion=day,ruc_exportador='00000000000',razon_social='Artificial test fixture',
                producto='palta',valor_fob_declarado=100,valor_fob_esperado=100,
                score_anomalia=.1,alertado=True,estado='PENDIENTE'))
        db.commit()
    login = api_client.post('/api/auth/login', json={'identifier': 'test-auditor', 'password': 'OnlyIsolatedTests2026!'})
    response = api_client.get('/api/dashboard/stats',headers={'Authorization':'Bearer '+login.json()['token']})
    assert response.status_code == 200
    data = response.json()
    assert data['total_alerts_count'] == data['active_alerts_count'] == 4
    assert len(data['trends_14_days']) == 14
    assert data['trends_14_days'][-1] == {'fecha':today.isoformat(),'cantidad':2}
    assert data['trends_14_days'][-2]['cantidad'] == 1
    assert sum(day['cantidad'] for day in data['trends_14_days']) == 3
