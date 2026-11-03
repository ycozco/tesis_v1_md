export async function loadResearchSnapshot(url, signal, fetcher = fetch) {
  for (let attempt = 0; attempt < 2; attempt++) {
    let response
    try {
      response = await fetcher(url, { signal, cache: 'no-store' })
    } catch (error) {
      if (signal?.aborted || error.name === 'AbortError') throw error
      if (attempt === 0) continue
      throw new Error('No se pudo conectar con el servidor local.')
    }
    if (!response.ok) {
      if (response.status >= 500 && attempt === 0) continue
      throw new Error(`El archivo de datos respondió HTTP ${response.status}.`)
    }
    let snapshot
    try { snapshot = await response.json() } catch {
      throw new Error('El archivo recibido no contiene JSON válido.')
    }
    if (snapshot?.schema_version !== 1 || !Array.isArray(snapshot.weekly_rows) ||
        !snapshot.manifest?.views?.conservadora || !Array.isArray(snapshot.signals) ||
        !Array.isArray(snapshot.paired_metrics)) {
      throw new Error('El archivo de datos tiene una estructura incompatible.')
    }
    return snapshot
  }
}
