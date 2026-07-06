import os
import time
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("La librería 'playwright' no está instalada. Instalándola automáticamente...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install"])
    from playwright.sync_api import sync_playwright

def capture():
    # Crear carpeta de capturas si no existe
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "screenshots")
    os.makedirs(output_dir, exist_ok=True)
    print(f"Las capturas se guardarán en: {output_dir}")

    with sync_playwright() as p:
        print("Iniciando navegador...")
        browser = p.chromium.launch(headless=True)
        # Configurar pantalla completa Full HD
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # 1. Login
        print("Accediendo a la página de Login...")
        page.goto("http://localhost:8050/login")
        page.wait_for_load_state("networkidle")
        
        print("Realizando inicio de sesión...")
        page.fill("#identifier", "auditor1")
        page.fill("#password", "correct")
        page.click("button[type='submit']")
        page.wait_for_url("**/dashboard")
        page.wait_for_load_state("networkidle")
        time.sleep(2)  # Dar tiempo a animaciones del Dashboard

        # 2. Captura: Dashboard Principal (Completo y Secciones)
        print("Capturando Dashboard...")
        page.screenshot(path=os.path.join(output_dir, "dashboard_completo.png"), full_page=True)
        
        # Captura sección del scatter plot
        scatter = page.query_selector(".glass-panel:has-text('Relación FOB Declarado vs Esperado')")
        if scatter:
            scatter.screenshot(path=os.path.join(output_dir, "dashboard_scatter_chart.png"))
            
        # Captura sección de distribución de desvío
        dist = page.query_selector(".glass-panel:has-text('Distribución del Desvío Porcentual')")
        if dist:
            dist.screenshot(path=os.path.join(output_dir, "dashboard_deviation_chart.png"))

        # 3. Captura: Bandeja de Alertas
        print("Capturando Bandeja de Alertas...")
        page.goto("http://localhost:8050/alerts")
        page.wait_for_load_state("networkidle")
        time.sleep(1.5)
        page.screenshot(path=os.path.join(output_dir, "bandeja_alertas_completa.png"), full_page=True)
        
        # Tabla de alertas
        table = page.query_selector(".glass-panel:has(table)")
        if table:
            table.screenshot(path=os.path.join(output_dir, "bandeja_alertas_tabla.png"))

        # 4. Captura: Detalle de Alerta (Capa 1 a 4 y Distribución)
        # Buscamos la primera alerta disponible en la bandeja para auditar
        alert_row = page.query_selector("table tbody tr")
        if alert_row:
            alert_link = alert_row.query_selector("a")
            if alert_link:
                alert_url = "http://localhost:8050" + alert_link.get_attribute("href")
                print(f"Navegando a detalle de alerta: {alert_url}")
                page.goto(alert_url)
                page.wait_for_load_state("networkidle")
                time.sleep(2.5)  # Esperar carga de modelo SHAP y RAG
                
                # Detalle completo
                page.screenshot(path=os.path.join(output_dir, "detalle_alerta_completo.png"), full_page=True)
                
                # Gráfico de SHAP
                shap = page.query_selector(".glass-panel:has-text('SHAP Explicabilidad Local')")
                if shap:
                    shap.screenshot(path=os.path.join(output_dir, "detalle_alerta_shap.png"))
                    
                # Gráfico de distribución de probabilidad nuevo
                prob = page.query_selector(".glass-panel:has-text('Distribución de Probabilidad y Densidad')")
                if prob:
                    prob.screenshot(path=os.path.join(output_dir, "detalle_alerta_probabilidad_kde.png"))
                    
                # Reporte RAG
                rag = page.query_selector(".glass-panel:has-text('Plan de Acción y Corrección Recomendado')")
                if not rag:
                    rag = page.query_selector(".glass-panel:has-text('Recomendación')")
                if rag:
                    rag.screenshot(path=os.path.join(output_dir, "detalle_alerta_rag_report.png"))

        # 5. Captura: Telemetría y Simulación
        print("Capturando Consola de Telemetría...")
        page.goto("http://localhost:8050/telemetry")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(output_dir, "telemetria_consola_completa.png"), full_page=True)
        
        # Log persistente de inyección
        inj_log = page.query_selector(".glass-panel:has-text('Log de Inyecciones')")
        if inj_log:
            inj_log.screenshot(path=os.path.join(output_dir, "telemetria_inyecciones_log.png"))

        # 6. Captura: Equidad e Integridad
        print("Capturando Dashboard de Integridad...")
        page.goto("http://localhost:8050/integrity")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(output_dir, "integridad_completa.png"), full_page=True)

        # 7. Captura: Configuración
        print("Capturando Configuración...")
        page.goto("http://localhost:8050/config")
        page.wait_for_load_state("networkidle")
        time.sleep(1.5)
        page.screenshot(path=os.path.join(output_dir, "configuracion_pipeline.png"), full_page=True)

        browser.close()
        print("¡Proceso de captura completado exitosamente!")

if __name__ == '__main__':
    capture()
