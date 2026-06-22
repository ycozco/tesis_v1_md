import os
import re

# Carpetas de origen y destino
SRC_DIR = '.'
TEMPLATES_DIR = 'templates'

os.makedirs(TEMPLATES_DIR, exist_ok=True)

def clean_main_content(html):
    # Extraer el contenido dentro de <main>...</main>
    main_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    if not main_match:
        return ""
    content = main_match.group(1)
    
    # Quitar banners globales repetitivos del entorno ya que están en base.html
    content = re.sub(
        r'<div class="mb-6 flex items-center justify-center w-full py-1\.5 glass-panel rounded-md[^"]*">.*?</div>',
        '',
        content,
        flags=re.DOTALL
    )
    return content

# 1. Crear base.html
# Extraeremos el head, el sidebar y el topnav de panel_del_auditor_final_esp/code.html
dashboard_src = os.path.join(SRC_DIR, 'panel_del_auditor_final_esp', 'code.html')

if os.path.exists(dashboard_src):
    with open(dashboard_src, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Extraer el Head
    head_match = re.search(r'<head>(.*?)</head>', html, re.DOTALL)
    head_content = head_match.group(1) if head_match else ''
    
    # Cambiar el título por una etiqueta dinámica
    head_content = re.sub(r'<title>.*?</title>', '<title>{% block title %}Oversight{% endblock %} - Agro-Intelligence Oversight</title>', head_content)
    
    # Extraer el Body y dividirlo en Sidebar, TopNavBar, y el Main block
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    body_content = body_match.group(1) if body_match else ''
    
    # Extraer Aside (Sidebar)
    aside_match = re.search(r'(<!-- SideNavBar[^>]*-->.*?<aside[^>]*>.*?</aside>)', body_content, re.DOTALL)
    if not aside_match:
        aside_match = re.search(r'(<aside[^>]*>.*?</aside>)', body_content, re.DOTALL)
    aside_content = aside_match.group(1) if aside_match else ''
    
    # Reescribir de forma más limpia la lista de navegación en base.html
    nav_list = """
<ul class="space-y-2">
<li>
<a class="flex items-center px-4 py-3 {% if active_page == 'dashboard' %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:text-primary hover:bg-surface-variant/20{% endif %} rounded-lg mx-2 transition-all duration-300" href="{{ url_for('dashboard') }}">
<span class="material-symbols-outlined shrink-0" data-icon="dashboard">dashboard</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Dashboard</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 {% if active_page == 'alerts' %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:text-primary hover:bg-surface-variant/20{% endif %} rounded-lg mx-2 transition-all duration-300" href="{{ url_for('alerts') }}">
<span class="material-symbols-outlined shrink-0" data-icon="security_update_warning">security_update_warning</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Bandeja Alertas</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 {% if active_page == 'data' %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:text-primary hover:bg-surface-variant/20{% endif %} rounded-lg mx-2 transition-all duration-300" href="{{ url_for('data_explorer') }}">
<span class="material-symbols-outlined shrink-0" data-icon="monitoring">monitoring</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Explorar Datos</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 {% if active_page == 'history' %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:text-primary hover:bg-surface-variant/20{% endif %} rounded-lg mx-2 transition-all duration-300" href="{{ url_for('history') }}">
<span class="material-symbols-outlined shrink-0" data-icon="fact_check">fact_check</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Historial Auditorías</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 {% if active_page == 'config' %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:text-primary hover:bg-surface-variant/20{% endif %} rounded-lg mx-2 transition-all duration-300" href="{{ url_for('config') }}">
<span class="material-symbols-outlined shrink-0" data-icon="settings">settings</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Configuración</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 {% if active_page == 'integrity' %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:text-primary hover:bg-surface-variant/20{% endif %} rounded-lg mx-2 transition-all duration-300" href="{{ url_for('integrity') }}">
<span class="material-symbols-outlined shrink-0" data-icon="shield">shield</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Integridad y Sesgo</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 {% if active_page == 'users' %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:text-primary hover:bg-surface-variant/20{% endif %} rounded-lg mx-2 transition-all duration-300" href="{{ url_for('users') }}">
<span class="material-symbols-outlined shrink-0" data-icon="supervisor_account">supervisor_account</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Control Usuarios</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 {% if active_page == 'telemetry' %}bg-primary-container text-on-primary-container{% else %}text-on-surface-variant hover:text-primary hover:bg-surface-variant/20{% endif %} rounded-lg mx-2 transition-all duration-300" href="{{ url_for('telemetry') }}">
<span class="material-symbols-outlined shrink-0" data-icon="science">science</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Telemetría Experimento</span>
</a>
</li>
</ul>
"""
    # Reemplazar la sección de navegación en aside_content
    nav_block_match = re.search(r'<nav[^>]*>.*?</nav>', aside_content, re.DOTALL)
    if nav_block_match:
        aside_content = aside_content.replace(nav_block_match.group(0), f"<nav class=\"flex-1 overflow-y-auto\">{nav_list}</nav>")
        
    # Modificar los links del footer del aside
    aside_content = re.sub(
        r'<span class="material-symbols-outlined shrink-0" data-icon="logout">logout</span>\s*<span class="[^"]*">Cerrar Sesión</span>',
        r'<span class="material-symbols-outlined shrink-0" data-icon="logout">logout</span><span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Cerrar Sesión</span>',
        aside_content
    )
    aside_content = re.sub(
        r'href="#"',
        r'href="{{ url_for(\'logout\') }}"',
        aside_content
    )
    
    # Extraer TopNavBar (Web)
    topnav_match = re.search(r'(<!-- TopNavBar[^>]*-->.*?<nav[^>]*>.*?</nav>)', body_content, re.DOTALL)
    if not topnav_match:
        topnav_match = re.search(r'(<nav[^>]*>.*?</nav>)', body_content, re.DOTALL)
    topnav_content = topnav_match.group(1) if topnav_match else ''
    
    # Hacer dinámico el nombre del auditor y su foto en topnav
    topnav_content = re.sub(
        r'<div class="w-8 h-8 rounded-full bg-surface-container-high border border-primary/30 overflow-hidden ml-2 cursor-pointer">.*?</div>',
        r'<div class="flex items-center gap-2 ml-2"><span class="text-body-sm text-on-surface font-medium">{{ session.get("nombre", "Auditor") }}</span><div class="w-8 h-8 rounded-full bg-surface-container-high border border-primary/30 overflow-hidden cursor-pointer"><img alt="Perfil" class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCxwvAsWimcF03V3njsUr4hg_f38wYuUsLCKv-xiu1PqPz3NR0-RIDqBBNh9BwgAvS4ns7FUNBXzxJ7wtir0npR8M3RPlm_whruKlOLHu7mBAhj9UF9FC6Ux9yZFTa-bKIkz5L2xU5CG3U1ETCNh4zAtHRLCE0utlfji8bJ1Tbf87aVkzvF-PF-2Slr3QZHlE-nDxHkXAMrMMDeWRV6ituElBxadSzZzBDRq378bk6lfFuG5I7oDw0ZHMmUPmTDlExpdWyT9v48Xv4"/></div></div>',
        topnav_content,
        flags=re.DOTALL
    )
    
    # Crear la plantilla base.html (sin f-string para evitar conflictos con Jinja2)
    base_html = """<!DOCTYPE html>
<html class="dark" lang="es">
<head>
    {head_content}
    {% block extra_head %}{% endblock %}
</head>
<body class="bg-background text-on-background font-body-md antialiased min-h-screen overflow-x-hidden selection:bg-primary-container selection:text-on-primary-container">
    
    <!-- Barra superior para Web -->
    {topnav_content}

    <!-- Contenedor Lateral y Contenido Principal -->
    <div class="flex h-screen pt-16 md:pt-0">
        <!-- Navegación lateral -->
        {aside_content}

        <!-- Lienzo de Contenido Principal -->
        <main class="flex-1 md:ml-20 w-full overflow-y-auto bg-background px-4 md:px-container-padding py-8 md:pt-24 pb-24 relative z-10">
            <!-- Global Environment Banner -->
            <div class="mb-6 flex items-center justify-center w-full py-1.5 glass-panel rounded-md border-tertiary/30 bg-tertiary/5 text-tertiary font-mono-data text-mono-data uppercase">
                <span class="material-symbols-outlined text-[16px] mr-2" data-icon="science">science</span>
                {% if session.get('condicion') %}
                    ENTORNO DE PRUEBA · EVALUACIÓN EN CURSO ({{ session.get('condicion') }})
                {% else %}
                    ENTORNO DE DEMOSTRACIÓN · DATOS SINTÉTICOS
                {% endif %}
            </div>

            {% block content %}{% endblock %}
        </main>
    </div>

    <!-- Navegación Móvil Inferior -->
    <nav class="md:hidden fixed bottom-0 w-full h-16 bg-surface-container/80 backdrop-blur-xl border-t border-white/5 z-50 flex justify-around items-center px-2 pb-safe">
        <a class="flex flex-col items-center justify-center w-16 h-full {% if active_page == 'dashboard' %}text-primary{% else %}text-on-surface-variant{% endif %}" href="{{ url_for('dashboard') }}">
            <div class="w-12 h-8 {% if active_page == 'dashboard' %}bg-primary-container{% endif %} rounded-full flex items-center justify-center mb-1">
                <span class="material-symbols-outlined" data-icon="dashboard">dashboard</span>
            </div>
            <span class="font-label-md text-[10px] tracking-tight">Inicio</span>
        </a>
        <a class="flex flex-col items-center justify-center w-16 h-full {% if active_page == 'alerts' %}text-primary{% else %}text-on-surface-variant{% endif %}" href="{{ url_for('alerts') }}">
            <div class="w-12 h-8 {% if active_page == 'alerts' %}bg-primary-container{% endif %} rounded-full flex items-center justify-center mb-1">
                <span class="material-symbols-outlined" data-icon="fact_check">fact_check</span>
            </div>
            <span class="font-label-md text-[10px] tracking-tight">Alertas</span>
        </a>
        <a class="flex flex-col items-center justify-center w-16 h-full {% if active_page == 'history' %}text-primary{% else %}text-on-surface-variant{% endif %}" href="{{ url_for('history') }}">
            <div class="w-12 h-8 {% if active_page == 'history' %}bg-primary-container{% endif %} rounded-full flex items-center justify-center mb-1">
                <span class="material-symbols-outlined" data-icon="history">history</span>
            </div>
            <span class="font-label-md text-[10px] tracking-tight">Historial</span>
        </a>
        <a class="flex flex-col items-center justify-center w-16 h-full {% if active_page == 'telemetry' %}text-primary{% else %}text-on-surface-variant{% endif %}" href="{{ url_for('telemetry') }}">
            <div class="w-12 h-8 {% if active_page == 'telemetry' %}bg-primary-container{% endif %} rounded-full flex items-center justify-center mb-1">
                <span class="material-symbols-outlined" data-icon="science">science</span>
            </div>
            <span class="font-label-md text-[10px] tracking-tight">Test</span>
        </a>
    </nav>

    {% block scripts %}{% endblock %}
</body>
</html>
""".replace("{head_content}", head_content).replace("{topnav_content}", topnav_content).replace("{aside_content}", aside_content)

    with open(os.path.join(TEMPLATES_DIR, 'base.html'), 'w', encoding='utf-8') as f:
        f.write(base_html)
    print("Creado templates/base.html exitosamente.")

# 1. login.html
login_src = os.path.join(SRC_DIR, 'login_del_auditor_esp', 'code.html')
if os.path.exists(login_src):
    with open(login_src, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Inyectar control de mensajes flash de Flask
    flash_html = """
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <div class="bg-error/20 border border-error/50 p-4 rounded-lg text-error text-body-sm mb-4">
                {{ messages[0] }}
            </div>
        {% endif %}
    {% endwith %}
    """
    html = re.sub(r'<form class="space-y-6" id="loginForm">', r'<form class="space-y-6" method="POST" action="{{ url_for(\'login\') }}" id="loginForm">', html)
    html = re.sub(r'</h3>\s*<p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Ingrese sus credenciales para acceder al sistema de supervisión de telemetría.</p>', r'</h3><p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Ingrese sus credenciales para acceder al sistema de supervisión de telemetría.</p>' + flash_html, html, flags=re.DOTALL)
    
    # Limpiar el javascript para permitir que el form se envíe al backend
    html = html.replace("e.preventDefault();", "")
    
    with open(os.path.join(TEMPLATES_DIR, 'login.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print("Creado templates/login.html.")

# 2. dashboard.html
dashboard_src = os.path.join(SRC_DIR, 'panel_del_auditor_final_esp', 'code.html')
if os.path.exists(dashboard_src):
    with open(dashboard_src, 'r', encoding='utf-8') as f:
        html = f.read()
    
    content = clean_main_content(html)
    
    # Remplazar KPIs con variables Jinja
    content = re.sub(r'<span class="font-display-lg text-display-lg text-error">\s*\d+\s*</span>', r'<span class="font-display-lg text-display-lg text-error">{{ active_alerts_count }}</span>', content)
    content = re.sub(r'<span class="font-display-lg text-display-lg text-on-surface">\s*1,240\s*</span>', r'<span class="font-display-lg text-display-lg text-on-surface">{{ total_alerts_count }}</span>', content)
    content = re.sub(r'<span class="font-display-lg text-display-lg text-on-surface">\s*42s\s*</span>', r'<span class="font-display-lg text-display-lg text-on-surface">{{ avg_decision_time_s }}s</span>', content)
    
    # Remplazar filas de la tabla de alertas
    tbody_pattern = r'<tbody class="font-mono-data text-mono-data">.*?</tbody>'
    alerts_loop = """
    <tbody class="font-mono-data text-mono-data">
        {% for alert in alerts %}
        <tr class="border-b border-white/5 hover:bg-white/[0.02] transition-colors group">
            <td class="py-3 px-4 text-on-surface">{{ alert.id_alerta }}</td>
            <td class="py-3 px-4">
                <span class="inline-flex items-center px-2 py-1 rounded bg-surface-variant text-on-surface-variant border border-white/10 font-body-sm text-body-sm">
                    <span class="w-2 h-2 rounded-full {% if alert.producto == 'Palta' %}bg-[#4A7C59]{% elif alert.producto == 'Uva' %}bg-[#8B5A8C]{% else %}bg-[#3B5998]{% endif %} mr-2"></span>{{ alert.producto }}
                </span>
            </td>
            <td class="py-3 px-4 text-on-surface-variant">{{ alert.razon_social }}</td>
            <td class="py-3 px-4">
                <div class="flex items-center gap-2">
                    <div class="w-16 h-1.5 bg-surface-container-highest rounded-full overflow-hidden">
                        <div class="h-full {% if alert.score_anomalia > 0.8 %}bg-error{% elif alert.score_anomalia > 0.6 %}bg-secondary{% else %}bg-primary-fixed-dim{% endif %}" style="width: {{ (alert.score_anomalia * 100) | int }}%"></div>
                    </div>
                    <span class="{% if alert.score_anomalia > 0.8 %}text-error{% elif alert.score_anomalia > 0.6 %}text-secondary{% else %}text-primary-fixed-dim{% endif %} font-bold">{{ alert.score_anomalia }}</span>
                </div>
            </td>
            <td class="py-3 px-4 text-right">
                <a href="{{ url_for('alert_detail', id_alerta=alert.id_alerta) }}" class="inline-block px-3 py-1 bg-transparent border border-error text-error rounded hover:bg-error/10 transition-colors font-label-md text-label-md uppercase opacity-80 group-hover:opacity-100">AUDITAR</a>
            </td>
        </tr>
        {% else %}
        <tr>
            <td colspan="5" class="py-6 text-center text-on-surface-variant">No hay alertas de prioridad pendientes.</td>
        </tr>
        {% endfor %}
    </tbody>
    """
    content = re.sub(tbody_pattern, alerts_loop, content, flags=re.DOTALL)
    
    # Remplazar feed de telemetría
    feed_pattern = r'<ul class="space-y-6 relative z-10">.*?</ul>'
    feed_loop = """
    <ul class="space-y-6 relative z-10">
        {% for log in feed_logs %}
        <li class="flex gap-4">
            <div class="w-4 h-4 rounded-full {% if 'anomalía' in log.evento or 'LOGIN_FAIL' in log.evento or 'UNAUTHORIZED' in log.evento %}bg-error shadow-[0_0_8px_rgba(255,180,171,0.6)] animate-pulse{% else %}bg-primary{% endif %} border-[3px] border-background shrink-0 mt-1 relative z-10"></div>
            <div>
                <div class="font-mono-data text-mono-data text-on-surface-variant text-[10px] mb-1">{{ log.fecha }} · Operador</div>
                <div class="font-body-sm text-body-sm text-on-surface font-medium">{{ log.evento }}</div>
            </div>
        </li>
        {% else %}
        <li class="py-4 text-center text-on-surface-variant font-body-sm">Sin telemetría activa en este ciclo.</li>
        {% endfor %}
    </ul>
    """
    content = re.sub(feed_pattern, feed_loop, content, flags=re.DOTALL)
    
    # Inyectar url_for en botones de navegación
    content = re.sub(r'href="#"', r'href="{{ url_for(\'alerts\') }}"', content)
    
    dashboard_html = """{% extends 'base.html' %}
{% block title %}Dashboard{% endblock %}
{% block content %}
    {content}
{% endblock %}
""".replace("{content}", content)

    with open(os.path.join(TEMPLATES_DIR, 'dashboard.html'), 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    print("Creado templates/dashboard.html.")

# 3. alerts.html (Bandeja de Gestión de Alertas)
alerts_src = os.path.join(SRC_DIR, 'bandeja_de_gesti_n_de_alertas', 'code.html')
if os.path.exists(alerts_src):
    with open(alerts_src, 'r', encoding='utf-8') as f:
        html = f.read()
        
    content = clean_main_content(html)
    
    # Cambiar cuerpo de tabla por bucle Jinja2
    tbody_pattern = r'<tbody class="font-mono-data text-mono-data">.*?</tbody>'
    alerts_loop = """
    <tbody class="font-mono-data text-mono-data">
        {% for alert in alerts %}
        <tr class="border-b border-white/5 hover:bg-white/[0.02] transition-colors group">
            <td class="py-3 px-4 text-on-surface">{{ alert.id_alerta }}</td>
            <td class="py-3 px-4">
                <span class="inline-flex items-center px-2 py-1 rounded bg-surface-variant text-on-surface-variant border border-white/10 font-body-sm text-body-sm">
                    <span class="w-2 h-2 rounded-full {% if alert.producto == 'Palta' %}bg-[#4A7C59]{% elif alert.producto == 'Uva' %}bg-[#8B5A8C]{% else %}bg-[#3B5998]{% endif %} mr-2"></span>{{ alert.producto }}
                </span>
            </td>
            <td class="py-3 px-4 text-on-surface-variant">{{ alert.razon_social }}</td>
            <td class="py-3 px-4">
                <div class="flex items-center gap-2">
                    <div class="w-16 h-1.5 bg-surface-container-highest rounded-full overflow-hidden">
                        <div class="h-full {% if alert.score_anomalia > 0.8 %}bg-error{% elif alert.score_anomalia > 0.6 %}bg-secondary{% else %}bg-primary-fixed-dim{% endif %}" style="width: {{ (alert.score_anomalia * 100) | int }}%"></div>
                    </div>
                    <span class="{% if alert.score_anomalia > 0.8 %}text-error{% elif alert.score_anomalia > 0.6 %}text-secondary{% else %}text-primary-fixed-dim{% endif %} font-bold">{{ alert.score_anomalia }}</span>
                </div>
            </td>
            <td class="py-3 px-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium 
                    {% if alert.estado == 'PENDIENTE' %}bg-error/10 text-error border border-error/20
                    {% elif alert.estado == 'EN_REVISION' %}bg-tertiary/10 text-tertiary border border-tertiary/20
                    {% else %}bg-primary/10 text-primary border border-primary/20{% endif %}">
                    {{ alert.estado }}
                </span>
            </td>
            <td class="py-3 px-4 text-right">
                <a href="{{ url_for('alert_detail', id_alerta=alert.id_alerta) }}" class="inline-block px-3 py-1 bg-transparent border border-error text-error rounded hover:bg-error/10 transition-colors font-label-md text-label-md uppercase opacity-80 group-hover:opacity-100">AUDITAR</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
    """
    content = re.sub(tbody_pattern, alerts_loop, content, flags=re.DOTALL)
    
    alerts_html = """{% extends 'base.html' %}
{% block title %}Cola de Alertas{% endblock %}
{% block content %}
    {content}
{% endblock %}
""".replace("{content}", content)

    with open(os.path.join(TEMPLATES_DIR, 'alerts.html'), 'w', encoding='utf-8') as f:
        f.write(alerts_html)
    print("Creado templates/alerts.html.")

# 4. detail.html (Detalle de Operación con Telemetría e IA Explicable)
detail_src = os.path.join(SRC_DIR, 'detalle_de_operaci_n_ia_explicable_esp', 'code.html')
if os.path.exists(detail_src):
    with open(detail_src, 'r', encoding='utf-8') as f:
        html = f.read()
        
    content = clean_main_content(html)
    
    # 4.1 Reemplazar variables fijas
    content = re.sub(r'DAM #012345', r'DAM #{{ alert.numero_dam }}', content)
    content = re.sub(r'RUC:</span>\s*<span[^>]*>\d+</span>', r'RUC:</span><span class="font-mono-data text-mono-data text-on-surface">{{ alert.ruc_exportador }}</span>', content)
    content = re.sub(r'Empresa:</span>\s*<span[^>]*>[^<]+</span>', r'Empresa:</span><span class="font-body-sm text-body-sm text-on-surface font-medium">{{ alert.razon_social }}</span>', content)
    content = re.sub(r'Producto:</span>\s*<span[^>]*>[^<]+</span>', r'Producto:</span><span class="font-body-sm text-body-sm text-on-surface font-medium">{{ alert.producto }}</span>', content)
    content = re.sub(r'Destino:</span>\s*<span[^>]*>[^<]+</span>', r'Destino:</span><span class="font-body-sm text-body-sm text-on-surface font-medium">Rotterdam</span>', content)
    
    # FOB Declarado vs Esperado
    content = re.sub(r'FOB Declarado</span>\s*<span[^>]*>\$[0-9,]+</span>', r'FOB Declarado</span><span class="text-on-surface font-mono-data">${{ "{:,.2f}".format(alert.valor_fob_declarado) }}</span>', content)
    content = re.sub(r'FOB Esperado \(Modelo\)</span>\s*<span[^>]*>\$[0-9,]+</span>', r'FOB Esperado (Modelo)</span><span class="text-primary font-mono-data">${{ "{:,.2f}".format(alert.valor_fob_esperado) }}</span>', content)
    
    # Desviación
    deviation_calc = """
    {% set dev = (((alert.valor_fob_esperado - alert.valor_fob_declarado) / alert.valor_fob_esperado) * 100) | round(1) %}
    """
    content = deviation_calc + content
    content = re.sub(r'Desviación</span>\s*<span[^>]*>[0-9.]+%</span>', r'Desviación</span><span class="font-display-lg text-[32px] text-error font-bold leading-none mt-1">{{ dev }}%</span>', content)
    
    # Score de anomalía unificado
    content = re.sub(r'Score de Confianza: [0-9.]+', r'Score de Anomalía: {{ alert.score_anomalia }}', content)
    
    # 4.2 Lógica Jinja2 para la Condición Experimental (Explicaciones locales SHAP y Reporte RAG)
    shap_rows = """
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-x-12 gap-y-4">
        {% for shap in shap_values %}
        <div class="flex items-center gap-4 group">
            <div class="w-1/3 text-right font-label-md text-label-md text-on-surface truncate group-hover:text-primary transition-colors">{{ shap.variable_nombre }}</div>
            <div class="w-2/3 flex items-center gap-2 {% if shap.shap_value < 0 %}flex-row-reverse justify-end{% endif %}">
                <div class="h-4 {% if shap.shap_value > 0 %}bg-error/80 rounded-r-sm{% else %}bg-tertiary/80 rounded-l-sm{% endif %}" style="width: {{ (shap.shap_value | abs * 200) | int }}%;"></div>
                <span class="font-mono-data text-[12px] {% if shap.shap_value > 0 %}text-error{% else %}text-tertiary{% endif %}">
                    {% if shap.shap_value > 0 %}+{% endif %}{{ shap.shap_value }} ({{ shap.variable_valor }})
                </span>
            </div>
        </div>
        {% endfor %}
    </div>
    """
    content = re.sub(r'<div class="grid grid-cols-1 lg:grid-cols-2 gap-x-12 gap-y-4">.*?</div>\s*</div>\s*</div>\s*<!-- Capa 4: Reporte RAG', shap_rows + "</div></div><!-- Capa 4: Reporte RAG", content, flags=re.DOTALL)
    
    # RAG Report Narrative
    content = re.sub(
        r'<div class="flex-1 glass-panel bg-surface-container-low/50 rounded-lg p-5 border border-white/5 font-body-md text-body-md text-on-surface-variant leading-relaxed overflow-y-auto">.*?</div>',
        r"""<div class="flex-1 glass-panel bg-surface-container-low/50 rounded-lg p-5 border border-white/5 font-body-md text-body-md text-on-surface-variant leading-relaxed overflow-y-auto">
            <p class="mb-4">
                El modelo ensemble ha marcado esta exportación aduanera debido a una desviación negativa del <span class="text-on-surface font-medium">{{ dev }}%</span> del valor FOB declarado frente al estimado de <strong>${{ "{:,.2f}".format(alert.valor_fob_esperado) }}</strong> para el producto <span class="text-on-surface font-medium">{{ alert.producto }}</span>.
            </p>
            <p class="mb-4">
                Las causas principales residen en el desvío de precio residual. Adicionalmente, se registran proxies climáticos y retrasos logísticos en el nodo portuario de origen.
            </p>
            <p>
                Según el protocolo institucional, las operaciones sospechosas con un score del ensemble superior a <strong>0.75</strong> ameritan una inspección complementaria de las credenciales fitosanitarias de SENASA y verificación del contrato comercial.
            </p>
        </div>""",
        content,
        flags=re.DOTALL
    )
    
    # Envolver la Capa 3 y la Capa 4 en la condición Jinja 'INTEGRADO'
    content = content.replace('<!-- Capa 3: Explicabilidad SHAP (Ancho Completo) -->', '{% if condicion == "INTEGRADO" %}<!-- Capa 3: Explicabilidad SHAP (Ancho Completo) -->')
    content = content.replace('<!-- Panel de Decisión (Col 8-12) -->', '{% else %}<div class="xl:col-span-12 glass-panel rounded-xl p-8 text-center text-on-surface-variant py-12"><span class="material-symbols-outlined text-[48px] mb-2">visibility_off</span><p class="font-body-md">Detalle explicativo local (SHAP) y reporte narrativo de IA (RAG) restringidos según el protocolo de usabilidad en Condición B (Aislada).</p></div>{% endif %}<!-- Panel de Decisión (Col 8-12) -->')
    
    # 4.3 Formulario de Adjudicación
    content = re.sub(
        r'<form class="space-y-6">',
        r'<form class="space-y-6" id="adjudicationForm" method="POST" action="{{ url_for(\'adjudicate\', id_alerta=alert.id_alerta) }}"><input type="hidden" id="time_to_decision_ms" name="time_to_decision_ms" value="0">',
        content
    )
    
    # Calificación Likert (5 estrellas) con eventos para guardado interactivo
    stars_html = """
    <div class="flex items-center gap-2">
        <input type="hidden" id="likert_comprehension" name="likert_comprehension" value="5">
        {% for i in range(1, 6) %}
        <button class="text-primary star-btn hover:scale-110 transition-transform" type="button" data-value="{{ i }}">
            <span class="material-symbols-outlined text-[28px]" id="star-icon-{{ i }}">star</span>
        </button>
        {% endfor %}
    </div>
    """
    # Reemplazar barra de estrellas
    content = re.sub(
        r'<label class="font-label-md text-label-md text-on-surface-variant block">Calificación de Comprensión de la IA</label>.*?</div>\s*</div>',
        r'<label class="font-label-md text-label-md text-on-surface-variant block">Calificación de Comprensión de la IA</label>' + stars_html + "</div>",
        content,
        flags=re.DOTALL
    )
    
    # JavaScript para la Telemetría de Usabilidad y las Estrellas
    scripts = """
<script>
    // Registro de Telemetría (Tiempo en milisegundos)
    const startTime = performance.now();
    const adjForm = document.getElementById('adjudicationForm');
    const timeInput = document.getElementById('time_to_decision_ms');
    
    adjForm.addEventListener('submit', () => {
        const endTime = performance.now();
        const elapsed = Math.round(endTime - startTime);
        timeInput.value = elapsed;
        console.log("Tiempo de decisión guardado (ms): " + elapsed);
    });

    // Control Interactivo de la Escala Likert de 5 Estrellas
    const stars = document.querySelectorAll('.star-btn');
    const likertInput = document.getElementById('likert_comprehension');
    
    stars.forEach(star => {
        star.addEventListener('click', () => {
            const val = parseInt(star.getAttribute('data-value'));
            likertInput.value = val;
            
            // Pintar estrellas
            for(let i = 1; i <= 5; i++) {
                const starIcon = document.getElementById('star-icon-' + i);
                if (i <= val) {
                    starIcon.classList.remove('text-on-surface-variant');
                    starIcon.classList.add('text-primary');
                    starIcon.style.fontVariationSettings = "'FILL' 1";
                } else {
                    starIcon.classList.remove('text-primary');
                    starIcon.classList.add('text-on-surface-variant');
                    starIcon.style.fontVariationSettings = "'FILL' 0";
                }
            }
        });
    });
</script>
"""
    
    detail_html = """{% extends 'base.html' %}
{% block title %}Detalle Operación #{{ alert.id_alerta }}{% endblock %}
{% block content %}
    {content}
{% endblock %}
{% block scripts %}
    {scripts}
{% endblock %}
""".replace("{content}", content).replace("{scripts}", scripts)

    with open(os.path.join(TEMPLATES_DIR, 'detail.html'), 'w', encoding='utf-8') as f:
        f.write(detail_html)
    print("Creado templates/detail.html.")

# 5. history.html (Historial de Auditoría)
history_src = os.path.join(SRC_DIR, 'my_audit_history', 'code.html')
if os.path.exists(history_src):
    with open(history_src, 'r', encoding='utf-8') as f:
        html = f.read()
        
    content = clean_main_content(html)
    
    # Cuerpo de tabla dinámico
    tbody_pattern = r'<tbody class="font-mono-data text-mono-data">.*?</tbody>'
    history_loop = """
    <tbody class="font-mono-data text-mono-data">
        {% for dec in decisions %}
        <tr class="border-b border-white/5 hover:bg-white/[0.02] transition-colors group">
            <td class="py-4 px-4 text-on-surface">{{ dec.id_decision }}</td>
            <td class="py-4 px-4 text-on-surface-variant">{{ dec.id_alerta }}</td>
            <td class="py-4 px-4">
                <span class="inline-flex items-center px-2 py-1 rounded bg-surface-variant text-on-surface-variant border border-white/10 font-body-sm text-body-sm">
                    {{ dec.producto }}
                </span>
            </td>
            <td class="py-4 px-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium 
                    {% if dec.user_decision == 1 %}bg-error/10 text-error border border-error/20
                    {% elif dec.user_decision == 2 %}bg-tertiary/10 text-tertiary border border-tertiary/20
                    {% else %}bg-primary/10 text-primary border border-primary/20{% endif %}">
                    {% if dec.user_decision == 1 %}Anomalía Confirmada
                    {% elif dec.user_decision == 2 %}Refiere Inspección
                    {% else %}Falsa Alarma{% endif %}
                </span>
            </td>
            <td class="py-4 px-4 text-center font-bold text-on-surface">{{ dec.score_anomalia }}</td>
            <td class="py-4 px-4 text-right text-secondary font-mono-data">{{ "{:,}".format(dec.time_to_decision_ms) }} ms</td>
            <td class="py-4 px-4 text-on-surface-variant">{{ dec.creado_en }}</td>
            <td class="py-4 px-4 text-right">
                <a href="{{ url_for('alert_detail', id_alerta=dec.id_alerta) }}" class="px-3 py-1 bg-transparent border border-primary text-primary rounded hover:bg-primary/10 transition-colors font-label-md text-label-md uppercase opacity-80 group-hover:opacity-100">Ver Detalle</a>
            </td>
        </tr>
        {% else %}
        <tr>
            <td colspan="8" class="py-8 text-center text-on-surface-variant">Usted no ha realizado ninguna adjudicación en este ciclo.</td>
        </tr>
        {% endfor %}
    </tbody>
    """
    content = re.sub(tbody_pattern, history_loop, content, flags=re.DOTALL)
    
    # Hacer dinámica la tarjeta de resumen superior
    content = re.sub(r'<span class="font-display-lg text-display-lg text-primary">\s*\d+\s*</span>', r'<span class="font-display-lg text-display-lg text-primary">{{ decisions | length }}</span>', content)
    
    history_html = """{% extends 'base.html' %}
{% block title %}Historial de Auditoría{% endblock %}
{% block content %}
    {content}
{% endblock %}
""".replace("{content}", content)

    with open(os.path.join(TEMPLATES_DIR, 'history.html'), 'w', encoding='utf-8') as f:
        f.write(history_html)
    print("Creado templates/history.html.")

# 6. config.html (Configuración del Modelo)
config_src = os.path.join(SRC_DIR, 'terminal_de_configuraci_n_del_modelo_esp', 'code.html')
if os.path.exists(config_src):
    with open(config_src, 'r', encoding='utf-8') as f:
        html = f.read()
        
    content = clean_main_content(html)
    
    # Envolver en form
    content = re.sub(r'<div class="xl:col-span-8 glass-panel rounded-xl p-6 relative overflow-hidden group">', r'<form method="POST" action="{{ url_for(\'config\') }}" class="xl:col-span-12 grid grid-cols-1 xl:grid-cols-12 gap-card-gap">', content)
    content = re.sub(
        r'<button class="px-6 py-2 bg-primary text-on-primary font-label-md text-label-md uppercase rounded-lg hover:shadow-\[0_0_15px_rgba\(118,219,143,0.4\)\] transition-all">Aplicar Cambios</button>',
        r'<button type="submit" class="px-6 py-2 bg-primary text-on-primary font-label-md text-label-md uppercase rounded-lg hover:shadow-[0_0_15px_rgba(118,219,143,0.4)] transition-all">Aplicar Cambios</button>',
        content
    )
    content += "\n</form>"
    
    config_html = """{% extends 'base.html' %}
{% block title %}Configuración del Pipeline{% endblock %}
{% block content %}
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <div class="mb-6 p-4 rounded-lg bg-primary/20 border border-primary/50 text-primary font-body-md">
                {{ messages[0] }}
            </div>
        {% endif %}
    {% endwith %}
    {content}
{% endblock %}
""".replace("{content}", content)

    with open(os.path.join(TEMPLATES_DIR, 'config.html'), 'w', encoding='utf-8') as f:
        f.write(config_html)
    print("Creado templates/config.html.")

# 7. integrity.html (Monitor de Equidad y Fairness)
integrity_src = os.path.join(SRC_DIR, 'monitor_de_telemetr_a_y_equidad_esp', 'code.html')
if os.path.exists(integrity_src):
    with open(integrity_src, 'r', encoding='utf-8') as f:
        html = f.read()
        
    content = clean_main_content(html)
    
    integrity_html = """{% extends 'base.html' %}
{% block title %}Integridad y Fairness{% endblock %}
{% block content %}
    {content}
{% endblock %}
""".replace("{content}", content)

    with open(os.path.join(TEMPLATES_DIR, 'integrity.html'), 'w', encoding='utf-8') as f:
        f.write(integrity_html)
    print("Creado templates/integrity.html.")

# 8. users.html (Usuarios y Seguridad)
users_src = os.path.join(SRC_DIR, 'control_de_usuarios_y_log_de_seguridad_esp', 'code.html')
if os.path.exists(users_src):
    with open(users_src, 'r', encoding='utf-8') as f:
        html = f.read()
        
    content = clean_main_content(html)
    
    # Inyectar logs reales
    tbody_pattern = r'<tbody class="font-mono-data text-mono-data">.*?</tbody>'
    logs_loop = """
    <tbody class="font-mono-data text-mono-data">
        {% for log in security_logs %}
        <tr class="border-b border-white/5 hover:bg-white/[0.01] transition-colors">
            <td class="py-4 px-4 text-on-surface">{{ log.id_log }}</td>
            <td class="py-4 px-4 text-on-surface-variant font-medium">{{ log.usuario }}</td>
            <td class="py-4 px-4">
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold
                    {% if 'FAIL' in log.evento or 'UNAUTHORIZED' in log.evento %}bg-error/10 text-error border border-error/20
                    {% else %}bg-primary/10 text-primary border border-primary/20{% endif %}">
                    {{ log.evento }}
                </span>
            </td>
            <td class="py-4 px-4 text-on-surface-variant">{{ log.ip_address }}</td>
            <td class="py-4 px-4 text-on-surface-variant text-right">{{ log.fecha }}</td>
        </tr>
        {% endfor %}
    </tbody>
    """
    content = re.sub(tbody_pattern, logs_loop, content, flags=re.DOTALL)
    
    # Inyectar usuarios reales
    users_loop = """
    <tbody class="font-mono-data text-mono-data">
        {% for user in all_users %}
        <tr class="border-b border-white/5 hover:bg-white/[0.01] transition-colors">
            <td class="py-4 px-6 text-on-surface">{{ user.id_usuario }}</td>
            <td class="py-4 px-6 font-medium text-on-surface">{{ user.nombre }}</td>
            <td class="py-4 px-6 text-on-surface-variant">{{ user.username }}</td>
            <td class="py-4 px-6">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary border border-primary/20">
                    {{ user.rol }}
                </span>
            </td>
            <td class="py-4 px-6 text-right">
                <span class="material-symbols-outlined text-primary text-sm">check_circle</span>
            </td>
        </tr>
        {% endfor %}
    </tbody>
    """
    content = re.sub(r'<tbody class="font-mono-data text-mono-data">.*?</tbody>', users_loop, content, count=1, flags=re.DOTALL)
    
    users_html = """{% extends 'base.html' %}
{% block title %}Control de Usuarios y Seguridad{% endblock %}
{% block content %}
    {content}
{% endblock %}
""".replace("{content}", content)

    with open(os.path.join(TEMPLATES_DIR, 'users.html'), 'w', encoding='utf-8') as f:
        f.write(users_html)
    print("Creado templates/users.html.")

# 9. telemetry.html (Consola de Telemetría del Experimento - Investigador)
telemetry_src = os.path.join(SRC_DIR, 'experimental_telemetry_console', 'code.html')
if os.path.exists(telemetry_src):
    with open(telemetry_src, 'r', encoding='utf-8') as f:
        html = f.read()
        
    content = clean_main_content(html)
    
    # Hacer dinámico el progreso de los testers
    tbody_pattern = r'<tbody class="font-mono-data text-mono-data">.*?</tbody>'
    progress_loop = """
    <tbody class="font-mono-data text-mono-data">
        {% for dec in recent_decisions %}
        <tr class="table-row-hover transition-colors">
            <td class="py-4 px-6 text-on-surface">USR-{{ dec.id_usuario }}-T</td>
            <td class="py-4 px-6">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium 
                    {% if dec.condicion_experimento == 'INTEGRADO' %}bg-primary/10 text-primary border border-primary/20
                    {% else %}bg-tertiary/10 text-tertiary border border-tertiary/20{% endif %}">
                    {{ dec.condicion_experimento }}
                </span>
            </td>
            <td class="py-4 px-6 text-on-surface-variant">{{ dec.id_alerta }}</td>
            <td class="py-4 px-6 text-secondary font-mono-data">{{ "{:,}".format(dec.time_to_decision_ms) }} ms</td>
            <td class="py-4 px-6 text-right">
                <span class="material-symbols-outlined text-primary text-sm">check_circle</span>
            </td>
        </tr>
        {% else %}
        <tr>
            <td colspan="5" class="py-6 text-center text-on-surface-variant">No hay telemetría de tests registrada aún en este ciclo.</td>
        </tr>
        {% endfor %}
    </tbody>
    """
    content = re.sub(tbody_pattern, progress_loop, content, flags=re.DOTALL)
    
    # Reemplazar KPIs
    content = re.sub(r'<span class="font-display-lg text-display-lg text-primary">\s*42s\s*</span>', r'<span class="font-display-lg text-display-lg text-primary">{{ avg_time_integrated_s }}s</span>', content)
    content = re.sub(r'<span class="font-display-lg text-display-lg text-tertiary">\s*78s\s*</span>', r'<span class="font-display-lg text-display-lg text-tertiary">{{ avg_time_isolated_s }}s</span>', content)
    content = re.sub(r'<span class="font-display-lg text-display-lg text-on-surface">\s*4\.5\s*</span>', r'<span class="font-display-lg text-display-lg text-on-surface">{{ avg_comp_integrated }}</span>', content)
    content = re.sub(r'<span class="font-display-lg text-display-lg text-on-surface">\s*2\.3\s*</span>', r'<span class="font-display-lg text-display-lg text-on-surface">{{ avg_comp_isolated }}</span>', content)
    
    telemetry_html = """{% extends 'base.html' %}
{% block title %}Consola de Telemetría Experimental{% endblock %}
{% block content %}
    {content}
{% endblock %}
""".replace("{content}", content)

    with open(os.path.join(TEMPLATES_DIR, 'telemetry.html'), 'w', encoding='utf-8') as f:
        f.write(telemetry_html)
    print("Creado templates/telemetry.html.")

# 10. data.html (Explorador de Datos y Centro de Carga)
data_src = os.path.join(SRC_DIR, 'explorador_de_datos_y_centro_de_carga', 'code.html')
if os.path.exists(data_src):
    with open(data_src, 'r', encoding='utf-8') as f:
        html = f.read()
        
    content = clean_main_content(html)
    
    # Hacer el formulario funcional
    content = re.sub(
        r'<form class="space-y-6">',
        r'<form class="space-y-6" method="POST" action="{{ url_for(\'data_explorer\') }}" enctype="multipart/form-data">',
        content
    )
    
    # Cuerpo de tabla de importaciones dinámico
    tbody_pattern = r'<tbody class="font-mono-data text-mono-data">.*?</tbody>'
    data_loop = """
    <tbody class="font-mono-data text-mono-data">
        {% for alert in alerts %}
        <tr class="border-b border-white/5 hover:bg-white/[0.01] transition-colors">
            <td class="py-4 px-6 text-on-surface">{{ alert.id_alerta }}</td>
            <td class="py-4 px-6 text-on-surface-variant font-medium">{{ alert.ruc_exportador }}</td>
            <td class="py-4 px-6 text-on-surface-variant">{{ alert.producto }}</td>
            <td class="py-4 px-6 text-right font-mono-data">${{ "{:,.2f}".format(alert.valor_fob_declarado) }}</td>
            <td class="py-4 px-6 text-right font-mono-data {% if alert.score_anomalia > 0.75 %}text-error{% else %}text-primary{% endif %}">{{ alert.score_anomalia }}</td>
        </tr>
        {% endfor %}
    </tbody>
    """
    content = re.sub(tbody_pattern, data_loop, content, flags=re.DOTALL)
    
    data_html = """{% extends 'base.html' %}
{% block title %}Explorador de Datos{% endblock %}
{% block content %}
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <div class="mb-6 p-4 rounded-lg bg-primary/20 border border-primary/50 text-primary font-body-md">
                {{ messages[0] }}
            </div>
        {% endif %}
    {% endwith %}
    {content}
{% endblock %}
""".replace("{content}", content)

    with open(os.path.join(TEMPLATES_DIR, 'data.html'), 'w', encoding='utf-8') as f:
        f.write(data_html)
    print("Creado templates/data.html.")

print("Todas las vistas han sido integradas dinámicamente en templates/.")
