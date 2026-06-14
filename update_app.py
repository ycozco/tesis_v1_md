import re
from pathlib import Path

app_path = Path('d:/tesis_yoset/src/app.py')
content = app_path.read_text(encoding='utf-8')

# 1. Update Navigation Menus in TEMPLATES
# Template 1: SECCIONES_TEMPLATE
nav_secciones_old = """    <div class="nav-menu">
      <a href="/" class="nav-item">🏠 Inicio</a>
      <a href="/secciones" class="nav-item active">📖 Secciones</a>
      <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
      <a href="/admin" class="nav-item">⚙️ Administración</a>
    </div>"""

nav_secciones_new = """    <div class="nav-menu">
      <a href="/" class="nav-item">🏠 Inicio</a>
      <a href="/secciones" class="nav-item active">📖 Secciones</a>
      <a href="/datos" class="nav-item">🗃️ Datos</a>
      <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
      <a href="/admin" class="nav-item">⚙️ Administración</a>
    </div>"""

# Template 2: generate_section_page
nav_section_page_old = """      <div class="nav-menu">
        <a href="/" class="nav-item">🏠 Inicio</a>
        <a href="/secciones" class="nav-item active">📖 Secciones</a>
        <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
        <a href="/admin" class="nav-item">⚙️ Administración</a>
      </div>"""

nav_section_page_new = """      <div class="nav-menu">
        <a href="/" class="nav-item">🏠 Inicio</a>
        <a href="/secciones" class="nav-item active">📖 Secciones</a>
        <a href="/datos" class="nav-item">🗃️ Datos</a>
        <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
        <a href="/admin" class="nav-item">⚙️ Administración</a>
      </div>"""

# Template 3: index
nav_index_old = """            <div class="nav-menu">
                <a href="/" class="nav-item active">🏠 Inicio</a>
                <a href="/secciones" class="nav-item">📖 Secciones</a>
                <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
                <a href="/admin" class="nav-item">⚙️ Administración</a>
            </div>"""

nav_index_new = """            <div class="nav-menu">
                <a href="/" class="nav-item active">🏠 Inicio</a>
                <a href="/secciones" class="nav-item">📖 Secciones</a>
                <a href="/datos" class="nav-item">🗃️ Datos</a>
                <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
                <a href="/admin" class="nav-item">⚙️ Administración</a>
            </div>"""

# Template 4: PROPUESTA_TEMPLATE
nav_propuesta_old = """            <div class="nav-menu">
                <a href="/" class="nav-item">🏠 Inicio</a>
                <a href="/secciones" class="nav-item">📖 Secciones</a>
                <a href="/propuesta" class="nav-item active">📊 Propuesta y Prototipo</a>
                <a href="/admin" class="nav-item">⚙️ Administración</a>
            </div>"""

nav_propuesta_new = """            <div class="nav-menu">
                <a href="/" class="nav-item">🏠 Inicio</a>
                <a href="/secciones" class="nav-item">📖 Secciones</a>
                <a href="/datos" class="nav-item">🗃️ Datos</a>
                <a href="/propuesta" class="nav-item active">📊 Propuesta y Prototipo</a>
                <a href="/admin" class="nav-item">⚙️ Administración</a>
            </div>"""

# Template 5: admin_dashboard
nav_admin_old = """                <div class="nav-menu">
                    <a href="/" class="nav-item">🏠 Inicio</a>
                    <a href="/secciones" class="nav-item">📖 Secciones</a>
                    <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
                    <a href="/admin" class="nav-item active">⚙️ Administración</a>
                </div>"""

nav_admin_new = """                <div class="nav-menu">
                    <a href="/" class="nav-item">🏠 Inicio</a>
                    <a href="/secciones" class="nav-item">📖 Secciones</a>
                    <a href="/datos" class="nav-item">🗃️ Datos</a>
                    <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
                    <a href="/admin" class="nav-item active">⚙️ Administración</a>
                </div>"""

content = content.replace(nav_secciones_old, nav_secciones_new)
content = content.replace(nav_section_page_old, nav_section_page_new)
content = content.replace(nav_index_old, nav_index_new)
content = content.replace(nav_propuesta_old, nav_propuesta_new)
content = content.replace(nav_admin_old, nav_admin_new)

