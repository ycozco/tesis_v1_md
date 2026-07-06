import os
import random
from models import SessionLocal, OperacionAlerta, ExplicacionSHAP

def populate():
    db = SessionLocal()
    try:
        alerts = db.query(OperacionAlerta).all()
        count = 0
        for a in alerts:
            shaps = db.query(ExplicacionSHAP).filter_by(id_alerta=a.id_alerta).count()
            if shaps == 0:
                fob_dec = float(a.valor_fob_declarado)
                fob_esp = float(a.valor_fob_esperado)
                desvio_usd = fob_dec - fob_esp
                
                shap_precio = 0.1200
                if desvio_usd < -20000:
                    shap_precio = 0.3800
                if desvio_usd < -40000:
                    shap_precio = 0.5800
                
                ex_precio = ExplicacionSHAP(
                    id_alerta=a.id_alerta,
                    variable_nombre='Precio Residual',
                    shap_value=shap_precio,
                    variable_valor=f'Desvío: ${desvio_usd:,.2f}'
                )
                db.add(ex_precio)
                
                temp = float(a.temperatura) if a.temperatura else 4.0
                shap_temp = 0.0200
                if temp > 8.0:
                    shap_temp = 0.3100
                if temp > 12.0:
                    shap_temp = 0.4900
                
                prod = a.producto
                temp_diff = temp - 6.0 if prod == 'Palta' else temp - 1.0 if prod == 'Arándano' else temp - 2.0 if prod == 'Uva' else temp - 13.0
                ex_temp = ExplicacionSHAP(
                    id_alerta=a.id_alerta,
                    variable_nombre='Desviación Temp.',
                    shap_value=shap_temp,
                    variable_valor=f'+{temp_diff:.1f}°C en contenedor'
                )
                db.add(ex_temp)
                
                retraso = int(a.retraso_dias) if a.retraso_dias else 0
                shap_retraso = 0.0400
                if retraso > 5:
                    shap_retraso = 0.2800
                if retraso > 10:
                    shap_retraso = 0.4400
                    
                ex_retraso = ExplicacionSHAP(
                    id_alerta=a.id_alerta,
                    variable_nombre='Retraso Logístico',
                    shap_value=shap_retraso,
                    variable_valor=f'+{retraso} días en puerto'
                )
                db.add(ex_retraso)
                
                shap_historial = random.choice([0.1200, -0.0800, 0.0500])
                ex_historial = ExplicacionSHAP(
                    id_alerta=a.id_alerta,
                    variable_nombre='Perfil de Historial',
                    shap_value=shap_historial,
                    variable_valor='Favorable (bajo riesgo)' if shap_historial < 0 else 'Moderado (alertas previas)'
                )
                db.add(ex_historial)
                
                shap_lluvias = 0.2200 if retraso > 6 and temp > 4.0 else -0.0200
                ex_lluvias = ExplicacionSHAP(
                    id_alerta=a.id_alerta,
                    variable_nombre='Lluvias Origen',
                    shap_value=shap_lluvias,
                    variable_valor='Normal' if shap_lluvias < 0 else '350mm acumulado (Fenómeno El Niño)'
                )
                db.add(ex_lluvias)
                count += 1
                
        db.commit()
        print(f"Completado! Se poblaron SHAP para {count} alertas.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    populate()
