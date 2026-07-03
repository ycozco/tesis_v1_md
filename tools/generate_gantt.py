import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
from datetime import datetime

def generate_chart():
    # Set style
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    
    # Data for Gantt
    tasks = [
        {"Task": "Fase 1: Preparación y Tratamiento de Datos", "Start": "2026-05-01", "End": "2026-05-31", "Color": "#4F46E5"},
        {"Task": "Fase 2: Desarrollo Backend y Modelado", "Start": "2026-06-01", "End": "2026-07-31", "Color": "#6366F1"},
        {"Task": "Fase 3: Explicabilidad y Reportes RAG", "Start": "2026-08-01", "End": "2026-08-31", "Color": "#818CF8"},
        {"Task": "Fase 4: Integración del Pipeline y UI Dashboard", "Start": "2026-09-01", "End": "2026-09-30", "Color": "#A5B4FC"},
        {"Task": "Fase 5: Protocolo de Usabilidad con Testers", "Start": "2026-10-01", "End": "2026-10-31", "Color": "#10B981"},
        {"Task": "Fase 6: Pruebas de Calidad e Impl. de Cambios", "Start": "2026-11-01", "End": "2026-11-30", "Color": "#34D399"},
        {"Task": "Fase 7: Redacción Final de Capítulos y Anexos", "Start": "2026-11-01", "End": "2026-11-30", "Color": "#F59E0B"},
        {"Task": "Fase 8: Revisiones Finales y Sustentación", "Start": "2026-12-01", "End": "2026-12-07", "Color": "#EF4444"}
    ]

    df = pd.DataFrame(tasks)
    df['Start'] = pd.to_datetime(df['Start'])
    df['End'] = pd.to_datetime(df['End'])

    # Plot bars
    for i, task in enumerate(tasks):
        start_num = mdates.date2num(df.loc[i, 'Start'])
        end_num = mdates.date2num(df.loc[i, 'End'])
        duration = end_num - start_num
        if duration <= 0:
            duration = 7  # ensure minimum width for sub-week tasks
        ax.barh(df.loc[i, 'Task'], duration, left=start_num, color=task['Color'], height=0.55, edgecolor='black', linewidth=0.7, alpha=0.95)

    # Format axes
    ax.set_xlabel('Meses (2026)', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_title('Planificación de Tesis e Implementación (Mayo - Diciembre 2026)', fontsize=13, fontweight='bold', pad=15)
    
    # Set x axis monthly intervals
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
    
    # Grid and style
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    
    ax.invert_yaxis()  # Top-down order
    plt.yticks(fontsize=9.5, fontweight='semibold')
    plt.xticks(fontsize=9)

    plt.tight_layout()
    os.makedirs('d:/tesis_yoset/data/downloads', exist_ok=True)
    out_path = 'd:/tesis_yoset/data/downloads/gantt_chart.png'
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    print(f"Chart saved to {out_path}")

if __name__ == '__main__':
    generate_chart()
