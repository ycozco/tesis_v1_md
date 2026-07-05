import React, { useState, useEffect } from 'react'

export default function Data() {
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [fileName, setFileName] = useState('')

  // RAG normative states
  const [ragDocs, setRagDocs] = useState([])
  const [docTitle, setDocTitle] = useState('')
  const [docCategory, setDocCategory] = useState('FDA')
  const [docContent, setDocContent] = useState('')
  const [loadingDocs, setLoadingDocs] = useState(false)
  const [savingDoc, setSavingDoc] = useState(false)

  const [realData, setRealData] = useState([])
  const [selectedDeviationFilter, setSelectedDeviationFilter] = useState('ALL')

  useEffect(() => {
    fetchDocs()
    fetch('/api/data/preview')
      .then(res => res.json())
      .then(data => setRealData(data))
      .catch(err => console.error('Error fetching preview data:', err))
  }, [])

  // Filter rows by deviation range
  const filteredData = realData.filter(row => {
    if (selectedDeviationFilter === 'ALL') return true
    const fob_dec = row.valor_fob_declarado
    const fob_esp = row.valor_fob_esperado
    const desv_pct = fob_esp > 0 ? (Math.abs(fob_dec - fob_esp) / fob_esp) * 100 : 0
    if (selectedDeviationFilter === '0-5%') return desv_pct <= 5
    if (selectedDeviationFilter === '5-10%') return desv_pct > 5 && desv_pct <= 10
    if (selectedDeviationFilter === '10-15%') return desv_pct > 10 && desv_pct <= 15
    if (selectedDeviationFilter === '>15%') return desv_pct > 15
    return true
  })

  const fetchDocs = () => {
    setLoadingDocs(true)
    fetch('/api/config/documents')
      .then(res => res.json())
      .then(data => {
        setRagDocs(data)
        setLoadingDocs(false)
      })
      .catch(err => {
        console.error('Error fetching RAG docs:', err)
        setLoadingDocs(false)
      })
  }

  const handleAddDoc = async (e) => {
    e.preventDefault()
    if (!docTitle || !docContent) {
      alert('Por favor complete el título y el contenido.')
      return
    }
    setSavingDoc(true)
    try {
      const response = await fetch('/api/config/documents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          titulo: docTitle,
          categoria: docCategory,
          contenido: docContent
        })
      })
      if (response.ok) {
        setDocTitle('')
        setDocContent('')
        fetchDocs()
        alert('Documento normativo indexado y vectorizado en pgvector exitosamente.')
      } else {
        const errData = await response.json()
        alert('Error al indexar documento: ' + errData.message)
      }
    } catch (err) {
      console.error(err)
      alert('Error de red al indexar documento.')
    } finally {
      setSavingDoc(false)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const files = e.dataTransfer.files
    if (files.length > 0) {
      triggerUpload(files[0])
    }
  }

  const handleFileSelect = (e) => {
    const files = e.target.files
    if (files.length > 0) {
      triggerUpload(files[0])
    }
  }

  const triggerUpload = (file) => {
    setFileName(file.name)
    setUploading(true)
    setProgress(0)

    // Simulate progress
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval)
          setTimeout(() => {
            setUploading(false)
            alert(`Archivo "${file.name}" cargado y preprocesado exitosamente en el clúster.`)
          }, 500)
          return 100
        }
        return prev + 10
      })
    }, 150)
  }

  // Render real database preview rows
  const renderDataRows = () => {
    const statusColors = {
      'PENDIENTE': 'text-tertiary',
      'EN_REVISION': 'text-primary',
      'CONFIRMADA': 'text-error animate-pulse',
      'FALSA_ALARMA': 'text-primary-fixed-dim',
      'REFIERE_INSPECCION': 'text-secondary'
    }

    if (filteredData && filteredData.length > 0) {
      return filteredData.map((row, i) => (
        <tr key={row.id_alerta || i} className={`border-b border-white/5 hover:bg-white/5 transition-colors ${i % 2 === 0 ? 'bg-white/[0.02]' : ''}`}>
          <td className="px-4 py-2.5">{row.ruc_exportador}</td>
          <td className="px-4 py-2.5">${row.valor_fob_declarado.toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
          <td className="px-4 py-2.5">{row.producto}</td>
          <td className="px-4 py-2.5 text-on-surface-variant font-mono-data">{row.fecha_operacion}</td>
          <td className={`px-4 py-2.5 ${statusColors[row.estado] || 'text-on-surface'} font-bold text-[12px]`}>{row.estado}</td>
        </tr>
      ))
    }

    const rows = []
    for (let i = 1; i <= 5; i++) {
      rows.push(
        <tr key={i} className="border-b border-white/5 text-on-surface-variant">
          <td colSpan="5" className="px-4 py-4 text-center">No hay alertas que coincidan con este rango de desviación.</td>
        </tr>
      )
    }
    return rows
  }

  return (
    <div className="z-10 relative">
      <div className="absolute top-[-10%] right-[-10%] w-[600px] h-[600px] bg-primary/5 rounded-full blur-[120px] pointer-events-none"></div>

      <div className="max-w-7xl mx-auto space-y-card-gap">
        
        {/* Page Header */}
        <div className="flex justify-between items-end mb-8">
          <div>
            <h1 className="font-headline-lg text-headline-lg text-on-surface">Explorador de Datos</h1>
            <p className="font-body-md text-body-md text-on-surface-variant mt-1">Gestionar e ingerir datasets de telemetría para análisis agroindustrial.</p>
          </div>
        </div>

        {/* KPI Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-card-gap mb-8">
          <div className="glass-panel rounded-xl p-6 relative overflow-hidden group">
            <div className="absolute right-0 bottom-0 opacity-10">
              <span className="material-symbols-outlined text-[100px]" style={{ fontVariationSettings: "'FILL' 1" }}>dataset</span>
            </div>
            <div className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">Datasets Totales</div>
            <div className="font-display-lg text-display-lg text-primary">12</div>
            <div className="mt-4 flex items-center text-primary text-sm">
              <span className="material-symbols-outlined text-[16px] mr-1">trending_up</span>
              <span>+2 esta semana</span>
            </div>
          </div>
          <div className="glass-panel rounded-xl p-6 relative overflow-hidden">
            <div className="absolute right-0 bottom-0 opacity-10">
              <span className="material-symbols-outlined text-[100px]" style={{ fontVariationSettings: "'FILL' 1" }}>table_rows</span>
            </div>
            <div className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">Registros Totales</div>
            <div className="font-display-lg text-display-lg text-on-surface">1.2M</div>
            <div className="mt-4 flex items-center text-on-surface-variant text-sm">
              <span className="material-symbols-outlined text-[16px] mr-1">check_circle</span>
              <span>Validación de Consistencia OK</span>
            </div>
          </div>
          <div className="glass-panel rounded-xl p-6 relative overflow-hidden">
            <div className="absolute right-0 bottom-0 opacity-10">
              <span className="material-symbols-outlined text-[100px]" style={{ fontVariationSettings: "'FILL' 1" }}>sync</span>
            </div>
            <div className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">Última Sincronización</div>
            <div className="font-display-lg text-display-lg text-on-surface">Hace un Momento</div>
            <div className="mt-4 flex items-center text-primary text-sm">
              <span className="flex h-2 w-2 rounded-full bg-primary mr-2 shadow-[0_0_8px_#76db8f] animate-pulse"></span>
              <span>Telemetría en Vivo Activa</span>
            </div>
          </div>
        </div>

        {/* Main Content Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-card-gap">
          
          {/* Left Column: Datasets & Upload */}
          <div className="lg:col-span-1 flex flex-col space-y-card-gap">
            {/* Upload Zone */}
            <div className="glass-panel rounded-xl p-6 flex flex-col">
              <h2 className="font-headline-sm text-headline-sm text-on-surface mb-4 font-semibold">Ingesta de Datos</h2>
              
              <div 
                className="border-2 border-dashed border-outline-variant rounded-lg p-8 flex flex-col items-center justify-center text-center transition-all duration-300 hover:border-primary/50 hover:bg-primary/5 cursor-pointer relative" 
                id="dropzone"
                onDragOver={handleDragOver}
                onDrop={handleDrop}
              >
                <input 
                  type="file" 
                  id="file-input" 
                  className="hidden" 
                  accept=".csv,.xlsx" 
                  onChange={handleFileSelect}
                />
                <label htmlFor="file-input" className="cursor-pointer flex flex-col items-center">
                  <span className="material-symbols-outlined text-4xl text-on-surface-variant mb-3">cloud_upload</span>
                  <div className="font-body-md text-body-md text-on-surface mb-1">Arrastre y suelte CSV/XLSX</div>
                  <div className="font-body-sm text-body-sm text-on-surface-variant mb-4">Tamaño máx. 15MB</div>
                  <span className="px-4 py-2 bg-primary/10 text-primary border border-primary/30 rounded-lg hover:bg-primary/20 transition-colors font-label-md text-label-md">
                    Examinar Archivos
                  </span>
                </label>
              </div>

              {/* Upload Progress Bar */}
              {uploading && (
                <div className="mt-4 pt-4 border-t border-white/5">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-body-sm text-body-sm text-on-surface truncate max-w-[80%]">{fileName}</span>
                    <span className="font-body-sm text-body-sm text-primary">{progress}%</span>
                  </div>
                  <div className="h-1.5 w-full bg-surface-container-high rounded-full overflow-hidden">
                    <div className="h-full bg-primary rounded-full shadow-[0_0_10px_rgba(118,219,143,0.5)] transition-all duration-150" style={{ width: `${progress}%` }}></div>
                  </div>
                </div>
              )}
            </div>

            {/* Dataset List */}
            <div className="glass-panel rounded-xl p-6 flex-grow">
              <div className="flex justify-between items-center mb-4">
                <h2 className="font-headline-sm text-headline-sm text-on-surface font-semibold">Datasets Activos</h2>
                <button className="text-primary hover:text-primary-fixed transition-colors">
                  <span className="material-symbols-outlined">filter_list</span>
                </button>
              </div>
              <ul className="space-y-2">
                <li className="p-3 rounded-lg border border-transparent cursor-pointer flex items-center justify-between group bg-surface-container-high/30 border-l-2 border-l-primary">
                  <div className="flex items-center">
                    <span className="material-symbols-outlined text-primary mr-3 text-[20px]">database</span>
                    <div>
                      <div className="font-body-sm text-body-sm text-on-surface font-semibold">SUNAT Aduanet</div>
                      <div className="font-label-md text-label-md text-on-surface-variant mt-0.5">840K filas • Verificado (Núcleo)</div>
                    </div>
                  </div>
                  <span className="material-symbols-outlined text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity">chevron_right</span>
                </li>
                <li className="p-3 rounded-lg border border-transparent cursor-pointer flex items-center justify-between group hover:bg-white/5">
                  <div className="flex items-center">
                    <span className="material-symbols-outlined text-on-surface-variant mr-3 text-[20px]">bar_chart</span>
                    <div>
                      <div className="font-body-sm text-body-sm text-on-surface">Trade Map</div>
                      <div className="font-label-md text-label-md text-on-surface-variant mt-0.5">15K filas • Activo (Benchmark)</div>
                    </div>
                  </div>
                  <span className="material-symbols-outlined text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity">chevron_right</span>
                </li>
                <li className="p-3 rounded-lg border border-transparent cursor-pointer flex items-center justify-between group hover:bg-white/5">
                  <div className="flex items-center">
                    <span className="material-symbols-outlined text-on-surface-variant mr-3 text-[20px]">grass</span>
                    <div>
                      <div className="font-body-sm text-body-sm text-on-surface">SISAP / MIDAGRI</div>
                      <div className="font-label-md text-label-md text-on-surface-variant mt-0.5">120K filas • Sincronizado (Mercado Interno)</div>
                    </div>
                  </div>
                  <span className="material-symbols-outlined text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity">chevron_right</span>
                </li>
                <li className="p-3 rounded-lg border border-transparent cursor-pointer flex items-center justify-between group hover:bg-white/5">
                  <div className="flex items-center">
                    <span className="material-symbols-outlined text-on-surface-variant mr-3 text-[20px]">monetization_on</span>
                    <div>
                      <div className="font-body-sm text-body-sm text-on-surface">BCRP Macro Control</div>
                      <div className="font-label-md text-label-md text-on-surface-variant mt-0.5">2.4K filas • Diario (Tipo Cambio)</div>
                    </div>
                  </div>
                  <span className="material-symbols-outlined text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity">chevron_right</span>
                </li>
                <li className="p-3 rounded-lg border border-transparent cursor-pointer flex items-center justify-between group hover:bg-white/5">
                  <div className="flex items-center">
                    <span className="material-symbols-outlined text-on-surface-variant mr-3 text-[20px]">partly_cloudy_day</span>
                    <div>
                      <div className="font-body-sm text-body-sm text-on-surface">NASA Power / SENAMHI</div>
                      <div className="font-label-md text-label-md text-on-surface-variant mt-0.5">45K filas • Diario (Clima Proxy)</div>
                    </div>
                  </div>
                  <span className="material-symbols-outlined text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity">chevron_right</span>
                </li>
                <li className="p-3 rounded-lg border border-transparent cursor-pointer flex items-center justify-between group hover:bg-white/5">
                  <div className="flex items-center">
                    <span className="material-symbols-outlined text-on-surface-variant mr-3 text-[20px]">local_shipping</span>
                    <div>
                      <div className="font-body-sm text-body-sm text-on-surface">APN / OSITRAN Logística</div>
                      <div className="font-label-md text-label-md text-on-surface-variant mt-0.5">12K filas • Mensual (Logístico Proxy)</div>
                    </div>
                  </div>
                  <span className="material-symbols-outlined text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity">chevron_right</span>
                </li>
                <li className="p-3 rounded-lg border border-transparent cursor-pointer flex items-center justify-between group hover:bg-white/5">
                  <div className="flex items-center">
                    <span className="material-symbols-outlined text-on-surface-variant mr-3 text-[20px]">health_and_safety</span>
                    <div>
                      <div className="font-body-sm text-body-sm text-on-surface">FDA / SENASA Alertas</div>
                      <div className="font-label-md text-label-md text-on-surface-variant mt-0.5">8K filas • Semanal (Sanitario Proxy)</div>
                    </div>
                  </div>
                  <span className="material-symbols-outlined text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity">chevron_right</span>
                </li>
                <li className="p-3 rounded-lg border border-transparent cursor-pointer flex items-center justify-between group hover:bg-white/5">
                  <div className="flex items-center">
                    <span className="material-symbols-outlined text-on-surface-variant mr-3 text-[20px]">science</span>
                    <div>
                      <div className="font-body-sm text-body-sm text-on-surface">Dataset Sintético Auxiliar</div>
                      <div className="font-label-md text-label-md text-on-surface-variant mt-0.5">5K filas • Inactivo (Escenarios)</div>
                    </div>
                  </div>
                  <span className="material-symbols-outlined text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity">chevron_right</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Right Column: Data Preview */}
          <div className="lg:col-span-2 glass-panel rounded-xl p-6 flex flex-col h-[700px]">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
              <div>
                <h2 className="font-headline-sm text-headline-sm text-on-surface flex items-center font-semibold">
                  <span className="material-symbols-outlined text-primary mr-2">view_list</span>
                  Previsualización de Dataset Experimental
                </h2>
                <div className="flex items-center gap-2 mt-1">
                  <p className="font-body-sm text-body-sm text-on-surface-variant">Mostrando las primeras 20 filas de telemetría ingerida</p>
                  <span className="bg-primary/20 text-primary px-2 py-0.5 rounded-full text-[10px] font-bold font-mono-data">
                    {filteredData.length} de {realData.length}
                  </span>
                </div>
              </div>
              <div className="flex flex-wrap items-center gap-3">
                <select
                  value={selectedDeviationFilter}
                  onChange={(e) => setSelectedDeviationFilter(e.target.value)}
                  className="bg-surface-container-low border border-white/10 rounded-lg py-1 px-2.5 text-xs font-body-sm text-on-surface focus:border-primary focus:ring-1 focus:ring-primary focus:bg-white/5 transition-all"
                >
                  <option value="ALL">Todas las Desviaciones</option>
                  <option value="0-5%">Riesgo Bajo (0-5%)</option>
                  <option value="5-10%">Riesgo Moderado (5-10%)</option>
                  <option value="10-15%">Riesgo Alto (10-15%)</option>
                  <option value=">15%">Riesgo Crítico (&gt;15%)</option>
                </select>
                <a
                  className="bg-primary text-on-primary py-1 px-3 rounded-lg flex items-center gap-1 hover:bg-primary-fixed transition-colors font-label-md text-xs uppercase tracking-wider font-semibold shadow-[0_0_10px_rgba(118,219,143,0.2)]"
                  href="/api/alerts/export/csv"
                  download
                >
                  <span className="material-symbols-outlined text-[16px]">file_download</span>
                  CSV
                </a>
              </div>
            </div>
            
            {/* Table Container */}
            <div className="flex-grow overflow-auto border border-white/5 rounded-lg bg-surface-container-low/50 relative">
              <table className="w-full text-left border-collapse whitespace-nowrap">
                <thead className="sticky top-0 bg-surface-container-high/90 backdrop-blur-md z-10 font-label-md text-label-md text-on-surface-variant uppercase border-b border-white/10">
                  <tr>
                    <th className="px-4 py-3">RUC</th>
                    <th className="px-4 py-3">FOB (USD/PEN)</th>
                    <th className="px-4 py-3">Volumen (KG)</th>
                    <th className="px-4 py-3">Fecha</th>
                    <th className="px-4 py-3">Estado</th>
                  </tr>
                </thead>
                <tbody className="font-mono-data text-mono-data text-on-surface" id="preview-table-body">
                  {renderDataRows()}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* RAG Biblioteca de Normativas */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-card-gap mt-8">
          {/* Form to add */}
          <div className="lg:col-span-1 glass-panel rounded-xl p-6 flex flex-col">
            <h2 className="font-headline-sm text-headline-sm text-on-surface mb-4 font-semibold flex items-center gap-2">
              <span className="material-symbols-outlined text-primary">add_box</span>
              Indexar Nueva Directiva (RAG)
            </h2>
            <form onSubmit={handleAddDoc} className="space-y-4 flex-grow flex flex-col">
              <div>
                <label className="font-label-md text-label-md text-on-surface-variant block mb-1">Título de la Normativa</label>
                <input 
                  type="text"
                  value={docTitle}
                  onChange={(e) => setDocTitle(e.target.value)}
                  placeholder="Ej. FDA CFR Title 21 - Sección 5"
                  className="w-full bg-transparent border border-outline/50 rounded-lg p-2.5 text-body-sm font-body-sm text-on-surface placeholder:text-on-surface-variant/40 focus:border-primary focus:ring-1 focus:ring-primary focus:bg-white/5 transition-all"
                  required
                />
              </div>
              
              <div>
                <label className="font-label-md text-label-md text-on-surface-variant block mb-1">Categoría</label>
                <select 
                  value={docCategory}
                  onChange={(e) => setDocCategory(e.target.value)}
                  className="w-full bg-surface-container-low border border-outline/50 rounded-lg p-2.5 text-body-sm font-body-sm text-on-surface focus:border-primary focus:ring-1 focus:ring-primary focus:bg-white/5 transition-all"
                >
                  <option value="FDA">FDA (Estados Unidos)</option>
                  <option value="SENASA">SENASA (Perú)</option>
                  <option value="LEY_IA">Ley de IA (Transparencia)</option>
                  <option value="OTROS">Otros Reglamentos</option>
                </select>
              </div>
              
              <div className="flex-grow flex flex-col">
                <label className="font-label-md text-label-md text-on-surface-variant block mb-1">Contenido Normativo</label>
                <textarea 
                  value={docContent}
                  onChange={(e) => setDocContent(e.target.value)}
                  placeholder="Ingrese el cuerpo textual completo para la indexación y vectorización semántica en pgvector..."
                  rows="4"
                  className="w-full flex-grow bg-transparent border border-outline/50 rounded-lg p-2.5 text-body-sm font-body-sm text-on-surface placeholder:text-on-surface-variant/40 focus:border-primary focus:ring-1 focus:ring-primary focus:bg-white/5 transition-all resize-none min-h-[120px]"
                  required
                />
              </div>

              <button 
                type="submit" 
                disabled={savingDoc}
                className="w-full bg-primary text-on-primary font-label-md text-label-md py-2.5 px-4 rounded-lg hover:bg-primary-fixed transition-colors flex justify-center items-center gap-2 shadow-[0_0_15px_rgba(118,219,143,0.2)]"
              >
                {savingDoc ? (
                  <>
                    <span className="material-symbols-outlined text-[18px] animate-spin">sync</span>
                    Vectorizando...
                  </>
                ) : (
                  <>
                    <span className="material-symbols-outlined text-[18px]">psychology</span>
                    Indexar en PostgreSQL
                  </>
                )}
              </button>
            </form>
          </div>

          {/* List of indexed docs */}
          <div className="lg:col-span-2 glass-panel rounded-xl p-6 flex flex-col h-[480px]">
            <h2 className="font-headline-sm text-headline-sm text-on-surface mb-2 font-semibold flex items-center gap-2">
              <span className="material-symbols-outlined text-primary">library_books</span>
              Biblioteca Normativa Activa (Indexada en pgvector)
            </h2>
            <p className="font-body-sm text-body-sm text-on-surface-variant mb-4">Regulaciones almacenadas con embeddings vectoriales de 384 dimensiones.</p>
            
            <div className="flex-grow overflow-auto border border-white/5 rounded-lg bg-surface-container-low/50 relative">
              {loadingDocs ? (
                <div className="flex items-center justify-center h-full">
                  <span className="material-symbols-outlined text-primary text-3xl animate-spin mr-2">sync</span>
                  <span className="text-on-surface-variant font-medium">Cargando biblioteca...</span>
                </div>
              ) : (
                <table className="w-full text-left border-collapse whitespace-nowrap">
                  <thead className="sticky top-0 bg-surface-container-high/90 backdrop-blur-md z-10 font-label-md text-label-md text-on-surface-variant uppercase border-b border-white/10">
                    <tr>
                      <th className="px-4 py-2.5">Título / Documento</th>
                      <th className="px-4 py-2.5">Categoría</th>
                      <th className="px-4 py-2.5">Cita Corta</th>
                      <th className="px-4 py-2.5">Estado Vectorial</th>
                    </tr>
                  </thead>
                  <tbody className="font-body-sm text-on-surface">
                    {ragDocs.map((doc, idx) => (
                      <tr key={doc.id_doc || idx} className={`border-b border-white/5 hover:bg-white/5 transition-colors ${idx % 2 === 0 ? 'bg-white/[0.02]' : ''}`}>
                        <td className="px-4 py-3 max-w-[280px] truncate" title={doc.titulo}>
                          <span className="font-medium text-on-surface block">{doc.titulo}</span>
                          <span className="text-[11px] text-on-surface-variant block truncate mt-0.5">{doc.contenido}</span>
                        </td>
                        <td className="px-4 py-3">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            doc.categoria === 'FDA' ? 'bg-blue-500/20 text-blue-300' :
                            doc.categoria === 'SENASA' ? 'bg-emerald-500/20 text-emerald-300' :
                            doc.categoria === 'LEY_IA' ? 'bg-purple-500/20 text-purple-300' :
                            'bg-yellow-500/20 text-yellow-300'
                          }`}>
                            {doc.categoria}
                          </span>
                        </td>
                        <td className="px-4 py-3 font-mono-data text-[12px] text-primary">
                          [{doc.categoria}-{doc.id_doc}]
                        </td>
                        <td className="px-4 py-3 text-on-surface-variant text-[11px]">
                          <span className="flex items-center gap-1.5 text-primary">
                            <span className="flex h-2 w-2 rounded-full bg-primary shadow-[0_0_6px_#76db8f]"></span>
                            Activo (384-dim)
                          </span>
                        </td>
                      </tr>
                    ))}
                    {ragDocs.length === 0 && (
                      <tr>
                        <td colSpan="4" className="px-4 py-8 text-center text-on-surface-variant">No hay directivas normativas indexadas en pgvector.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}
