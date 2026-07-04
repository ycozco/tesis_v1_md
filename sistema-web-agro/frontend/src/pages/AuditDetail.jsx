import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

export default function AuditDetail() {
  const { id_decision } = useParams()
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeRagDoc, setActiveRagDoc] = useState(null)

  useEffect(() => {
    fetch(`/api/decisiones/${id_decision}`)
      .then(res => res.json())
      .then(resData => {
        setData(resData)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching decision details:', err)
        setLoading(false)
      })
  }, [id_decision])

  if (loading || !data) {
    return (
      <div className="flex h-screen bg-background text-on-background overflow-hidden justify-center items-center">
        <div className="flex flex-col items-center gap-4">
          <span className="material-symbols-outlined text-primary text-[64px] animate-spin" style={{animationDuration:'1.8s'}}>sync</span>
          <h2 className="font-headline-md text-on-surface text-center">Cargando Registro Histórico</h2>
          <p className="text-on-surface-variant text-sm text-center">Recuperando trazabilidad del archivo de decisiones...</p>
        </div>
      </div>
    )
  }

  const { decision, alert, explanations = [] } = data
  const dev = alert.valor_fob_esperado > 0 ? (((alert.valor_fob_esperado - alert.valor_fob_declarado) / alert.valor_fob_esperado) * 100).toFixed(1) : '0.0'
  const isIntegrated = decision.condicion_experimento === 'INTEGRADO' || decision.condicion_experimento === 'ADMIN'

  // Map API vector documents
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

    const lines = text.split('\n');
    
    return lines.map((line, lineIdx) => {
      let trimmed = line.trim();
      if (!trimmed) return <div key={lineIdx} className="h-2"></div>;

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

      if (trimmed === '---') {
        return <hr key={lineIdx} className="border-white/10 my-4" />;
      }

      if (trimmed.startsWith('>') || trimmed.startsWith('> ⚠️')) {
        const noteText = trimmed.replace(/^>\s*(⚠️)?\s*/, '');
        return (
          <div key={lineIdx} className="my-3 p-3 bg-error/10 border-l-4 border-error text-error rounded-r-lg font-body-sm text-[12px] flex items-start gap-2 leading-relaxed">
            <span className="material-symbols-outlined text-[16px] shrink-0 mt-0.5">warning</span>
            <div><strong>Nota de Riesgo:</strong> {noteText}</div>
          </div>
        );
      }

      let isListItem = false;
      if (trimmed.startsWith('-') || trimmed.startsWith('*')) {
        isListItem = true;
        trimmed = trimmed.replace(/^[-*]\s+/, '');
      }

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

  return (
    <div className="flex-grow overflow-y-auto p-container-padding pb-24 md:pb-container-padding">
      
      {/* Operation Header */}
      <div className="mb-gutter">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <span className="bg-primary/20 text-primary border border-primary/30 px-2 py-0.5 rounded text-[10px] font-mono-data uppercase">
                Auditoría Congelada
              </span>
              <span className="text-on-surface-variant font-mono-data text-[12px]">Registro ID: DEC-{1000 + decision.id_decision}</span>
            </div>
            <h2 className="font-headline-lg text-headline-lg text-on-surface flex items-center gap-3">
              <span className="material-symbols-outlined text-primary text-[32px]">bookmark</span>
              Auditoría de DAM #{alert.numero_dam}
            </h2>
          </div>
          <button 
            className="glass-panel px-5 py-2 rounded-lg font-label-md text-label-md text-on-surface hover:bg-white/10 transition-colors flex items-center gap-2"
            onClick={() => navigate('/history')}
          >
            <span className="material-symbols-outlined text-[18px]">arrow_back</span>
            Volver al Historial
          </button>
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
        </div>
      </div>

      {/* Experimental Condition Banner */}
      <div className={`mb-4 flex items-center gap-3 px-4 py-2 rounded-lg text-sm ${
        decision.condicion_experimento === 'INTEGRADO' ? 'bg-primary/10 border border-primary/30 text-primary' :
        decision.condicion_experimento === 'ADMIN'     ? 'bg-secondary/10 border border-secondary/30 text-secondary' :
                                                          'bg-surface-container border border-white/10 text-on-surface-variant'
      }`}>
        <span className="material-symbols-outlined text-[18px]">
          {decision.condicion_experimento === 'INTEGRADO' ? 'visibility' : decision.condicion_experimento === 'ADMIN' ? 'admin_panel_settings' : 'visibility_off'}
        </span>
        <span className="font-medium">
          {decision.condicion_experimento === 'INTEGRADO'
            ? '🟢 Condición A — INTEGRADO: Capas de explicabilidad IA visibles al momento del registro'
            : decision.condicion_experimento === 'ADMIN'
            ? '🔵 Modo Supervisión — Acceso completo a todas las capas de análisis'
            : ' 🟡 Condición B — AISLADO: Solo métricas de detección visibles al momento del registro'}
        </span>
      </div>

      {/* Grid Layout Principal */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-stack-lg mt-6">
        
        {/* Columna Izquierda: Métricas de Riesgo y Capas Analíticas (lg:col-span-8) */}
        <div className="lg:col-span-8 flex flex-col gap-stack-lg">
          
          {/* Fila 1: Ensemble Card y Distribución de Probabilidad */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-stack-lg">
            
            {/* Tarjeta de Severidad PyOD */}
            <div className="glass-panel rounded-xl p-stack-lg flex flex-col justify-center items-center relative overflow-hidden min-h-[220px]">
              <div className="z-10 text-center space-y-stack-sm">
                <span className="material-symbols-outlined text-4xl text-error">warning</span>
                <h3 className="font-label-md text-label-md uppercase tracking-widest text-on-surface-variant text-[11px]">
                  Puntaje de Severidad PyOD
                </h3>
                <div className="text-[34px] font-bold tracking-tight uppercase anomaly-gradient leading-none my-1">
                  {alert.score_anomalia > 0.8 ? 'RIESGO CRÍTICO' : alert.score_anomalia > 0.6 ? 'RIESGO ALTO' : 'RIESGO BAJO'}
                </div>
                <p className="font-mono-sm text-mono-sm text-on-surface-variant">
                  Puntaje de Conjunto: <span className="text-white font-bold">{alert.score_anomalia.toFixed(4)}</span> / 1.000
                </p>
              </div>
            </div>

            {/* Distribución de Probabilidad y Métricas */}
            <div className="glass-panel rounded-xl p-stack-md flex flex-col justify-between">
              <h3 className="font-label-md text-label-md uppercase tracking-widest text-on-surface-variant mb-2 text-[11px]">
                Distribución de Probabilidad
              </h3>
              <div className="relative h-20 w-full chart-grid flex items-end mb-4 border-b border-l border-white/10 px-2 pb-1 overflow-hidden">
                <svg className="absolute inset-0 w-full h-full" preserveAspectRatio="none" viewBox="0 0 100 50">
                  <path d="M 0 50 C 20 50, 30 10, 50 5, 70 10, 80 50, 100 50" fill="none" stroke="rgba(156, 240, 255, 0.4)" strokeWidth="1.5"></path>
                  <circle cx={Math.max(15, Math.min(alert.score_anomalia * 100, 85))} cy="25" fill="#ef4444" r="3" className="animate-pulse"></circle>
                  <line stroke="#ef4444" strokeDasharray="2" strokeWidth="0.75" x1={Math.max(15, Math.min(alert.score_anomalia * 100, 85))} x2={Math.max(15, Math.min(alert.score_anomalia * 100, 85))} y1="25" y2="50"></line>
                </svg>
                <div className="absolute top-1 left-2 text-[8px] font-mono-sm text-error">DAM Actual</div>
                <div className="absolute top-1 right-2 text-[8px] font-mono-sm text-tertiary">Media Clúster</div>
              </div>
              <div className="grid grid-cols-3 gap-2 border-t border-white/5 pt-3">
                <div className="text-center">
                  <div className="text-[9px] text-on-surface-variant font-mono-sm uppercase">Precisión</div>
                  <div className="font-bold text-primary font-mono-sm text-[12px]">92.4%</div>
                </div>
                <div className="text-center border-l border-r border-white/10">
                  <div className="text-[9px] text-on-surface-variant font-mono-sm uppercase">Recall</div>
                  <div className="font-bold text-primary font-mono-sm text-[12px]">88.7%</div>
                </div>
                <div className="text-center">
                  <div className="text-[9px] text-on-surface-variant font-mono-sm uppercase">F1-Score</div>
                  <div className="font-bold text-primary font-mono-sm text-[12px]">0.905</div>
                </div>
              </div>
            </div>

          </div>

          {/* GBDT Regressor & Atribución Variables SHAP Horizontal */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-stack-lg">
            
            {/* Análisis Regresor GBDT */}
            <div className="glass-panel rounded-xl p-stack-md flex flex-col justify-between min-h-[170px]">
              <div className="flex items-center gap-2 mb-3">
                <span className="material-symbols-outlined text-primary text-[16px]">analytics</span>
                <h3 className="font-label-md text-label-md uppercase tracking-widest text-on-surface-variant text-[11px]">
                  Análisis Regresor GBDT
                </h3>
              </div>
              
              <div className="grid grid-cols-2 gap-stack-sm mb-3">
                <div>
                  <p className="text-on-surface-variant font-label-md text-[10px] uppercase">FOB Declarado</p>
                  <p className="font-headline-md text-lg font-bold text-error">${alert.valor_fob_declarado.toLocaleString('en-US', { minimumFractionDigits: 2 })}</p>
                </div>
                <div>
                  <p className="text-on-surface-variant font-label-md text-[10px] uppercase">Rango Esperado</p>
                  <p className="font-headline-md text-lg font-bold text-primary">${alert.valor_fob_esperado.toLocaleString('en-US', { minimumFractionDigits: 2 })}</p>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="relative w-16 h-10 flex items-center justify-center flex-shrink-0">
                  <svg className="w-full h-full transform" viewBox="0 0 100 60">
                    <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="rgba(255,255,255,0.1)" strokeLinecap="round" strokeWidth="8"></path>
                    <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#ec6a06" strokeDasharray="126" strokeDashoffset="30" strokeLinecap="round" strokeWidth="8"></path>
                    <line stroke="white" strokeLinecap="round" strokeWidth="2.5" transform={`rotate(${180 - (Math.max(0, Math.min(parseFloat(dev) || 0, 30)) / 30 * 180)} 50 50)`} x1="50" x2="50" y1="50" y2="15"></line>
                  </svg>
                </div>
                <p className="font-mono-sm text-[10px] text-secondary-fixed-dim bg-[#2c1a11]/45 p-2 rounded border border-secondary/15 flex-1">
                  Desviación: <strong className="text-error">-{dev}%</strong> del centroide. Impacto fiscal est.: <strong className="text-white">-${Math.abs(alert.valor_fob_esperado - alert.valor_fob_declarado).toLocaleString('en-US', {maximumFractionDigits:0})}</strong>
                </p>
              </div>
            </div>

            {/* Atribución de Variables SHAP (Barras Horizontales) */}
            <div className="glass-panel rounded-xl p-stack-md flex flex-col justify-between">
              <div className="flex items-center gap-2 mb-3">
                <span className="material-symbols-outlined text-tertiary text-[16px]">bar_chart</span>
                <h3 className="font-label-md text-label-md uppercase tracking-widest text-on-surface-variant text-[11px]">
                  Atribución de Variables (SHAP)
                </h3>
              </div>
              <div className="space-y-2">
                {isIntegrated ? (
                  explanations.slice(0, 4).map((exp, index) => {
                    const isPositive = exp.shap_value >= 0
                    const absVal = Math.min(Math.abs(exp.shap_value) * 150, 95)
                    return (
                      <div key={exp.id_explicacion || index} className="space-y-0.5">
                        <div className="flex justify-between text-[9px] font-mono-sm uppercase">
                          <span className="text-on-surface-variant">{exp.variable_nombre}</span>
                          <span className={`font-bold ${isPositive ? 'text-error' : 'text-tertiary'}`}>
                            {isPositive ? `+${exp.shap_value.toFixed(2)}` : exp.shap_value.toFixed(2)}
                          </span>
                        </div>
                        <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden relative">
                          <div 
                            className={`h-full rounded-full ${isPositive ? 'bg-error' : 'bg-tertiary'}`}
                            style={{ width: `${absVal}%` }}
                          ></div>
                        </div>
                      </div>
                    )
                  })
                ) : (
                  <div className="h-full flex items-center justify-center text-[10px] text-on-surface-variant/40 italic py-4">
                    Atribución oculta por la condición experimental.
                  </div>
                )}
              </div>
              {isIntegrated && (
                <button 
                  className="mt-2 w-full py-1.5 border border-white/10 rounded-lg text-[10px] font-label-md text-on-surface-variant hover:bg-white/5 hover:text-white transition-colors flex items-center justify-center gap-2"
                  onClick={() => handleOpenRag('LMY-IA-D115')}
                >
                  <span className="material-symbols-outlined text-[12px]">info</span>
                  Ver detalles RAG
                </button>
              )}
            </div>

          </div>

        </div>

        {/* Columna Derecha: Explicabilidad y Acción (lg:col-span-4) */}
        <div className="lg:col-span-4 flex flex-col gap-stack-lg">
          
          {/* Variables de Atribución SHAP con Datos */}
          <div className="glass-panel rounded-xl p-stack-md flex flex-col">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-label-md text-label-md uppercase tracking-widest text-on-surface-variant text-[11px]">
                Variables de Atribución SHAP
              </h3>
              <span className="material-symbols-outlined text-on-surface-variant text-sm">info</span>
            </div>
            
            <ul className="space-y-2">
              {isIntegrated ? (
                explanations.map((exp, index) => {
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
                })
              ) : (
                <div className="text-[10px] text-on-surface-variant/40 italic py-4 text-center">
                  Explicaciones locales no disponibles para esta condición.
                </div>
              )}
            </ul>
            {isIntegrated && (
              <div className="text-[9px] font-mono-sm text-on-surface-variant italic mt-3 pt-2 border-t border-white/5 flex justify-between">
                <span>Base E[f(x)] = 0.51</span>
                <span>Salida = {(0.51 + explanations.reduce((acc, cur) => acc + cur.shap_value, 0)).toFixed(2)}</span>
              </div>
            )}
          </div>

          {/* Adjudicación del Auditor (Métricas de Telemetría) */}
          <div className="glass-panel rounded-xl p-stack-md flex flex-col justify-between border border-primary/20">
            <h3 className="font-label-md text-label-md uppercase tracking-widest text-primary mb-3 text-[11px]">
              Decisión Registrada (Trazabilidad)
            </h3>
            
            <div className="space-y-3 font-mono-data text-xs text-on-surface">
              <div className="flex justify-between border-b border-white/5 pb-2">
                <span className="text-on-surface-variant">Clasificación:</span>
                <span className="font-bold">
                  {decision.user_decision === 1 && <span className="text-error">Anomalía</span>}
                  {decision.user_decision === 0 && <span className="text-secondary">Falsa Alarma</span>}
                  {decision.user_decision === 2 && <span className="text-tertiary">Inspección</span>}
                </span>
              </div>
              <div className="flex justify-between border-b border-white/5 pb-2">
                <span className="text-on-surface-variant">Tiempo de Decisión:</span>
                <span className="font-bold text-secondary">
                  {(decision.time_to_decision_ms / 1000).toFixed(2)}s
                </span>
              </div>
              <div className="flex justify-between border-b border-white/5 pb-2">
                <span className="text-on-surface-variant">Comprensión IA:</span>
                <div className="flex text-primary gap-0.5">
                  {[1, 2, 3, 4, 5].map(i => (
                    <span 
                      key={i} 
                      className="material-symbols-outlined text-[14px]"
                      style={{ fontVariationSettings: i <= decision.likert_comprehension ? "'FILL' 1" : "'FILL' 0" }}
                    >
                      star
                    </span>
                  ))}
                </div>
              </div>
              <div className="space-y-1">
                <span className="text-on-surface-variant text-[10px] uppercase">Justificación del Auditor</span>
                <div className="bg-white/5 border border-white/10 rounded-lg p-2 italic text-on-surface-variant text-[11px] max-h-[80px] overflow-y-auto custom-scrollbar">
                  "{decision.justification_text}"
                </div>
              </div>
            </div>
          </div>

        </div>

      </div>

      {/* ----------------- CAPA 4 NARRATIVA TÉCNICA RAG ----------------- */}
      {isIntegrated && (
        <div className="glass-panel rounded-xl p-6 mt-stack-lg flex flex-col bg-white/[0.01]">
          <h3 className="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-3">
            <span className="material-symbols-outlined text-primary">description</span>
            Capa 4: Narrativa Técnica de IA (Motor RAG)
          </h3>
          <p className="font-body-sm text-[12px] text-on-surface-variant mb-4">Sustentación jurídica y logística contextualizada registrada.</p>
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

      {/* ----------------- MODALES ----------------- */}

      {/* Modal Citas Normativas RAG */}
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

    </div>
  )
}
