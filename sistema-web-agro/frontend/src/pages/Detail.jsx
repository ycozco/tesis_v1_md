import React, { useState, useEffect, useRef, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../App.jsx'

export default function Detail() {
  const { id_alerta } = useParams()
  const navigate = useNavigate()
  const { user, condicion } = useAuth()

  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [logLines, setLogLines] = useState([])
  const [loadError, setLoadError] = useState(null)
  const [logsMinimized, setLogsMinimized] = useState(true)
  const logEndRef = useRef(null)
  const logIntervalRef = useRef(null)

  const addLog = useCallback((msg, level = 'INFO') => {
    const ts = new Date().toLocaleTimeString('es-PE', { hour12: false })
    setLogLines(prev => [...prev, { ts, msg, level }])
  }, [])


  // Form states
  const [userDecision, setUserDecision] = useState(null)
  const [justificationText, setJustificationText] = useState('')
  const [likertComprehension, setLikertComprehension] = useState(0)
  const [hoverLikert, setHoverLikert] = useState(0)
  
  // Modal states
  const [showConfirmModal, setShowConfirmModal] = useState(false)
  const [activeRagDoc, setActiveRagDoc] = useState(null)

  // Timing states
  const startTimeRef = useRef(null)

  const [companyHistory, setCompanyHistory] = useState([])

  // Auto-scroll logs to bottom
  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logLines])

  useEffect(() => {
    startTimeRef.current = performance.now()

    // Simulated pipeline log steps (refleja lo que hace el backend)
    const PIPELINE_STEPS = [
      { delay: 100,  level: 'INFO',    msg: `[PIPELINE] Iniciando análisis para alerta: ${id_alerta}` },
      { delay: 300,  level: 'INFO',    msg: '[DB] Consultando operaciones_alertas en PostgreSQL...' },
      { delay: 600,  level: 'INFO',    msg: '[DB] Alerta recuperada — cargando variables de trazabilidad.' },
      { delay: 900,  level: 'INFO',    msg: '[SHAP] Cargando modelos XGBoost y LightGBM desde models_weights/...' },
      { delay: 1300, level: 'INFO',    msg: '[SHAP] Ejecutando TreeExplainer sobre vector de 4 features.' },
      { delay: 1700, level: 'INFO',    msg: '[SHAP] Valores SHAP calculados — recuperando de base de datos.' },
      { delay: 2000, level: 'INFO',    msg: '[RAG] Inicializando sentence-transformer (BGE-small-en-v1.5)...' },
      { delay: 2400, level: 'WARN',    msg: '[RAG] Búsqueda vectorial en pgvector — cosine similarity threshold: 0.75' },
      { delay: 2800, level: 'INFO',    msg: '[RAG] Documentos normativos recuperados: FDA, SENASA, Ley IA-PCM.' },
      { delay: 3100, level: 'INFO',    msg: '[LLM] Generando narrativa explicativa con Google Gemini Flash...' },
      { delay: 3500, level: 'INFO',    msg: '[LLM] Reporte generado — verificando fidelidad numérica (fidelity_score).' },
      { delay: 3900, level: 'SUCCESS', msg: '[PIPELINE] Análisis de 4 capas completado. Serializando respuesta JSON...' },
    ]

    PIPELINE_STEPS.forEach(({ delay, level, msg }) => {
      setTimeout(() => addLog(msg, level), delay)
    })

    fetch(`/api/alerts/${id_alerta}`)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`)
        return res.json()
      })
      .then(resData => {
        addLog('[API] Respuesta recibida del backend Flask/Gunicorn.', 'SUCCESS')
        setData(resData)
        if (resData.decision) {
          setUserDecision(resData.decision.user_decision)
          setJustificationText(resData.decision.justification_text)
          setLikertComprehension(resData.decision.likert_comprehension)
        }
        setLoading(false)
      })
      .catch(err => {
        addLog(`[ERROR] ${err.message}`, 'ERROR')
        console.error('Error fetching alert detail:', err)
        setLoadError(err.message)
        setLoading(false)
      })

    fetch(`/api/alerts/${id_alerta}/company-history`)
      .then(res => res.json())
      .then(histData => {
        setCompanyHistory(histData)
        addLog(`[DB] Historial de empresa: ${histData.length} operaciones cargadas.`, 'INFO')
      })
      .catch(err => {
        console.error('Error fetching company history:', err)
      })
  }, [id_alerta])

  if (loading || (!data && !loadError)) {
    return (
      <div className="flex h-screen bg-background text-on-background overflow-hidden">
        {/* LEFT — progress steps */}
        <div className="flex-1 flex flex-col items-center justify-center p-10 gap-6">
          <span className="material-symbols-outlined text-primary text-[64px] animate-spin" style={{animationDuration:'1.8s'}}>hub</span>
          <h2 className="font-headline-md text-on-surface text-center">Ejecutando Pipeline de 4 Capas</h2>
          <p className="text-on-surface-variant text-sm text-center max-w-xs">El motor de IA está analizando la operación. Los pasos se registran en tiempo real en el panel de logs.</p>
          <div className="w-full max-w-sm space-y-2 mt-2">
            {[
              { icon: 'database', label: 'Capa 1 — Extracción de datos', done: logLines.length > 2 },
              { icon: 'psychology', label: 'Capa 2 — Modelo de anomalía (Ensemble)', done: logLines.length > 4 },
              { icon: 'bar_chart_4_bars', label: 'Capa 3 — SHAP Explicabilidad', done: logLines.length > 6 },
              { icon: 'article', label: 'Capa 4 — RAG + Reporte LLM', done: logLines.length > 9 },
            ].map(({ icon, label, done }) => (
              <div key={label} className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-all duration-500 ${
                done ? 'glass-panel border border-primary/30' : 'opacity-40'
              }`}>
                <span className={`material-symbols-outlined text-[20px] ${
                  done ? 'text-primary' : 'text-on-surface-variant'
                }`}>{done ? 'check_circle' : icon}</span>
                <span className={`text-sm font-medium ${
                  done ? 'text-on-surface' : 'text-on-surface-variant'
                }`}>{label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT — live log terminal */}
        <div className="w-[420px] flex flex-col bg-[#0a0a0f] border-l border-white/5 font-mono-data">
          {/* Terminal header */}
          <div className="flex items-center gap-2 px-4 py-3 border-b border-white/10 bg-[#111118]">
            <div className="w-2.5 h-2.5 rounded-full bg-red-500"></div>
            <div className="w-2.5 h-2.5 rounded-full bg-yellow-500"></div>
            <div className="w-2.5 h-2.5 rounded-full bg-green-500"></div>
            <span className="ml-3 text-[11px] text-on-surface-variant tracking-widest uppercase">agro-intelligence · pipeline log</span>
            <span className="ml-auto text-[10px] text-primary animate-pulse">● LIVE</span>
          </div>
          {/* Log body */}
          <div className="flex-1 overflow-y-auto p-4 space-y-1 text-[11px] leading-relaxed">
            {logLines.length === 0 && (
              <span className="text-on-surface-variant opacity-50">Iniciando módulos del pipeline...</span>
            )}
            {logLines.map((line, i) => (
              <div key={i} className="flex gap-2">
                <span className="text-on-surface-variant shrink-0 select-none">{line.ts}</span>
                <span className={`shrink-0 font-bold ${
                  line.level === 'ERROR' ? 'text-red-400' :
                  line.level === 'WARN'  ? 'text-yellow-400' :
                  line.level === 'SUCCESS' ? 'text-green-400' :
                  'text-cyan-400'
                }`}>[{line.level}]</span>
                <span className="text-on-surface break-all">{line.msg}</span>
              </div>
            ))}
            {/* Blinking cursor */}
            <div className="flex gap-2">
              <span className="text-primary animate-pulse select-none">▌</span>
            </div>
            <div ref={logEndRef} />
          </div>
          {/* Terminal footer */}
          <div className="px-4 py-2 border-t border-white/10 bg-[#111118] text-[10px] text-on-surface-variant flex items-center justify-between">
            <span>{logLines.length} líneas registradas</span>
            <span className="text-primary">alerta: {id_alerta}</span>
          </div>
        </div>
      </div>
    )
  }

  if (loadError) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] gap-4">
        <span className="material-symbols-outlined text-error text-5xl">error</span>
        <h2 className="text-xl font-semibold text-error">Error al cargar el análisis</h2>
        <p className="text-on-surface-variant text-sm font-mono-data">{loadError}</p>
        <button className="glass-panel px-5 py-2 rounded-lg text-sm" onClick={() => navigate('/alerts')}>Volver a Alertas</button>
      </div>
    )
  }

  const { alert, explanations = [], decision } = data
  const isAudited = !!decision
  const dev = alert.valor_fob_esperado > 0 ? (((alert.valor_fob_esperado - alert.valor_fob_declarado) / alert.valor_fob_esperado) * 100).toFixed(1) : '0.0'

  // Map API vector documents to the local database keys
  const fetchedRagDocs = {}
  if (data.rag_documents) {
    data.rag_documents.forEach(doc => {
      const key = `${doc.categoria}-${doc.id_doc}`
      fetchedRagDocs[key] = {
        title: doc.titulo,
        body: doc.contenido
      }
    })
  }

  // RAG Document Database
  const RAG_DOCUMENTS = {
    'FDA-2025-C1': {
      title: 'FDA CFR Title 21 - Importación de Perecederos (Capítulo 1)',
      body: 'Sección 21.341 de la FDA: Todos los despachos agroindustriales con una desviación en valor FOB superior al 15% o que muestren proxies de riesgo logístico deben ser retenidos para inspección física sensorial de temperatura y calidad del empaque. Se debe verificar el contrato y la factura comercial contra la DAM.'
    },
    'SENASA-Directiva-04': {
      title: 'SENASA Directiva de Control Fitosanitario Agroexportador N° 04-2026',
      body: 'Directiva SENASA: Estipula inspecciones aleatorias obligatorias en puerto de origen (ej. Paita, Callao) para productos de palta Hass y uva que sufran retrasos mayores a 48 horas en zona primaria de embarque. Esto previene la propagación de plagas por pérdida de cadena de frío.'
    },
    'LMY-IA-D115': {
      title: 'Reglamento de la Ley de IA del Perú (D.S. N° 115-2025-PCM)',
      body: 'El reglamento estipula la obligación de los sistemas de IA de alto riesgo que operan en aduanas peruanas de proveer interfaces explicables a los operadores humanos para evitar sesgos discriminatorios algorítmicos. Las explicaciones locales (SHAP) y resúmenes narrativos RAG son obligatorios para validar anomalías.'
    },
    ...fetchedRagDocs
  }

  const handleOpenRag = (docId) => {
    if (RAG_DOCUMENTS[docId]) {
      setActiveRagDoc(RAG_DOCUMENTS[docId])
    }
  }

  const renderReportWithCitations = (text) => {
    if (!text) return null;

    // Procesar líneas del informe para compilar títulos, listas y citas
    const lines = text.split('\n');
    
    return lines.map((line, lineIdx) => {
      let trimmed = line.trim();
      if (!trimmed) return <div key={lineIdx} className="h-2"></div>;

      // 1. Títulos Principales (### o ####)
      if (trimmed.startsWith('###')) {
        const titleText = trimmed.replace(/^###\s+/, '');
        return (
          <h3 key={lineIdx} className="font-headline-sm text-[16px] text-primary border-b border-primary/20 pb-2 mt-4 mb-3 uppercase tracking-wider flex items-center gap-2">
            <span className="material-symbols-outlined text-[18px]">bookmark</span> {titleText}
          </h3>
        );
      }
      if (trimmed.startsWith('####')) {
        const titleText = trimmed.replace(/^####\s+/, '');
        return (
          <h4 key={lineIdx} className="font-headline-sm text-[13px] text-secondary mt-3 mb-2 uppercase tracking-wide flex items-center gap-1.5">
            <span className="material-symbols-outlined text-[15px]">label_important</span> {titleText}
          </h4>
        );
      }

      // 2. Líneas separadoras (---)
      if (trimmed === '---') {
        return <hr key={lineIdx} className="border-white/10 my-4" />;
      }

      // 3. Notas técnicas y advertencias (> ⚠️)
      if (trimmed.startsWith('>') || trimmed.startsWith('> ⚠️')) {
        const noteText = trimmed.replace(/^>\s*(⚠️)?\s*/, '');
        return (
          <div key={lineIdx} className="my-3 p-3 bg-error/10 border-l-4 border-error text-error rounded-r-lg font-body-sm text-[12px] flex items-start gap-2 leading-relaxed">
            <span className="material-symbols-outlined text-[16px] shrink-0 mt-0.5">warning</span>
            <div><strong>Nota de Riesgo:</strong> {noteText}</div>
          </div>
        );
      }

      // 4. Listas ordenadas o viñetas (- o *)
      let isListItem = false;
      if (trimmed.startsWith('-') || trimmed.startsWith('*')) {
        isListItem = true;
        trimmed = trimmed.replace(/^[-*]\s+/, '');
      }

      // 5. Compilar citas legislativas, negritas (**), y código en línea (`) dentro del texto
      const regex = /(\[[A-Z0-9_-]+\])/g;
      const parts = trimmed.split(regex);
      const processedLine = parts.flatMap((part, partIdx) => {
        const match = part.match(/^\[([A-Z0-9_-]+)\]$/);
        if (match) {
          const docId = match[1];
          const doc = RAG_DOCUMENTS[docId];
          if (doc) {
            return [
              <a
                key={`cit-${partIdx}`}
                href={`#${docId}`}
                onClick={(e) => {
                  e.preventDefault();
                  setActiveRagDoc(doc);
                }}
                className="bg-primary/10 text-primary border border-primary/20 px-1.5 py-0.5 rounded text-[10px] font-mono-data cursor-pointer hover:bg-primary/25 transition-colors mx-1 inline-flex items-center gap-0.5"
              >
                <span className="material-symbols-outlined text-[11px]">menu_book</span>
                {part}
              </a>
            ];
          }
        }

        // Parsear negritas (**bold**) y código (`code`) en el texto restante
        const boldAndCodeRegex = /(\*\*[^*]+\*\*|`[^`]+`)/g;
        const subParts = part.split(boldAndCodeRegex);
        
        return subParts.map((subPart, subIdx) => {
          if (subPart.startsWith('**') && subPart.endsWith('**')) {
            return <strong key={`b-${partIdx}-${subIdx}`} className="text-on-surface font-semibold">{subPart.slice(2, -2)}</strong>;
          }
          if (subPart.startsWith('`') && subPart.endsWith('`')) {
            return <code key={`c-${partIdx}-${subIdx}`} className="bg-white/5 border border-white/10 rounded px-1.5 py-0.5 text-[11px] text-secondary font-mono-data">{subPart.slice(1, -1)}</code>;
          }
          return subPart;
        });
      });

      if (isListItem) {
        return (
          <div key={lineIdx} className="flex items-start gap-2 pl-4 py-1 text-on-surface-variant font-body-md text-[13px]">
            <span className="text-secondary select-none shrink-0 mt-2.5 w-1.5 h-1.5 rounded-full bg-secondary"></span>
            <div className="flex-1 leading-relaxed">{processedLine}</div>
          </div>
        );
      }

      return (
        <p key={lineIdx} className="text-on-surface-variant leading-relaxed font-body-md text-[13px] mb-2 pl-2">
          {processedLine}
        </p>
      );
    });
  }

  const handleFormSubmit = (e) => {
    e.preventDefault()
    if (userDecision === null) {
      alert('Por favor seleccione una clasificación para la alerta.')
      return
    }
    if (likertComprehension === 0) {
      alert('Por favor califique su nivel de comprensión de la explicación de la IA.')
      return
    }
    // Open Confirmation Modal
    setShowConfirmModal(true)
  }

  const handleConfirmDecision = async () => {
    const endTime = performance.now()
    const elapsed = Math.round(endTime - startTimeRef.current)

    try {
      const response = await fetch(`/api/alerts/${id_alerta}/adjudicate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_decision: userDecision,
          justification_text: justificationText,
          likert_comprehension: likertComprehension,
          time_to_decision_ms: elapsed,
          username: user.username,
          condicion: condicion || 'INTEGRADO'
        })
      })

      if (response.ok) {
        setShowConfirmModal(false)
        navigate('/dashboard')
      } else {
        const errorData = await response.json()
        alert('Error al guardar la decisión: ' + errorData.message)
      }
    } catch (err) {
      console.error(err)
      alert('Error de red al guardar la decisión.')
    }
  }

  return (
    <div className="flex-grow overflow-y-auto p-container-padding pb-24 md:pb-container-padding">
      
      {/* Operation Header */}
      <div className="mb-gutter">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <span className={`px-2 py-0.5 rounded text-[10px] font-mono-data tracking-wider uppercase ${condicion === 'INTEGRADO' ? 'bg-primary/20 text-primary border border-primary/30' : 'bg-secondary/20 text-secondary border border-secondary/30'}`}>
                {condicion === 'INTEGRADO' ? 'Condición A (Explicable)' : 'Condición B (Aislada)'}
              </span>
              <span className="text-on-surface-variant font-mono-data text-[12px]">Estado de Alerta: <strong className="text-on-surface">{alert.estado}</strong></span>
            </div>
            <h2 className="font-headline-lg text-headline-lg text-on-surface flex items-center gap-3">
              <span className="material-symbols-outlined text-primary text-[32px]">inventory_2</span>
              DAM #{alert.numero_dam}
            </h2>
          </div>
          <div className="flex gap-3">
            <button className="glass-panel px-4 py-2 rounded-lg font-label-md text-label-md text-on-surface hover:bg-white/10 transition-colors flex items-center gap-2" onClick={() => navigate('/history')}>
              <span className="material-symbols-outlined text-[18px]">history</span>
              Historial
            </button>
            <button className="glass-panel px-4 py-2 rounded-lg font-label-md text-label-md text-on-surface hover:bg-white/10 transition-colors flex items-center gap-2" onClick={() => window.print()}>
              <span className="material-symbols-outlined text-[18px]">download</span>
              Exportar
            </button>
          </div>
        </div>
        
        {/* Meta Badges */}
        <div className="flex flex-wrap gap-2">
          <div className="glass-panel px-3 py-1.5 rounded-md flex items-center gap-2 border-l-2 border-l-primary/50">
            <span className="material-symbols-outlined text-[16px] text-on-surface-variant">corporate_fare</span>
            <span className="font-mono-data text-mono-data text-on-surface-variant">RUC:</span>
            <span className="font-mono-data text-mono-data text-on-surface">{alert.ruc_exportador}</span>
          </div>
          <div className="glass-panel px-3 py-1.5 rounded-md flex items-center gap-2 border-l-2 border-l-primary/50">
            <span className="material-symbols-outlined text-[16px] text-on-surface-variant">storefront</span>
            <span className="font-body-sm text-body-sm text-on-surface-variant">Empresa:</span>
            <span className="font-body-sm text-body-sm text-on-surface font-medium">{alert.razon_social}</span>
          </div>
          <div className="glass-panel px-3 py-1.5 rounded-md flex items-center gap-2 border-l-2 border-l-secondary/50">
            <span className="material-symbols-outlined text-[16px] text-on-surface-variant">eco</span>
            <span className="font-body-sm text-body-sm text-on-surface-variant">Producto:</span>
            <span className="font-body-sm text-body-sm text-on-surface font-medium">{alert.producto}</span>
          </div>
          <div className="glass-panel px-3 py-1.5 rounded-md flex items-center gap-2 border-l-2 border-l-tertiary/50">
            <span className="material-symbols-outlined text-[16px] text-on-surface-variant">sailing</span>
            <span className="font-body-sm text-body-sm text-on-surface-variant">Destino:</span>
            <span className="font-body-sm text-body-sm text-on-surface font-medium">Rotterdam (NLD)</span>
          </div>
        </div>
      </div>

      {/* Experimental Condition Banner */}
      <div className={`mb-4 flex items-center gap-3 px-4 py-2 rounded-lg text-sm ${
        condicion === 'INTEGRADO' ? 'bg-primary/10 border border-primary/30 text-primary' :
        condicion === 'ADMIN'     ? 'bg-secondary/10 border border-secondary/30 text-secondary' :
                                    'bg-surface-container border border-white/10 text-on-surface-variant'
      }`}>
        <span className="material-symbols-outlined text-[18px]">
          {condicion === 'INTEGRADO' ? 'visibility' : condicion === 'ADMIN' ? 'admin_panel_settings' : 'visibility_off'}
        </span>
        <span className="font-medium">
          {condicion === 'INTEGRADO'
            ? '🟢 Condición A — INTEGRADO: Capas de explicabilidad IA visibles'
            : condicion === 'ADMIN'
            ? '🔵 Modo Supervisión — Acceso completo a todas las capas de análisis'
            : '🟡 Condición B — AISLADO: Solo métricas de detección (sin SHAP/RAG)'}
        </span>
        <span className="ml-auto font-mono-data text-[11px] opacity-60">{condicion}</span>
      </div>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-card-gap">
        
        {/* Layer 1: GBDT Prediction (Col 1-6) */}
        <div className="xl:col-span-6 glass-panel rounded-xl p-6 relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-error/5 to-transparent opacity-50 pointer-events-none"></div>
          <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-6">
            <span className="material-symbols-outlined text-secondary">monitoring</span>
            Capa 1: Predicción de Valor (GBDT)
          </h3>
          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="flex-1 w-full space-y-6">
              <div>
                <div className="flex justify-between font-label-md text-label-md mb-2">
                  <span className="text-on-surface-variant">FOB Declarado</span>
                  <span className="text-on-surface font-mono-data">${alert.valor_fob_declarado.toLocaleString('en-US', { minimumFractionDigits: 2 })}</span>
                </div>
                <div className="h-3 w-full bg-surface-container rounded-full overflow-hidden">
                  <div className="h-full bg-surface-variant rounded-full relative" style={{ width: '60%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between font-label-md text-label-md mb-2">
                  <span className="text-primary flex items-center gap-1">
                    <span className="material-symbols-outlined text-[14px]">psychiatry</span> FOB Esperado (Modelo)
                  </span>
                  <span className="text-primary font-mono-data">${alert.valor_fob_esperado.toLocaleString('en-US', { minimumFractionDigits: 2 })}</span>
                </div>
                <div className="h-3 w-full bg-surface-container rounded-full overflow-hidden">
                  <div className="h-full bg-primary/80 rounded-full relative shadow-[0_0_10px_rgba(118,219,143,0.5)]" style={{ width: '85%' }}>
                    {/* Marker for declared value */}
                    <div className="absolute top-0 bottom-0 left-[70%] w-1 bg-white/50 z-10"></div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Semicircular SVG Gauge (Task 2.3) */}
            {(() => {
              const cleanPct = Math.max(0, Math.min(parseFloat(dev) || 0, 30))
              const angle = 180 - (cleanPct / 30 * 180) // 180deg (0% deviation) to 0deg (30% deviation)
              const radian = (angle * Math.PI) / 180
              const pointerX = 50 + 35 * Math.cos(radian)
              const pointerY = 50 - 35 * Math.sin(radian)
              return (
                <div className="flex flex-col items-center justify-center shrink-0 w-36 h-28 bg-white/[0.02] border border-white/5 rounded-xl p-3">
                  <svg className="w-full h-full overflow-visible" viewBox="0 0 100 60">
                    {/* Background Arcs for green, orange, red zones */}
                    {/* Zone 1: 0 - 5% (180deg to 150deg) */}
                    <path d="M 10 50 A 40 40 0 0 1 15.36 30" fill="none" stroke="#76db8f" strokeWidth="8" strokeLinecap="round" />
                    {/* Zone 2: 5 - 15% (150deg to 90deg) */}
                    <path d="M 15.36 30 A 40 40 0 0 1 50 10" fill="none" stroke="#f97316" strokeWidth="8" />
                    {/* Zone 3: 15 - 30% (90deg to 0deg) */}
                    <path d="M 50 10 A 40 40 0 0 1 90 50" fill="none" stroke="#ef4444" strokeWidth="8" strokeLinecap="round" />

                    {/* Center Pin */}
                    <circle cx="50" cy="50" r="5" fill="#fff" className="shadow-lg" />
                    {/* Pointer Hand */}
                    <line x1="50" y1="50" x2={pointerX} y2={pointerY} stroke="#fff" strokeWidth="2.5" strokeLinecap="round" className="transition-all duration-500 ease-out" />
                    
                    {/* Numeric deviation inside */}
                    <text x="50" y="44" textAnchor="middle" fill="#fff" fontSize="8" fontWeight="bold" className="font-mono-data">
                      {parseFloat(dev) > 0 ? `+${dev}%` : `${dev}%`}
                    </text>
                    <text x="50" y="54" textAnchor="middle" fill="rgba(255,255,255,0.4)" fontSize="4.5" fontWeight="bold" className="font-label-md uppercase tracking-wider">
                      Desviación
                    </text>
                  </svg>
                </div>
              )
            })()}
          </div>
        </div>

        {/* Layer 2: Ensemble Score (Col 7-12) */}
        <div className="xl:col-span-6 glass-panel rounded-xl p-6 relative border-error/30">
          <div className="absolute top-0 left-0 w-full h-1 bg-error animate-pulse"></div>
          <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-2">
            <span className="material-symbols-outlined text-error">gavel</span>
            Capa 2: Severidad de Anomalía (Ensemble)
          </h3>
          <p class="font-body-sm text-body-sm text-on-surface-variant mb-6">Consenso ponderado de Isolation Forest, Local Outlier Factor y ECOD.</p>
          <div className="flex items-center justify-center h-40 bg-error/5 border border-error/20 rounded-lg relative overflow-hidden group">
            <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-error/10 via-transparent to-transparent animate-pulse opacity-50"></div>
            <div className="flex flex-col items-center z-10">
              <span className="material-symbols-outlined text-[48px] text-error mb-2 drop-shadow-[0_0_15px_rgba(255,180,171,0.5)]">
                {alert.score_anomalia > 0.65 ? 'warning_amber' : 'check_circle'}
              </span>
              <h4 className="font-display-lg text-[36px] text-error tracking-tight drop-shadow-[0_0_10px_rgba(255,180,171,0.3)]">
                {alert.score_anomalia > 0.8 ? 'RIESGO CRÍTICO' : alert.score_anomalia > 0.6 ? 'RIESGO ALTO' : 'RIESGO BAJO'}
              </h4>
              <div className="font-mono-data text-[12px] text-error/80 mt-2 bg-error/10 px-3 py-1 rounded-full border border-error/20">
                Puntaje del Consenso: {alert.score_anomalia.toFixed(3)}
              </div>
            </div>
          </div>
        </div>

        {/* ----------------- SECCIÓN EXCLUSIVA DE EXPLICABILIDAD CON IA ----------------- */}
        {(condicion === 'INTEGRADO' || condicion === 'ADMIN') && (
          <div className="xl:col-span-12 grid grid-cols-1 xl:grid-cols-12 gap-card-gap p-6 bg-gradient-to-b from-[#131320]/80 to-[#0a0a0f]/40 border border-primary/20 rounded-2xl relative overflow-hidden my-4">
            {/* Glow Decorative Header line */}
            <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-primary/50 to-transparent"></div>
            
            {/* Header Section */}
            <div className="xl:col-span-12 flex items-center gap-3 mb-2 border-b border-white/5 pb-4">
              <span className="material-symbols-outlined text-primary text-[32px] animate-pulse">auto_awesome</span>
              <div>
                <h3 className="font-display-lg text-headline-sm text-on-surface font-bold tracking-wide uppercase">
                  MÓDULO DE EXPLICABILIDAD EXPLICATIVA CON IA
                </h3>
                <p className="text-on-surface-variant font-body-sm text-body-sm">
                  Evaluación transparente bajo conformidad del Decreto Supremo N.° 115-2025-PCM (Reglamento de la Ley de IA del Perú).
                </p>
              </div>
            </div>

            {/* Layer 3: SHAP Explicability (Full Width Inside Module) */}
            <div className="xl:col-span-12 glass-panel rounded-xl p-6 bg-white/[0.01]">
              <div className="flex justify-between items-end mb-6">
                <div>
                  <h4 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2">
                    <span className="material-symbols-outlined text-tertiary">analytics</span>
                    Capa 3: Variables de Influencia Local (Atribución SHAP)
                  </h4>
                  <p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Factores que impulsan el score (Rojo aumenta la probabilidad de anomalía; Azul reduce el riesgo).</p>
                </div>
                <button 
                  className="text-primary text-label-md font-label-md flex items-center hover:underline"
                  onClick={() => handleOpenRag('LMY-IA-D115')}
                >
                  Regulación Ley de IA <span className="material-symbols-outlined text-[16px] ml-1">arrow_forward</span>
                </button>
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-x-12 gap-y-4">
                {explanations.map((exp, index) => {
                  const isPositive = exp.shap_value >= 0
                  const absVal = Math.min(Math.abs(exp.shap_value) * 150, 95) // Scale for visualization
                  
                  return (
                    <div key={exp.id_explicacion || index} className="flex items-center gap-4 group">
                      <div className="w-1/3 text-right font-label-md text-label-md text-on-surface truncate group-hover:text-primary transition-colors">
                        {exp.variable_nombre}
                      </div>
                      <div className={`w-2/3 flex items-center gap-2 ${isPositive ? '' : 'flex-row-reverse justify-end'}`}>
                        <div 
                          className={`h-4 rounded-sm transition-all duration-300 ${isPositive ? 'bg-error/85' : 'bg-tertiary/85'}`}
                          style={{ width: `${absVal}%` }}
                        ></div>
                        <span className={`font-mono-data text-[12px] ${isPositive ? 'text-error' : 'text-tertiary'}`}>
                          {isPositive ? `+${exp.shap_value.toFixed(2)}` : exp.shap_value.toFixed(2)}
                        </span>
                        <span className="text-[10px] text-on-surface-variant font-mono-data ml-2">(val: {exp.variable_valor})</span>
                      </div>
                    </div>
                  )
                })}
                {explanations.length === 0 && (
                  <div className="col-span-2 text-center py-4 text-on-surface-variant">No se registraron explicaciones SHAP para esta operación.</div>
                )}
              </div>
            </div>

            {/* Layer 4: RAG Report (Full Width Inside Module) */}
            <div className="xl:col-span-12 glass-panel rounded-xl p-6 flex flex-col bg-white/[0.01]">
              <h4 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-4">
                <span className="material-symbols-outlined text-primary">description</span>
                Capa 4: Narrativa Técnica de IA (Motor RAG)
              </h4>
              <div className="flex-1 glass-panel bg-surface-container-low/50 rounded-lg p-5 border border-white/5 font-body-md text-body-md text-on-surface-variant leading-relaxed overflow-y-auto max-h-[350px] whitespace-pre-wrap">
                {renderReportWithCitations(data.rag_report)}
              </div>
              <div className="mt-3 flex justify-end gap-2 text-on-surface-variant font-label-md text-[10px] uppercase tracking-wider">
                <span className="flex items-center gap-1">
                  <span className="material-symbols-outlined text-[14px]">auto_awesome</span> Generado por RAG Core v2.5
                </span>
              </div>
            </div>
          </div>
        )}


        {/* Adjudication Panel (Col 8-12 / Col 1-5 if B) */}
        <div className={`${(condicion === 'INTEGRADO' || condicion === 'ADMIN') ? 'xl:col-span-5' : 'xl:col-span-12'} glass-panel-elevated rounded-xl p-6 flex flex-col border-primary/20`}>
          <h3 className="font-headline-sm text-headline-sm text-primary flex items-center gap-2 mb-6">
            <span className="material-symbols-outlined">rule</span>
            Adjudicación de Operación
          </h3>
          
          <form className="flex-1 flex flex-col space-y-6" onSubmit={handleFormSubmit}>
            
            {/* Radio Buttons */}
            <div className="space-y-3">
              <label className={`flex items-center gap-3 p-3 rounded-lg border border-outline/30 ${isAudited ? '' : 'cursor-pointer hover:bg-white/5'} transition-colors focus-within:border-primary focus-within:bg-primary/5 ${userDecision === 1 ? 'border-primary bg-primary/5' : ''}`}>
                <input 
                  className="w-4 h-4 text-primary bg-transparent border-outline focus:ring-primary focus:ring-offset-background" 
                  name="adjudication" 
                  type="radio" 
                  value="1"
                  checked={userDecision === 1}
                  onChange={() => !isAudited && setUserDecision(1)}
                  disabled={isAudited}
                />
                <span className="font-body-md text-on-surface font-semibold">Anomalía Confirmada (True Positive)</span>
              </label>
              <label className={`flex items-center gap-3 p-3 rounded-lg border border-outline/30 ${isAudited ? '' : 'cursor-pointer hover:bg-white/5'} transition-colors focus-within:border-secondary focus-within:bg-secondary/5 ${userDecision === 0 ? 'border-secondary bg-secondary/5' : ''}`}>
                <input 
                  className="w-4 h-4 text-secondary bg-transparent border-outline focus:ring-secondary focus:ring-offset-background" 
                  name="adjudication" 
                  type="radio" 
                  value="0"
                  checked={userDecision === 0}
                  onChange={() => !isAudited && setUserDecision(0)}
                  disabled={isAudited}
                />
                <span className="font-body-md text-on-surface font-semibold">Falsa Alarma (Deriva del Modelo)</span>
              </label>
              <label className={`flex items-center gap-3 p-3 rounded-lg border border-outline/30 ${isAudited ? '' : 'cursor-pointer hover:bg-white/5'} transition-colors focus-within:border-tertiary focus-within:bg-tertiary/5 ${userDecision === 2 ? 'border-tertiary bg-tertiary/5' : ''}`}>
                <input 
                  className="w-4 h-4 text-tertiary bg-transparent border-outline focus:ring-tertiary focus:ring-offset-background" 
                  name="adjudication" 
                  type="radio" 
                  value="2"
                  checked={userDecision === 2}
                  onChange={() => !isAudited && setUserDecision(2)}
                  disabled={isAudited}
                />
                <span className="font-body-md text-on-surface font-semibold">Dudoso / Requiere Inspección Física</span>
              </label>
            </div>

            {/* Justification Text */}
            <div className="space-y-2">
              <div className="flex justify-between font-label-md text-label-md text-on-surface-variant">
                <span>Nota de Justificación Técnica</span>
                <span className="font-mono-data text-[10px]">{justificationText.length} / 250</span>
              </div>
              <textarea 
                className="w-full bg-transparent border border-outline/50 rounded-lg p-3 text-body-sm font-body-sm text-on-surface placeholder:text-on-surface-variant/40 focus:border-primary focus:ring-1 focus:ring-primary focus:bg-white/5 transition-all resize-none disabled:opacity-75" 
                placeholder="Ingrese el razonamiento técnico que sustente su clasificación..." 
                rows="3"
                value={justificationText}
                onChange={(e) => !isAudited && setJustificationText(e.target.value.slice(0, 250))}
                required
                disabled={isAudited}
              />
            </div>

            {/* Likert Scale */}
            <div className="space-y-2">
              <label className="font-label-md text-label-md text-on-surface-variant block">Calificación de Comprensión de Explicación de IA</label>
              <div className="flex items-center gap-2">
                {[1, 2, 3, 4, 5].map(starVal => (
                  <button 
                    key={starVal}
                    className="transition-colors focus:outline-none"
                    type="button"
                    onClick={() => !isAudited && setLikertComprehension(starVal)}
                    onMouseEnter={() => !isAudited && setHoverLikert(starVal)}
                    onMouseLeave={() => !isAudited && setHoverLikert(0)}
                    disabled={isAudited}
                  >
                    <span 
                      className={`material-symbols-outlined text-[28px] ${
                        starVal <= (hoverLikert || likertComprehension) ? 'text-primary' : 'text-on-surface-variant'
                      }`}
                      style={{ fontVariationSettings: starVal <= (hoverLikert || likertComprehension) ? "'FILL' 1" : "'FILL' 0" }}
                    >
                      star
                    </span>
                  </button>
                ))}
                <span className="text-[11px] font-mono-data text-on-surface-variant ml-2">
                  {likertComprehension === 1 && 'Muy Incomprensible'}
                  {likertComprehension === 2 && 'Dificultosa'}
                  {likertComprehension === 3 && 'Aceptable'}
                  {likertComprehension === 4 && 'Comprensible'}
                  {likertComprehension === 5 && 'Altamente Explicable'}
                </span>
              </div>
            </div>

            {/* Submit Action */}
            {!isAudited ? (
              <button 
                className="w-full mt-auto bg-primary text-on-primary font-label-md text-label-md py-3 px-4 rounded-lg hover:bg-primary-fixed transition-colors flex justify-center items-center gap-2 shadow-[0_0_15px_rgba(118,219,143,0.3)] hover:shadow-[0_0_25px_rgba(118,219,143,0.5)]" 
                type="submit"
              >
                <span className="material-symbols-outlined text-[18px]">send</span>
                Enviar Decisión a Telemetría
              </button>
            ) : (
              <div className="p-4 bg-primary/10 border border-primary/20 text-primary rounded-lg text-center font-label-md text-label-md flex justify-center items-center gap-2">
                <span className="material-symbols-outlined">lock</span>
                DECISIÓN REGISTRADA EN EL HISTORIAL
              </div>
            )}
          </form>
        </div>

        {/* Historial de la Empresa Exportadora */}
        <div className="xl:col-span-12 glass-panel rounded-xl p-6">
          <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-4">
            <span className="material-symbols-outlined text-primary">history_edu</span>
            Historial del Exportador (Comportamiento de Reincidencia)
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse font-mono-data text-xs">
              <thead>
                <tr className="bg-white/[0.02] border-b border-primary/20 font-label-md text-label-md text-on-surface-variant uppercase">
                  <th className="py-2.5 px-4">ID ALERTA</th>
                  <th className="py-2.5 px-4">DAM</th>
                  <th className="py-2.5 px-4">FECHA OPERACIÓN</th>
                  <th className="py-2.5 px-4">PRODUCTO</th>
                  <th className="py-2.5 px-4 text-right">VALOR FOB DECLARADO</th>
                  <th className="py-2.5 px-4 text-right">VALOR FOB ESPERADO</th>
                  <th className="py-2.5 px-4 text-right">SCORE ANOMALÍA</th>
                  <th className="py-2.5 px-4 text-right">ESTADO</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-on-surface">
                {companyHistory.map(hist => (
                  <tr key={hist.id_alerta} className="hover:bg-white/5 transition-colors">
                    <td className="py-3.5 px-4 text-primary font-bold">{hist.id_alerta}</td>
                    <td className="py-3.5 px-4">{hist.numero_dam}</td>
                    <td className="py-3.5 px-4">{hist.fecha_operacion}</td>
                    <td className="py-3.5 px-4">{hist.producto}</td>
                    <td className="py-3.5 px-4 text-right">${hist.valor_fob_declarado.toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                    <td className="py-3.5 px-4 text-right">${hist.valor_fob_esperado.toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                    <td className="py-3.5 px-4 text-right font-bold text-secondary">{hist.score_anomalia.toFixed(4)}</td>
                    <td className="py-3.5 px-4 text-right">
                      <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold ${
                        hist.estado === 'CONFIRMADA' ? 'bg-error/15 text-error border border-error/20' :
                        hist.estado === 'PENDIENTE' ? 'bg-secondary/15 text-secondary border border-secondary/20' :
                        'bg-surface-variant text-on-surface-variant border border-white/10'
                      }`}>
                        {hist.estado}
                      </span>
                    </td>
                  </tr>
                ))}
                {companyHistory.length === 0 && (
                  <tr>
                    <td colSpan="8" className="py-6 text-center text-on-surface-variant font-body-sm">Sin otras alertas históricas para este exportador.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

      </div>

      {/* ----------------- MODALES ----------------- */}

      {/* Modal 1: Confirmación de Adjudicación */}
      {showConfirmModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-modal max-w-md w-full rounded-xl p-6 relative overflow-hidden">
            <h3 className="font-headline-sm text-headline-sm text-primary mb-4 flex items-center gap-2">
              <span className="material-symbols-outlined">gavel</span>
              Confirmar Adjudicación
            </h3>
            <p className="font-body-md text-body-md text-on-surface-variant mb-6">
              ¿Está seguro de enviar esta decisión? Este registro se encriptará e inyectará en la base de datos de telemetría experimental para medir la eficiencia.
            </p>
            
            <div className="space-y-3 font-mono-data text-xs text-on-surface bg-white/5 p-4 rounded-lg mb-6 border border-white/5">
              <div className="flex justify-between">
                <span className="text-on-surface-variant">Clasificación:</span>
                <span className="font-bold text-primary">
                  {userDecision === 1 && 'Anomalía Confirmada'}
                  {userDecision === 0 && 'Falsa Alarma'}
                  {userDecision === 2 && 'Requiere Inspección'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-on-surface-variant">Calificación Explicabilidad:</span>
                <span>{likertComprehension} de 5 estrellas</span>
              </div>
              <div className="border-t border-white/10 pt-2">
                <span className="text-on-surface-variant block mb-1">Nota de Justificación:</span>
                <p className="italic text-on-surface-variant leading-relaxed">"{justificationText}"</p>
              </div>
            </div>

            <div className="flex justify-end gap-3">
              <button 
                className="px-4 py-2 bg-transparent text-on-surface font-label-md text-label-md hover:bg-white/5 rounded transition-colors"
                onClick={() => setShowConfirmModal(false)}
              >
                Cancelar
              </button>
              <button 
                className="px-6 py-2 bg-primary text-on-primary font-label-md text-label-md hover:bg-primary-fixed rounded transition-colors shadow-[0_0_10px_rgba(118,219,143,0.3)] font-semibold"
                onClick={handleConfirmDecision}
              >
                Confirmar y Registrar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal 2: Citas Normativas RAG */}
      {activeRagDoc && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-modal max-w-lg w-full rounded-xl p-6 relative border-t-4 border-t-primary">
            <button 
              className="absolute top-4 right-4 text-on-surface-variant hover:text-on-surface focus:outline-none"
              onClick={() => setActiveRagDoc(null)}
            >
              <span className="material-symbols-outlined">close</span>
            </button>
            <h3 className="font-headline-sm text-headline-sm text-primary mb-4 flex items-center gap-2 pr-6">
              <span className="material-symbols-outlined">menu_book</span>
              {activeRagDoc.title}
            </h3>
            <div className="font-body-md text-body-md text-on-surface-variant leading-relaxed bg-white/5 p-4 rounded-lg border border-white/5 max-h-[300px] overflow-y-auto mb-6">
              {activeRagDoc.body}
            </div>
            <div className="flex justify-end">
              <button 
                className="px-5 py-2 bg-primary/20 text-primary border border-primary/30 font-label-md text-label-md hover:bg-primary/30 rounded transition-colors"
                onClick={() => setActiveRagDoc(null)}
              >
                Entendido
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Dock de Logs del Pipeline Minimizable */}
      <div className={`fixed bottom-0 right-4 z-40 w-[460px] bg-[#0a0a0f] border-t border-x border-white/10 rounded-t-xl shadow-2xl transition-all duration-300 font-mono-data ${
        logsMinimized ? 'h-10' : 'h-[300px]'
      }`}>
        {/* Encabezado del Dock */}
        <div 
          className="flex items-center gap-2 px-4 py-2 border-b border-white/10 bg-[#111118] cursor-pointer hover:bg-[#181822] rounded-t-xl"
          onClick={() => setLogsMinimized(!logsMinimized)}
        >
          <span className="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse"></span>
          <span className="text-[10px] text-on-surface-variant font-bold uppercase tracking-wider">Módulos de IA (Pipeline Logs)</span>
          
          <div className="ml-auto flex items-center gap-2">
            <span className="text-[9px] bg-white/10 px-2 py-0.5 rounded text-on-surface-variant">{logLines.length} Msg</span>
            <span className="material-symbols-outlined text-[16px] text-on-surface-variant transition-transform duration-300" style={{
              transform: logsMinimized ? 'rotate(180deg)' : 'rotate(0deg)'
            }}>keyboard_arrow_down</span>
          </div>
        </div>

        {/* Cuerpo del Dock (Visible solo cuando no está minimizado) */}
        <div className="h-[258px] overflow-y-auto p-3 space-y-1 text-[10px] leading-relaxed">
          {logLines.map((line, i) => (
            <div key={i} className="flex gap-2">
              <span className="text-on-surface-variant shrink-0 select-none">{line.ts}</span>
              <span className={`shrink-0 font-bold ${
                line.level === 'ERROR' ? 'text-red-400' :
                line.level === 'WARN'  ? 'text-yellow-400' :
                line.level === 'SUCCESS' ? 'text-green-400' :
                'text-cyan-400'
              }`}>[{line.level}]</span>
              <span className="text-on-surface break-all">{line.msg}</span>
            </div>
          ))}
          <div ref={logEndRef} />
        </div>
      </div>

    </div>
  )
}
