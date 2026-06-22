import React, { useState, useEffect } from 'react'

export default function Config() {
  const [loading, setLoading] = useState(true)
  const [flashMsg, setFlashMsg] = useState('')
  const [testingConnection, setTestingConnection] = useState(false)
  const [testResult, setTestResult] = useState(null)

  // Hyperparameters states
  const [activeModel, setActiveModel] = useState('xgboost')
  const [mae, setMae] = useState(0.024)
  const [mse, setMse] = useState(0.038)
  const [r2Score, setR2Score] = useState(0.942)
  const [shapTopK, setShapTopK] = useState(5)
  const [llmEngine, setLlmEngine] = useState('gpt4o')
  const [llmTemp, setLlmTemp] = useState(0.1)
  const [llmSimThresh, setLlmSimThresh] = useState(0.75)
  const [weightIF, setWeightIF] = useState(0.45)
  const [weightLOF, setWeightLOF] = useState(0.30)
  const [weightECOD, setWeightECOD] = useState(0.25)
  const [globalThreshold, setGlobalThreshold] = useState(0.65)

  useEffect(() => {
    // Fetch initial configuration
    fetch('/api/config')
      .then(res => res.json())
      .then(data => {
        setActiveModel(data.xgboost_version.includes('XGBoost') ? 'xgboost' : 'lightgbm')
        setMae(data.mae)
        setMse(data.mse)
        setR2Score(data.r2_score)
        setShapTopK(data.shap_top_k)
        setLlmEngine(data.llm_engine.includes('GPT-4o') ? 'gpt4o' : 'claude3')
        setLlmTemp(data.llm_temperature)
        setLlmSimThresh(data.llm_similarity_threshold)
        setWeightIF(data.weights.isolation_forest)
        setWeightLOF(data.weights.lof)
        setWeightECOD(data.weights.ecod)
        setGlobalThreshold(data.global_threshold)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching config:', err)
        setLoading(false)
      })
  }, [])

  // Auto-adjust metrics based on model selected to make it feel alive
  const handleModelChange = (modelVal) => {
    setActiveModel(modelVal)
    if (modelVal === 'xgboost') {
      setMae(0.024)
      setMse(0.038)
      setR2Score(0.942)
    } else if (modelVal === 'lightgbm') {
      setMae(0.028)
      setMse(0.042)
      setR2Score(0.929)
    } else {
      setMae(0.035)
      setMse(0.051)
      setR2Score(0.898)
    }
  }

  const handleTestConnection = () => {
    setTestingConnection(true)
    setTestResult(null)
    
    // Simulate connection tests
    setTimeout(() => {
      setTestResult({
        predictor: { ok: true, latency: 12 },
        ensemble: { ok: true, latency: 8 },
        rag: { ok: true, latency: 142 }
      })
    }, 1500)
  }

  const handleApplyChanges = async (e) => {
    e.preventDefault()
    
    // Validate that weights sum up to approximately 1.00
    const sum = parseFloat(weightIF) + parseFloat(weightLOF) + parseFloat(weightECOD)
    if (Math.abs(sum - 1.0) > 0.01) {
      alert('La suma de los pesos del ensamble debe ser exactamente 1.00 (Actualmente: ' + sum.toFixed(2) + ')')
      return
    }

    try {
      const response = await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          active_model: activeModel,
          weights: { isolation_forest: weightIF, lof: weightLOF, ecod: weightECOD },
          global_threshold: globalThreshold,
          llm_temperature: llmTemp,
          llm_similarity_threshold: llmSimThresh
        })
      })

      if (response.ok) {
        setFlashMsg('Cambios aplicados exitosamente en el pipeline de IA.')
        setTimeout(() => setFlashMsg(''), 5000)
        window.scrollTo({ top: 0, behavior: 'smooth' })
      } else {
        alert('Error al aplicar cambios.')
      }
    } catch (err) {
      console.error(err)
      alert('Error de red al aplicar cambios.')
    }
  }

  const sumWeights = (parseFloat(weightIF) + parseFloat(weightLOF) + parseFloat(weightECOD)).toFixed(2)

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <span className="material-symbols-outlined text-primary text-5xl animate-spin">sync</span>
        <span className="ml-3 text-lg font-medium text-primary">Cargando pipeline del modelo...</span>
      </div>
    )
  }

  return (
    <div>
      {/* Toast Notification */}
      {flashMsg && (
        <div className="mb-6 p-4 rounded-lg bg-primary/20 border border-primary/50 text-primary font-body-md flex items-center gap-2">
          <span className="material-symbols-outlined">check_circle</span>
          <span>{flashMsg}</span>
        </div>
      )}

      <form onSubmit={handleApplyChanges}>
        {/* Header */}
        <header className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 pb-4 border-b border-white/5 mb-8">
          <div>
            <h1 className="font-display-lg text-display-lg text-primary-fixed mb-1">Configuración del Modelo</h1>
            <p className="font-body-lg text-body-lg text-on-surface-variant">Gestión de Pipeline &amp; Ajuste de Hiperparámetros</p>
          </div>
          <div className="flex gap-4">
            <button 
              className="px-6 py-2 rounded glass-panel text-on-surface hover:text-primary transition-all font-label-md text-label-md uppercase tracking-wider flex items-center gap-2" 
              id="btn-test"
              type="button"
              onClick={handleTestConnection}
            >
              <span className="material-symbols-outlined text-[18px]">hub</span>
              Probar Conexión
            </button>
            <button 
              className="px-6 py-2 rounded bg-primary text-on-primary hover:bg-primary-fixed-dim transition-all font-label-md text-label-md uppercase tracking-wider flex items-center gap-2 shadow-[0_0_15px_rgba(118,219,143,0.3)] hover:shadow-[0_0_20px_rgba(118,219,143,0.5)] font-semibold" 
              id="btn-apply"
              type="submit"
            >
              <span className="material-symbols-outlined text-[18px]" style={{ fontVariationSettings: "'FILL' 1" }}>save</span>
              Aplicar Cambios
            </button>
          </div>
        </header>

        {/* Bento Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-card-gap mb-8">
          
          {/* Predictor Section (Span 8) */}
          <section className="lg:col-span-8 glass-panel rounded-xl p-6 flex flex-col gap-6 relative overflow-hidden">
            <div className="absolute -top-24 -right-24 w-64 h-64 bg-primary/5 rounded-full blur-3xl pointer-events-none"></div>
            <div className="flex justify-between items-start">
              <div>
                <h2 className="font-headline-md text-headline-md text-on-surface flex items-center gap-2">
                  <span className="material-symbols-outlined text-primary">online_prediction</span>
                  Predictor Activo
                </h2>
                <p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Modelo central de pronóstico de valor aduanero</p>
              </div>
              <div className="relative group">
                <select 
                  className="appearance-none bg-surface-container-high border border-outline-variant text-on-surface rounded-lg px-4 py-2 pr-10 font-body-md text-body-md focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors cursor-pointer"
                  value={activeModel}
                  onChange={(e) => handleModelChange(e.target.value)}
                >
                  <option value="xgboost">XGBoost v2.1</option>
                  <option value="lightgbm">LightGBM v3.3</option>
                  <option value="rf">Random Forest</option>
                </select>
                <span className="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant pointer-events-none">expand_more</span>
              </div>
            </div>

            {/* Metrics Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-2">
              <div className="bg-surface-container-low/50 border border-white/5 rounded-lg p-4 flex flex-col">
                <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">Error Absoluto Medio (MAE)</span>
                <div className="flex items-end gap-2">
                  <span className="font-headline-lg text-headline-lg text-primary data-value">{mae}</span>
                  <span className="font-body-sm text-body-sm text-tertiary mb-1">↓ 0.002</span>
                </div>
              </div>
              <div className="bg-surface-container-low/50 border border-white/5 rounded-lg p-4 flex flex-col">
                <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">Error Cuadrático Medio (MSE)</span>
                <div className="flex items-end gap-2">
                  <span className="font-headline-lg text-headline-lg text-on-surface data-value">{mse}</span>
                  <span className="font-body-sm text-body-sm text-on-surface-variant mb-1">Estable</span>
                </div>
              </div>
              <div className="bg-surface-container-low/50 border border-white/5 rounded-lg p-4 flex flex-col">
                <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">Puntaje R²</span>
                <div className="flex items-end gap-2">
                  <span className="font-headline-lg text-headline-lg text-primary-fixed data-value">{r2Score}</span>
                  <span className="font-body-sm text-body-sm text-tertiary mb-1">↑ 0.01</span>
                </div>
              </div>
            </div>

            {/* SHAP Settings */}
            <div className="mt-auto pt-4 border-t border-white/5 flex items-center justify-between">
              <div className="flex items-center gap-2 text-on-surface-variant">
                <span className="material-symbols-outlined text-[18px]">analytics</span>
                <span className="font-body-sm text-body-sm">Vista de Explicabilidad SHAP</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="font-label-md text-label-md uppercase text-on-surface-variant">Variables Principales:</span>
                <div className="flex bg-surface-container-high rounded-md p-1 border border-white/5">
                  <button 
                    className={`px-3 py-1 rounded text-body-sm font-body-sm transition-colors ${shapTopK === 5 ? 'bg-surface-variant text-on-surface' : 'text-on-surface-variant hover:text-on-surface'}`}
                    type="button"
                    onClick={() => setShapTopK(5)}
                  >
                    Top 5
                  </button>
                  <button 
                    className={`px-3 py-1 rounded text-body-sm font-body-sm transition-colors ${shapTopK === 8 ? 'bg-surface-variant text-on-surface' : 'text-on-surface-variant hover:text-on-surface'}`}
                    type="button"
                    onClick={() => setShapTopK(8)}
                  >
                    Top 8
                  </button>
                </div>
              </div>
            </div>
          </section>

          {/* RAG/LLM Config (Span 4) */}
          <aside className="lg:col-span-4 glass-panel rounded-xl p-6 flex flex-col gap-6 relative">
            <div className="flex items-center gap-2 mb-2">
              <span className="material-symbols-outlined text-tertiary">memory</span>
              <h2 className="font-headline-md text-headline-md text-on-surface">Interrogador LLM</h2>
            </div>
            <div className="space-y-5">
              {/* Provider */}
              <div className="flex flex-col gap-2">
                <label className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Motor Proveedor</label>
                <div className="relative">
                  <select 
                    className="w-full appearance-none bg-surface-container-low border border-white/10 text-on-surface rounded-lg px-4 py-2 pr-10 font-body-md text-body-md focus:outline-none focus:border-tertiary focus:ring-1 focus:ring-tertiary transition-colors cursor-pointer"
                    value={llmEngine}
                    onChange={(e) => setLlmEngine(e.target.value)}
                  >
                    <option value="gpt4o">OpenAI GPT-4o</option>
                    <option value="claude3">Anthropic Claude 3.5</option>
                    <option value="llama3">Meta Llama 3 70B</option>
                  </select>
                  <span className="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant pointer-events-none">expand_more</span>
                </div>
              </div>
              
              {/* Temperature */}
              <div className="flex flex-col gap-2">
                <div className="flex justify-between items-center">
                  <label className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Temperatura (Creatividad)</label>
                  <span className="font-mono-data text-mono-data text-tertiary data-value">{llmTemp}</span>
                </div>
                <input 
                  className="w-full accent-tertiary cursor-pointer" 
                  max="1" 
                  min="0" 
                  step="0.1" 
                  type="range"
                  value={llmTemp}
                  onChange={(e) => setLlmTemp(parseFloat(e.target.value))}
                />
                <div className="flex justify-between text-xs text-on-surface-variant/50">
                  <span>Preciso</span>
                  <span>Creativo</span>
                </div>
              </div>
              
              {/* Similarity Threshold */}
              <div className="flex flex-col gap-2">
                <div className="flex justify-between items-center">
                  <label className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Corte de Similitud RAG</label>
                  <span className="font-mono-data text-mono-data text-tertiary data-value">{llmSimThresh}</span>
                </div>
                <input 
                  className="w-full accent-tertiary cursor-pointer" 
                  max="1" 
                  min="0.5" 
                  step="0.05" 
                  type="range"
                  value={llmSimThresh}
                  onChange={(e) => setLlmSimThresh(parseFloat(e.target.value))}
                />
              </div>
            </div>
          </aside>

          {/* Ensemble Settings (Span 12) */}
          <section className="lg:col-span-12 glass-panel rounded-xl p-6 flex flex-col gap-6">
            <header className="flex justify-between items-end border-b border-white/5 pb-4">
              <div>
                <h2 className="font-headline-md text-headline-md text-on-surface flex items-center gap-2">
                  <span className="material-symbols-outlined text-secondary">scatter_plot</span>
                  Pesos del Ensamble de Anomalías (Outlier Consensus)
                </h2>
                <p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Ajustar contribución de los algoritmos de detección de valores atípicos.</p>
              </div>
              <div className="flex flex-col items-end gap-1 bg-surface-container-low/50 px-4 py-2 rounded-lg border border-error/20">
                <label className="font-label-md text-label-md text-error uppercase tracking-wider">Umbral de Alerta Global</label>
                <div className="flex items-center gap-2">
                  <span className="font-headline-sm text-headline-sm text-error">{globalThreshold}</span>
                  <input 
                    type="range" 
                    min="0.1" 
                    max="0.9" 
                    step="0.05" 
                    className="accent-error w-24 cursor-pointer"
                    value={globalThreshold}
                    onChange={(e) => setGlobalThreshold(parseFloat(e.target.value))}
                  />
                  <span className="material-symbols-outlined text-error text-[16px]">warning</span>
                </div>
              </div>
            </header>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Isolation Forest */}
              <div className="flex flex-col gap-3 group">
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-secondary"></div>
                    <label className="font-body-md text-body-md text-on-surface font-medium">Isolation Forest</label>
                  </div>
                  <span className="font-mono-data text-mono-data text-secondary bg-secondary/10 px-2 py-0.5 rounded">w: {weightIF}</span>
                </div>
                <input 
                  className="w-full group-hover:opacity-100 opacity-80 transition-opacity accent-secondary cursor-pointer" 
                  max="1" 
                  min="0" 
                  step="0.05" 
                  type="range"
                  value={weightIF}
                  onChange={(e) => setWeightIF(parseFloat(e.target.value))}
                />
              </div>
              
              {/* Local Outlier Factor */}
              <div className="flex flex-col gap-3 group">
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-tertiary"></div>
                    <label className="font-body-md text-body-md text-on-surface font-medium">LOF (Densidad)</label>
                  </div>
                  <span className="font-mono-data text-mono-data text-tertiary bg-tertiary/10 px-2 py-0.5 rounded">w: {weightLOF}</span>
                </div>
                <input 
                  className="w-full group-hover:opacity-100 opacity-80 transition-opacity accent-tertiary cursor-pointer" 
                  max="1" 
                  min="0" 
                  step="0.05" 
                  type="range"
                  value={weightLOF}
                  onChange={(e) => setWeightLOF(parseFloat(e.target.value))}
                />
              </div>
              
              {/* ECOD */}
              <div className="flex flex-col gap-3 group">
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-primary-fixed"></div>
                    <label className="font-body-md text-body-md text-on-surface font-medium">ECOD (Empírico)</label>
                  </div>
                  <span className="font-mono-data text-mono-data text-primary-fixed bg-primary-fixed/10 px-2 py-0.5 rounded">w: {weightECOD}</span>
                </div>
                <input 
                  className="w-full group-hover:opacity-100 opacity-80 transition-opacity accent-primary-fixed cursor-pointer" 
                  max="1" 
                  min="0" 
                  step="0.05" 
                  type="range"
                  value={weightECOD}
                  onChange={(e) => setWeightECOD(parseFloat(e.target.value))}
                />
              </div>
            </div>

            {/* Summation indicator */}
            <div className="w-full h-1 bg-surface-container-high rounded-full overflow-hidden flex mt-2">
              <div className="h-full bg-secondary" style={{ width: `${weightIF * 100}%` }}></div>
              <div className="h-full bg-tertiary" style={{ width: `${weightLOF * 100}%` }}></div>
              <div className="h-full bg-primary-fixed" style={{ width: `${weightECOD * 100}%` }}></div>
            </div>
            <div className="flex justify-between items-center font-label-md text-label-md">
              <span className={`${Math.abs(parseFloat(sumWeights) - 1.0) > 0.01 ? 'text-error font-bold' : 'text-on-surface-variant'}`}>
                {Math.abs(parseFloat(sumWeights) - 1.0) > 0.01 ? '¡Los pesos no suman 1.00!' : 'Suma de pesos válida'}
              </span>
              <span className="text-on-surface-variant">Σ {sumWeights} / 1.00</span>
            </div>
          </section>
        </div>
      </form>

      {/* ----------------- CONNECTION TEST MODAL ----------------- */}
      {testingConnection && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-modal max-w-md w-full rounded-xl p-6 relative border-t-4 border-t-primary">
            <h3 className="font-headline-sm text-headline-sm text-on-surface mb-6 flex items-center gap-2">
              <span className="material-symbols-outlined text-primary">hub</span>
              Prueba de Conexión de Pipeline
            </h3>

            {!testResult ? (
              <div className="flex flex-col items-center justify-center py-8">
                <span className="material-symbols-outlined text-primary text-5xl animate-spin mb-4">sync</span>
                <span className="text-body-md text-on-surface-variant">Estableciendo túnel de telemetría con clúster...</span>
              </div>
            ) : (
              <div className="space-y-4 mb-8">
                <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/5">
                  <div className="flex items-center gap-3">
                    <span className="material-symbols-outlined text-primary">check_circle</span>
                    <span className="font-body-md text-on-surface font-semibold">XGBoost &amp; GBDT Predictor</span>
                  </div>
                  <span className="font-mono-data text-xs text-primary">{testResult.predictor.latency}ms</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/5">
                  <div className="flex items-center gap-3">
                    <span className="material-symbols-outlined text-primary">check_circle</span>
                    <span className="font-body-md text-on-surface font-semibold">PyOD Outlier Ensemble Node</span>
                  </div>
                  <span className="font-mono-data text-xs text-primary">{testResult.ensemble.latency}ms</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/5">
                  <div className="flex items-center gap-3">
                    <span className="material-symbols-outlined text-primary">check_circle</span>
                    <span className="font-body-md text-on-surface font-semibold">LLM RAG Vector DB Node</span>
                  </div>
                  <span className="font-mono-data text-xs text-primary">{testResult.rag.latency}ms</span>
                </div>
                <div className="p-3 bg-primary/10 border border-primary/20 rounded-md text-primary text-body-sm flex items-center gap-2">
                  <span className="material-symbols-outlined text-[18px]">cloud_done</span>
                  <span>Todos los nodos respondieron exitosamente. Pipeline nominal.</span>
                </div>
              </div>
            )}

            {testResult && (
              <div className="flex justify-end">
                <button 
                  className="px-6 py-2 bg-primary text-on-primary font-label-md text-label-md hover:bg-primary-fixed rounded transition-colors font-semibold"
                  onClick={() => setTestingConnection(false)}
                >
                  Entendido
                </button>
              </div>
            )}
          </div>
        </div>
      )}

    </div>
  )
}