# 2. Add DATOS_TEMPLATE, /datos route, and /api/data/<key> route
datos_code = """
# =============================================================================
# EXPLORADOR DE DATOS INTERACTIVO
# =============================================================================

DATOS_TEMPLATE = \"\"\"<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Explorador de Datasets | Tesis Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #0f172a;
            --card: #1e293b;
            --primary: #6366f1;
            --accent: #10b981;
            --warn: #f59e0b;
            --error: #ef4444;
            --text: #f8fafc;
            --muted: #94a3b8;
            --border: rgba(255, 255, 255, 0.08);
            --glass: rgba(30, 41, 59, 0.7);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.08) 0px, transparent 50%);
            color: var(--text);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        
        /* Navigation Bar Styles */
        .main-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 12px 24px;
            margin-bottom: 30px;
        }
        .nav-logo {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 700;
            font-size: 1.15rem;
            color: #fff;
        }
        .logo-dot {
            width: 8px;
            height: 8px;
            background: var(--accent);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent);
            animation: pulse-dot 2s infinite;
        }
        @keyframes pulse-dot {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }
        .nav-menu {
            display: flex;
            gap: 8px;
        }
        .nav-item {
            color: var(--muted);
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .nav-item:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.04);
        }
        .nav-item.active {
            color: #fff;
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.25);
        }

        header { margin-bottom: 30px; }
        h1 { font-size: 2.2rem; margin-bottom: 6px; background: linear-gradient(to right, #818cf8, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .sub { color: var(--muted); font-size: 1rem; }

        .explorer-layout {
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 24px;
        }
        .card {
            background: var(--glass);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 24px;
        }
        .card h2 { font-size: 1.25rem; color: #c7d2fe; margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }

        /* Dataset list styling */
        .dataset-list { display: flex; flex-direction: column; gap: 8px; }
        .dataset-btn {
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border);
            color: var(--muted);
            padding: 12px 16px;
            border-radius: 12px;
            cursor: pointer;
            text-align: left;
            font-family: inherit;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.2s;
        }
        .dataset-btn:hover { color: #fff; border-color: var(--primary); background: rgba(99, 102, 241, 0.05); }
        .dataset-btn.active { color: #fff; border-color: var(--primary); background: var(--primary); box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3); }

        /* Table & Controls */
        .controls-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; gap: 16px; }
        .search-input {
            background: rgba(0,0,0,0.2);
            border: 1px solid var(--border);
            padding: 10px 16px;
            border-radius: 10px;
            color: #fff;
            font-family: inherit;
            font-size: 0.9rem;
            width: 250px;
            outline: none;
        }
        .search-input:focus { border-color: var(--primary); }
        .limit-select {
            background: #1e293b;
            border: 1px solid var(--border);
            padding: 8px 12px;
            border-radius: 8px;
            color: #fff;
            font-family: inherit;
            font-size: 0.85rem;
            outline: none;
        }

        .table-wrap { overflow-x: auto; max-height: 500px; border: 1px solid var(--border); border-radius: 12px; background: rgba(0,0,0,0.15); }
        table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
        th { background: #1e293b; padding: 12px 14px; font-weight: 600; border-bottom: 2px solid var(--border); color: #cbd5e1; cursor: pointer; user-select: none; }
        th:hover { color: #fff; background: rgba(99, 102, 241, 0.2); }
        td { padding: 10px 14px; border-bottom: 1px solid var(--border); color: #e2e8f0; }
        tr:hover td { background: rgba(255,255,255,0.03); }

        .pagination { display: flex; justify-content: space-between; align-items: center; margin-top: 16px; }
        .page-btn {
            background: rgba(255,255,255,0.05);
            border: 1px solid var(--border);
            color: #fff;
            padding: 6px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-family: inherit;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .page-btn:hover { background: rgba(99, 102, 241, 0.15); }
        .page-btn:disabled { opacity: 0.3; cursor: not-allowed; }

        .metadata-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
        .meta-card { background: rgba(255,255,255,0.02); padding: 12px; border-radius: 8px; text-align: center; border: 1px solid var(--border); }
        .meta-val { font-size: 1.3rem; font-weight: 700; color: var(--primary); font-family: 'JetBrains Mono', monospace; }
        .meta-lbl { font-size: 0.75rem; color: var(--muted); text-transform: uppercase; }

        .chart-container { width: 100%; height: 260px; display: flex; justify-content: center; align-items: center; position: relative; }
        
        .loading-overlay { text-align: center; padding: 60px; color: var(--muted); }
        .spinner { width: 40px; height: 40px; border: 4px solid rgba(255,255,255,0.1); border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 16px; }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
<div class="container">
    <!-- Main Navbar -->
    <nav class="main-navbar">
        <div class="nav-logo">
            <span class="logo-dot"></span>
            <span class="logo-text">Tesis Hub</span>
        </div>
        <div class="nav-menu">
            <a href="/" class="nav-item">🏠 Inicio</a>
            <a href="/secciones" class="nav-item">📖 Secciones</a>
            <a href="/datos" class="nav-item active">🗃️ Datos</a>
            <a href="/propuesta" class="nav-item">📊 Propuesta y Prototipo</a>
            <a href="/admin" class="nav-item">⚙️ Administración</a>
        </div>
    </nav>

    <header>
        <h1>Explorador de Datasets de Tesis</h1>
        <p class="sub">Visualice, ordene, filtre y analice las estadísticas de las fuentes reales e hipotéticas del sistema.</p>
    </header>

    <div class="explorer-layout">
        <!-- Sidebar -->
        <aside>
            <div class="card">
                <h2>Fuentes de Datos</h2>
                <div class="dataset-list">
                    <button class="dataset-btn active" onclick="loadDataset('synthetic_agro', this)">🤖 Dataset Sintético v1.0</button>
                    <button class="dataset-btn" onclick="loadDataset('bcrp_exchange', this)">💵 Tipo de Cambio (BCRP)</button>
                    <button class="dataset-btn" onclick="loadDataset('faostat_prod', this)">🌾 Producción Agro (FAOSTAT)</button>
                    <button class="dataset-btn" onclick="loadDataset('sunat_export', this)">🚢 Exportaciones (SUNAT)</button>
                    <button class="dataset-btn" onclick="loadDataset('validated_refs', this)">📋 Datasets Validados (CSV)</button>
                </div>
            </div>
            
            <div class="card">
                <h2>Resumen Técnico</h2>
                <div id="metadata-container">
                    <!-- Loaded dynamically -->
                    <p style="color:var(--muted); font-size:0.9rem; text-align:center;">Cargando metadatos...</p>
                </div>
            </div>
        </aside>

        <!-- Main Panel -->
        <main>
            <div class="card" id="chart-card">
                <h2>Análisis Gráfico</h2>
                <div class="chart-container">
                    <canvas id="dataset-chart"></canvas>
                </div>
            </div>

            <div class="card">
                <h2>Registros de Datos</h2>
                <div class="controls-row">
                    <div>
                        <span style="font-size:0.85rem; color:var(--muted)">Mostrar</span>
                        <select class="limit-select" id="page-size-select" onchange="changePageSize(this.value)">
                            <option value="10">10 filas</option>
                            <option value="25">25 filas</option>
                            <option value="50">50 filas</option>
                        </select>
                    </div>
                    <input type="text" class="search-input" id="search-box" placeholder="Buscar registros..." onkeyup="filterRows(this.value)">
                </div>

                <div id="table-loading-container" class="loading-overlay">
                    <div class="spinner"></div>
                    <p>Cargando datos del archivo CSV...</p>
                </div>

                <div id="table-display-container" style="display:none;">
                    <div class="table-wrap">
                        <table id="data-table">
                            <thead id="table-head"></thead>
                            <tbody id="table-body"></tbody>
                        </table>
                    </div>

                    <div class="pagination">
                        <span style="font-size:0.85rem; color:var(--muted)" id="page-indicator">Mostrando 1-10 de 100</span>
                        <div>
                            <button class="page-btn" id="prev-btn" onclick="prevPage()">Anterior</button>
                            <button class="page-btn" id="next-btn" onclick="nextPage()" style="margin-left:8px;">Siguiente</button>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</div>

<script>
    let currentData = { columns: [], rows: [] };
    let filteredRows = [];
    let currentPage = 1;
    let pageSize = 10;
    let activeDataset = 'synthetic_agro';
    let chartInstance = null;

    async function loadDataset(key, btn) {
        if (btn) {
            document.querySelectorAll('.dataset-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }
        activeDataset = key;
        
        // Reset view
        document.getElementById('table-loading-container').style.display = 'block';
        document.getElementById('table-display-container').style.display = 'none';
        document.getElementById('search-box').value = '';
        
        try {
            const res = await fetch(`/api/data/${key}`);
            const payload = await res.json();
            if (payload.error) {
                alert(payload.error);
                return;
            }
            currentData = payload;
            filteredRows = [...currentData.rows];
            currentPage = 1;
            
            renderMetadata(payload.stats);
            renderChart(key, payload);
            renderTable();
        } catch (e) {
            alert("Error cargando el dataset: " + e.message);
        }
    }

    function renderMetadata(stats) {
        const container = document.getElementById('metadata-container');
        container.innerHTML = `
            <div class="metadata-grid">
                <div class="meta-card">
                    <div class="meta-val">${stats.num_rows.toLocaleString()}</div>
                    <div class="meta-lbl">Registros</div>
                </div>
                <div class="meta-card">
                    <div class="meta-val">${stats.num_cols}</div>
                    <div class="meta-lbl">Columnas</div>
                </div>
            </div>
            <p style="font-size:0.85rem; margin-bottom:4px; color:var(--muted);">Archivo: <span style="color:#fff; font-family:monospace;">${stats.filename}</span></p>
        `;
    }

    function renderChart(key, data) {
        const ctx = document.getElementById('dataset-chart').getContext('2d');
        if (chartInstance) {
            chartInstance.destroy();
        }
        
        const chartCard = document.getElementById('chart-card');
        chartCard.style.display = 'block';

        let chartConfig = {};

        if (key === 'synthetic_agro') {
            // Pie chart of anomaly types
            const anomalies = data.rows.filter(r => r.etiqueta_anomalia === '1' || r.etiqueta_anomalia === 1);
            const counts = {};
            anomalies.forEach(r => {
                const t = r.tipo_anomalia || 'Desconocido';
                counts[t] = (counts[t] || 0) + 1;
            });
            chartConfig = {
                type: 'pie',
                data: {
                    labels: Object.keys(counts),
                    datasets: [{
                        data: Object.values(counts),
                        backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6'],
                        borderWidth: 1,
                        borderColor: '#1e293b'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right', labels: { color: '#f8fafc', font: { family: 'Outfit' } } }
                    }
                }
            };
        } 
        else if (key === 'bcrp_exchange') {
            // Line chart of exchange rate over time
            // Columns: "", "PN01205PM", "PN01206PM", "PN01207PM", etc.
            // Row has: Col_0 (mes like "May24"), "PN01207PM" (Promedio rate)
            const labels = [];
            const values = [];
            
            // BCRP columns: Col_0 is month, Col_3 (PN01207PM) is interbank average
            data.rows.forEach(r => {
                const month = r.Col_0 || r[''] || 'N/A';
                const rate = parseFloat(r['PN01207PM'] || r['Col_3']);
                if (month !== 'N/A' && !isNaN(rate)) {
                    labels.push(month);
                    values.push(rate);
                }
            });
            
            chartConfig = {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Tipo de cambio promedio interbancario (S/ por USD)',
                        data: values,
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        fill: true,
                        tension: 0.3,
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: {
                        legend: { labels: { color: '#f8fafc' } }
                    }
                }
            };
        } 
        else if (key === 'faostat_prod') {
            // Bar chart of area harvested for top 8 crops
            const crops = {};
            data.rows.forEach(r => {
                const cropName = r.Item || 'N/A';
                const area = parseFloat(r.Value);
                if (cropName !== 'N/A' && r.Element === 'Area harvested' && !isNaN(area)) {
                    crops[cropName] = area;
                }
            });
            const sortedCrops = Object.entries(crops).sort((a, b) => b[1] - a[1]).slice(0, 8);
            chartConfig = {
                type: 'bar',
                data: {
                    labels: sortedCrops.map(c => c[0]),
                    datasets: [{
                        label: 'Área cosechada (Hectáreas) - 2024',
                        data: sortedCrops.map(c => c[1]),
                        backgroundColor: '#10b981',
                        borderWidth: 0,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 9 } } },
                        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            };
        } 
        else if (key === 'sunat_export') {
            // Bar chart comparing sectors
            // Look for non-traditional sectors
            const labels = ['Agropecuario', 'Textil', 'Quimico', 'Pesquero no trad.'];
            const values = [];
            
            data.rows.forEach(r => {
                const sector = (r.Col_0 || r[''] || '').toLowerCase();
                const totalVal = parseFloat((r.Total || '').replace(/,/g, ''));
                if (sector.includes('agropecuario') && !isNaN(totalVal)) values[0] = totalVal / 1000; // in millions
                if (sector.includes('textil') && !isNaN(totalVal)) values[1] = totalVal / 1000;
                if (sector.includes('quimico') && !isNaN(totalVal)) values[2] = totalVal / 1000;
                if (sector.includes('pesquero no tradicional') && !isNaN(totalVal)) values[3] = totalVal / 1000;
            });
            
            chartConfig = {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Exportaciones FOB Trimestre 2026 (Millones USD)',
                        data: values,
                        backgroundColor: '#fbbf24',
                        borderWidth: 0,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#94a3b8' } },
                        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                    },
                    plugins: { legend: { labels: { color: '#f8fafc' } } }
                }
            };
        }
        else {
            // Default / hide chart for validated refs
            chartCard.style.display = 'none';
            return;
        }

        chartInstance = new Chart(ctx, chartConfig);
    }

    function renderTable() {
        document.getElementById('table-loading-container').style.display = 'none';
        document.getElementById('table-display-container').style.display = 'block';

        const head = document.getElementById('table-head');
        const body = document.getElementById('table-body');
        
        // 1. Render Header
        let headHtml = '<tr>';
        currentData.columns.forEach(col => {
            headHtml += `<th onclick="sortTable('${col}')">${col} ↕</th>`;
        });
        headHtml += '</tr>';
        head.innerHTML = headHtml;

        // 2. Paginate Rows
        const startIndex = (currentPage - 1) * pageSize;
        const endIndex = Math.min(startIndex + pageSize, filteredRows.length);
        const paginatedRows = filteredRows.slice(startIndex, endIndex);

        // 3. Render Body
        let bodyHtml = '';
        if (paginatedRows.length === 0) {
            bodyHtml = `<tr><td colspan="${currentData.columns.length}" style="text-align:center; color:var(--muted); font-style:italic; padding:30px;">No se encontraron registros que coincidan con la búsqueda.</td></tr>`;
        } else {
            paginatedRows.forEach(row => {
                bodyHtml += '<tr>';
                currentData.columns.forEach(col => {
                    const val = row[col] !== undefined && row[col] !== null ? row[col] : '';
                    bodyHtml += `<td>${val}</td>`;
                });
                bodyHtml += '</tr>';
            });
        }
        body.innerHTML = bodyHtml;

        // 4. Update Pagination Controls
        const total = filteredRows.length;
        document.getElementById('page-indicator').innerText = total > 0 ? 
            `Mostrando ${startIndex + 1}-${endIndex} de ${total}` : 
            'Mostrando 0-0 de 0';

        document.getElementById('prev-btn').disabled = currentPage === 1;
        document.getElementById('next-btn').disabled = endIndex >= total;
    }

    function filterRows(term) {
        term = term.toLowerCase().trim();
        if (term === '') {
            filteredRows = [...currentData.rows];
        } else {
            filteredRows = currentData.rows.filter(row => {
                return currentData.columns.some(col => {
                    const val = String(row[col]).toLowerCase();
                    return val.includes(term);
                });
            });
        }
        currentPage = 1;
        renderTable();
    }

    function sortAsc = true;
    let lastSortedCol = '';
    function sortTable(col) {
        if (lastSortedCol === col) {
            sortAsc = !sortAsc;
        } else {
            sortAsc = true;
            lastSortedCol = col;
        }
        
        filteredRows.sort((a, b) => {
            let valA = a[col];
            let valB = b[col];
            
            // Check if they are numeric
            const numA = parseFloat(valA);
            const numB = parseFloat(valB);
            
            if (!isNaN(numA) && !isNaN(numB)) {
                return sortAsc ? numA - numB : numB - numA;
            }
            
            valA = String(valA).toLowerCase();
            valB = String(valB).toLowerCase();
            if (valA < valB) return sortAsc ? -1 : 1;
            if (valA > valB) return sortAsc ? 1 : -1;
            return 0;
        });
        
        currentPage = 1;
        renderTable();
    }

    function changePageSize(val) {
        pageSize = parseInt(val);
        currentPage = 1;
        renderTable();
    }

    function prevPage() {
        if (currentPage > 1) {
            currentPage--;
            renderTable();
        }
    }

    function nextPage() {
        const total = filteredRows.length;
        if (currentPage * pageSize < total) {
            currentPage++;
            renderTable();
        }
    }

    // Load initial dataset on load
    window.onload = () => {
        loadDataset('synthetic_agro');
    };
</script>
</body>
</html>
\"\"\"
"""

