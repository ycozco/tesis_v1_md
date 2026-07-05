import React, { useState, useEffect, useRef, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../App.jsx'
import SeverityPanel from '../components/SeverityPanel.jsx'
import ProbabilityPanel from '../components/ProbabilityPanel.jsx'
import RegressionPanel from '../components/RegressionPanel.jsx'
import ShapPanel from '../components/ShapPanel.jsx'

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
  const [showCorrectionModal, setShowCorrectionModal] = useState(false)

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
      </div>

      {/* Grid Layout Principal según Imagen */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-6">
        
        {/* Columna Izquierda: Métricas de Riesgo y Capas Analíticas (lg:col-span-8) */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          
          {/* Fila 1: Ensemble Card y Distribución de Probabilidad */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <SeverityPanel alert={alert} />
            <ProbabilityPanel alert={alert} />
          </div>

          {/* GBDT Regressor & Atribución Variables SHAP Horizontal */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <RegressionPanel alert={alert} />
            <ShapPanel explanations={explanations} handleOpenRag={handleOpenRag} />
          </div>

        </div>

        {/* Columna Derecha: Explicabilidad y Acción (lg:col-span-4) */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          
          {/* Variables de Atribución SHAP con Datos */}
          <div className="glass-panel rounded-xl p-4 flex flex-col">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-label-md text-label-md uppercase tracking-widest text-on-surface-variant text-[11px]">
                Variables de Atribución SHAP
              </h3>
              <span className="material-symbols-outlined text-on-surface-variant text-sm">info</span>
            </div>
            
            <ul className="space-y-2">
              {explanations.map((exp, index) => {
                const isPositive = exp.shap_value >= 0
                const percent = Math.min(Math.abs(exp.shap_value) * 100, 100)
                return (
                  <li key={exp.id_explicacion || index} className="flex flex-col bg-white/5 p-2 rounded-lg border border-white/10">
                    <div className="flex justify-between items-center mb-1">
                      <div className="flex items-center gap-2">
                        <span className={`material-symbols-outlined text-[14px] ${isPositive ? 'text-error' : 'text-tertiary'}`}>
                          {isPositive ? 'trending_up' : 'trending_down'}
                        </span>
                        <span className="font-mono-sm text-[11px] text-on-surface-variant uppercase truncate max-w-[120px]">{exp.variable_nombre}</span>
                      </div>
                      <span className={`font-bold font-mono-sm text-[11px] ${isPositive ? 'text-error' : 'text-tertiary'}`}>
                        {isPositive ? `+${exp.shap_value.toFixed(2)}` : exp.shap_value.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center text-[9px] font-mono-sm">
                      <span className="text-white/50">Valor: {exp.variable_valor}</span>
                      <div className="w-16 h-1 bg-white/10 rounded-full overflow-hidden">
                        <div className={`h-full ${isPositive ? 'bg-error' : 'bg-tertiary'}`} style={{ width: `${percent}%` }}></div>
                      </div>
                    </div>
                  </li>
                )
              })}
            </ul>
            <div className="text-[9px] font-mono-sm text-on-surface-variant italic mt-3 pt-2 border-t border-white/5 flex justify-between">
              <span>Base E[f(x)] = 0.51</span>
              <span>Salida = {(0.51 + explanations.reduce((acc, cur) => acc + cur.shap_value, 0)).toFixed(2)}</span>
            </div>
          </div>

          {/* Adjudicación Rápida (Formulario de Acción) */}
          <div className="glass-panel rounded-xl p-4 flex flex-col flex-1 min-h-[220px] justify-between">
            <h3 className="font-label-md text-label-md uppercase tracking-widest text-on-surface-variant mb-3 text-[11px]">
              Adjudicación Rápida
            </h3>
            
            <form className="flex-1 flex flex-col justify-between" onSubmit={handleFormSubmit}>
              <div className="space-y-3">
                <div className="flex gap-2">
                  <button 
                    type="button"
                    onClick={() => !isAudited && setUserDecision(1)}
                    className={`flex-1 py-2 px-1 text-[10px] font-bold rounded border ${userDecision === 1 ? 'bg-error/20 border-error text-error' : 'border-white/10 text-on-surface-variant'} transition-colors`}
                  >
                    Anomalía (TP)
                  </button>
                  <button 
                    type="button"
                    onClick={() => !isAudited && setUserDecision(0)}
                    className={`flex-1 py-2 px-1 text-[10px] font-bold rounded border ${userDecision === 0 ? 'bg-secondary/20 border-secondary text-secondary' : 'border-white/10 text-on-surface-variant'} transition-colors`}
                  >
                    Falsa Alarma
                  </button>
                  <button 
                    type="button"
                    onClick={() => !isAudited && setUserDecision(2)}
                    className={`flex-1 py-2 px-1 text-[10px] font-bold rounded border ${userDecision === 2 ? 'bg-tertiary/20 border-tertiary text-tertiary' : 'border-white/10 text-on-surface-variant'} transition-colors`}
                  >
                    Inspección
                  </button>
                </div>

                <div className="space-y-1">
                  <label className="font-label-md text-[10px] text-on-surface-variant uppercase">Justificación Técnica</label>
                  <textarea 
                    className="w-full bg-white/5 border border-white/10 rounded-lg p-2 font-mono-sm text-mono-sm focus:border-primary focus:ring-0 outline-none min-h-[60px] custom-scrollbar" 
                    placeholder="Ingrese comentarios de auditoría..."
                    value={justificationText}
                    onChange={(e) => !isAudited && setJustificationText(e.target.value.slice(0, 250))}
                    required
                    disabled={isAudited}
                  />
                </div>

                {/* Stars alignment */}
                <div className="flex items-center justify-between py-1 border-t border-white/5 mt-1">
                  <span className="text-[9px] text-on-surface-variant uppercase">Calificación IA:</span>
                  <div className="flex gap-1">
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
                          className={`material-symbols-outlined text-[16px] ${
                            starVal <= (hoverLikert || likertComprehension) ? 'text-primary' : 'text-on-surface-variant'
                          }`}
                          style={{ fontVariationSettings: starVal <= (hoverLikert || likertComprehension) ? "'FILL' 1" : "'FILL' 0" }}
                        >
                          star
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {!isAudited ? (
                <div className="grid grid-cols-2 gap-2 pt-2">
                  <button 
                    className="bg-primary text-on-primary font-label-md text-[11px] py-1.5 rounded-lg hover:brightness-110 active:scale-95 transition-all flex items-center justify-center gap-1 font-bold"
                    type="submit"
                  >
                    <span className="material-symbols-outlined text-[14px]">gavel</span>
                    Adjudicar
                  </button>
                  <button 
                    className="border border-white/10 text-white font-label-md text-[11px] py-1.5 rounded-lg hover:bg-white/10 active:scale-95 transition-all flex items-center justify-center gap-1"
                    type="button"
                    onClick={() => {
                      if (!isAudited) {
                        setUserDecision(2);
                        setJustificationText("Operación escalada para revisión física manual.");
                        setLikertComprehension(3);
                      }
                    }}
                  >
                    <span className="material-symbols-outlined text-[14px]">assignment_return</span>
                    Escalar
                  </button>
                </div>
              ) : (
                <div className="p-2 bg-primary/10 border border-primary/20 text-primary rounded-lg text-center font-label-md text-[10px] flex justify-center items-center gap-1 mt-2">
                  <span className="material-symbols-outlined text-[14px]">lock</span>
                  DECISIÓN REGISTRADA
                </div>
              )}
            </form>
          </div>

        </div>

      </div>

      {/* ----------------- CAPA 4 NARRATIVA TÉCNICA RAG (Ancho Completo Abajo) ----------------- */}
      {(condicion === 'INTEGRADO' || condicion === 'ADMIN') && (
        <div className="glass-panel rounded-xl p-6 mt-6 flex flex-col bg-white/[0.01]">
          <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-3">
            <span className="material-symbols-outlined text-primary">description</span>
            Capa 4: Narrativa Técnica de IA (Motor RAG)
          </h3>
          <p className="font-body-sm text-[12px] text-on-surface-variant mb-4">Sustentación jurídica y logística contextualizada.</p>
          <div className="glass-panel bg-surface-container-low/40 rounded-lg p-4 border border-white/5 font-body-md text-body-md text-on-surface-variant leading-relaxed overflow-y-auto max-h-[250px] whitespace-pre-wrap">
            {renderReportWithCitations(data.rag_report)}
          </div>
          <div className="mt-3 flex justify-end gap-2 text-on-surface-variant font-label-md text-[9px] uppercase tracking-wider">
            <span className="flex items-center gap-1 font-mono-data">
              <span className="material-symbols-outlined text-[12px] text-primary">auto_awesome</span> Generado por RAG Core v2.5
            </span>
          </div>
        </div>
      )}

      {/* ----------------- PLAN DE CORRECCIÓN DE AUDITORÍA ----------------- */}
      {(condicion === 'INTEGRADO' || condicion === 'ADMIN') && (
        <div className="border border-error/30 bg-error/5 p-5 rounded-xl mt-6 flex flex-col gap-4">
          <div className="flex items-center gap-3">
            <span className="material-symbols-outlined text-error text-[28px]">assignment_late</span>
            <div>
              <h3 className="font-headline-sm text-headline-sm text-error font-bold">
                Plan de Acción y Corrección Recomendado
              </h3>
              <p className="text-[11px] text-on-surface-variant font-mono-sm">Generación metodológica de respuesta ante anomalías críticas</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-2">
            <div className="bg-white/5 p-3 rounded-lg border border-white/5">
              <span className="font-mono-sm text-[9px] uppercase tracking-wider text-error font-bold block mb-1">🚨 Alerta Detectada</span>
              <p className="font-body-sm text-[12px] text-on-surface leading-relaxed">
                Subvaloración severa de exportación de <strong>{alert.producto}</strong> por el exportador <strong>{alert.razon_social}</strong> (desviación de -80% respecto al valor de referencia del modelo GBDT calibrado).
              </p>
            </div>
            
            <div className="bg-white/5 p-3 rounded-lg border border-white/5">
              <span className="font-mono-sm text-[9px] uppercase tracking-wider text-primary font-bold block mb-1">🎯 Conclusión del Sistema</span>
              <p className="font-body-sm text-[12px] text-on-surface leading-relaxed">
                Riesgo fiscal crítico confirmado por el Ensemble de PyOD (IF + LOF + ECOD: {alert.score_anomalia.toFixed(4)}). No se detectaron anomalías logísticas (retrasos, merma) que justifiquen una caída genuina del valor comercial.
              </p>
            </div>
            
            <div className="bg-white/5 p-3 rounded-lg border border-white/5">
              <span className="font-mono-sm text-[9px] uppercase tracking-wider text-secondary-fixed-dim font-bold block mb-1">📋 Recomendación Operativa</span>
              <p className="font-body-sm text-[12px] text-on-surface leading-relaxed">
                Detener el levante aduanero de la DAM <strong>{alert.numero_dam}</strong>, programar inspección física y solicitar factura comercial de compraventa e historial bancario de la transacción.
              </p>
            </div>
          </div>

          <div className="flex justify-end mt-2">
            <button 
              type="button"
              className="bg-error/20 text-error border border-error/30 hover:bg-error/30 transition-all font-label-md text-label-md py-2 px-5 rounded-lg flex items-center gap-2 font-bold"
              onClick={() => setShowCorrectionModal(true)}
            >
              <span className="material-symbols-outlined text-[16px]">verified_user</span>
              Ver Sustento y Documentación de Tesis
            </button>
          </div>
        </div>
      )}

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

      {/* Modal 3: Sustento de Plan de Corrección y Documentación */}
      {showCorrectionModal && (
        <div className="fixed inset-0 bg-black/85 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-modal max-w-2xl w-full rounded-xl p-6 relative border-t-4 border-t-error">
            <button 
              className="absolute top-4 right-4 text-on-surface-variant hover:text-on-surface focus:outline-none"
              onClick={() => setShowCorrectionModal(false)}
            >
              <span className="material-symbols-outlined">close</span>
            </button>
            <h3 className="font-headline-sm text-headline-sm text-error mb-4 flex items-center gap-2 pr-6">
              <span className="material-symbols-outlined">gavel</span>
              Sustento Metodológico y Normativa Legal
            </h3>
            
            <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar font-body-sm text-[13px] text-on-surface-variant leading-relaxed">
              <div className="bg-white/5 p-3 rounded-lg border border-white/5">
                <h4 className="font-bold text-white mb-1 flex items-center gap-1.5">
                  <span className="material-symbols-outlined text-[16px] text-error">balance</span>
                  1. Marco Legal Fitosanitario y de Valoración (SUNAT & SENASA)
                </h4>
                <p>
                  De acuerdo con el <strong>Procedimiento General de Valoración de Aduanas DESPA-PG.01</strong> de la SUNAT, ante desviaciones extremas de precios declarados que superen los umbrales de riesgo, se habilita la duda razonable. Asimismo, el <strong>Reglamento de la Ley de Sanidad Agraria (D.S. N° 030-2020-MINAGRI)</strong> dictaminado por el SENASA exige que la trazabilidad del lote se valide contra registros físicos para prevenir blanqueo de producción o fraude de origen.
                </p>
              </div>

              <div className="bg-white/5 p-3 rounded-lg border border-white/5">
                <h4 className="font-bold text-white mb-1 flex items-center gap-1.5">
                  <span className="material-symbols-outlined text-[16px] text-primary">auto_stories</span>
                  2. Sustentación Científica y Capas del Pipeline (Tesis Hub)
                </h4>
                <p>
                  La validez metodológica de esta recomendación está sustentada en los capítulos de la investigación adscrita al Tesis Hub. Puedes consultar los detalles de diseño en las siguientes secciones documentales de la tesis:
                </p>
                <ul className="list-disc pl-5 mt-2 space-y-1.5 font-mono-data text-xs">
                  <li>
                    <a href="http://localhost:8000/seccion/03-07-busqueda-datos-y-fuentes" target="_blank" rel="noreferrer" className="text-primary hover:underline flex items-center gap-1">
                      <span className="material-symbols-outlined text-[12px]">link</span>
                      Capítulo III: Fuentes y Operacionalización de Datos
                    </a>
                  </li>
                  <li>
                    <a href="http://localhost:8000/seccion/01-06-agent" target="_blank" rel="noreferrer" className="text-primary hover:underline flex items-center gap-1">
                      <span className="material-symbols-outlined text-[12px]">link</span>
                      Anexo B: Evaluación del Piloto de Usabilidad y Telemetría
                    </a>
                  </li>
                  <li>
                    <a href="http://localhost:8000/seccion/02-30-capitulo3" target="_blank" rel="noreferrer" className="text-primary hover:underline flex items-center gap-1">
                      <span className="material-symbols-outlined text-[12px]">link</span>
                      Capítulo III: Diseño Experimental del Ensemble PyOD
                    </a>
                  </li>
                </ul>
              </div>
            </div>

            <div className="flex justify-end gap-3 mt-6 border-t border-white/10 pt-4">
              <button 
                className="px-5 py-2 bg-error/20 text-error border border-error/30 font-label-md text-label-md hover:bg-error/30 rounded transition-colors"
                onClick={() => setShowCorrectionModal(false)}
              >
                Cerrar Sustento
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