# Find the place before if __name__ == '__main__':
split_str = "if __name__ == '__main__':"
parts = content.split(split_str)
if len(parts) == 2:
    new_content = parts[0] + datos_code + "\n" + split_str + parts[1]
    
    # 3. Add Flask routes for `/datos` and `/api/data/<key>` in the app routes section
    # Let's add them before `@app.route('/admin')` to keep it clean
    admin_decorator = "@app.route('/admin')"
    route_code = """
@app.route('/datos')
def view_data_explorer():
    \"\"\"Sirve la vista del Explorador de Datasets interactivo.\"\"\"
    return render_template_string(DATOS_TEMPLATE)


@app.route('/api/data/<key>')
def api_data_explorer(key):
    \"\"\"Servicio API para leer y estructurar archivos CSV del proyecto.\"\"\"
    DATA_FILES = {
        "bcrp_exchange": Path('/app/data/bcrp/bcrp-tipo-cambio-mensual.csv'),
        "faostat_prod": Path('/app/data/faostat/faostat-produccion-peru-2024.csv'),
        "sunat_export": Path('/app/data/sunat/sunat-exportacion-sectorial-2026.csv'),
        "synthetic_agro": Path('/app/data/dataset_agro_sintetico_v1.csv'),
        "validated_refs": Path('/app/entregable/referencias-datasets-validadas.csv')
    }
    
    if key not in DATA_FILES:
        return jsonify({"error": "Dataset no registrado"}), 404
        
    filepath = DATA_FILES[key]
    if not filepath.exists():
        return jsonify({"error": f"Archivo físico {filepath.name} no encontrado en el servidor. Asegúrese de haberlo generado."}), 404
        
    content = ""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
            break
        except Exception:
            continue
            
    if not content:
        return jsonify({"error": "No se pudo leer el archivo con ninguna codificación"}), 500
        
    lines = content.split('\\n')
    lines = [l for l in lines if l.strip()]
    
    start_index = 0
    if "sunat-exportacion-sectorial" in filepath.name:
        for idx, line in enumerate(lines):
            if "Sector" in line:
                start_index = idx
                break
                
    csv_data = "\\n".join(lines[start_index:])
    
    import csv
    import io
    reader = csv.reader(io.StringIO(csv_data))
    rows = []
    columns = []
    
    try:
        header = next(reader)
        columns = [h.strip() if h.strip() else f"Col_{i}" for i, h in enumerate(header)]
        for r in reader:
            if len(r) == 0:
                continue
            if len(r) < len(columns):
                r = r + [""] * (len(columns) - len(r))
            else:
                r = r[:len(columns)]
            rows.append(dict(zip(columns, r)))
    except Exception as e:
        return jsonify({"error": f"Error parseando CSV: {str(e)}"}), 500
        
    num_rows = len(rows)
    num_cols = len(columns)
    
    null_counts = {}
    for col in columns:
        null_counts[col] = 0
        
    for r in rows:
        for col in columns:
            val = str(r[col]).strip().lower()
            if val in ["", "n.d.", "n/d", "null", "none", "n.a.", "n/a"]:
                null_counts[col] += 1
                
    stats = {
        "num_rows": num_rows,
        "num_cols": num_cols,
        "null_counts": null_counts,
        "filename": filepath.name
    }
    
    return jsonify({
        "columns": columns,
        "rows": rows,
        "stats": stats
    })


"""
    new_content = new_content.replace(admin_decorator, route_code + admin_decorator)
    
    # Write back to app.py
    app_path.write_text(new_content, encoding='utf-8')
    print("app.py actualizado exitosamente con el Explorador de Datos!")
else:
    print("Error: No se encontró if __name__ == '__main__':")
