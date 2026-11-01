export async function researchApi(path, token, options = {}) {
  if (!token) throw new Error('Inicie sesión para consultar el backend de investigación.')
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), 70000)
  try {
    const response = await fetch(`/api/research/${path}`, {
      ...options, signal: controller.signal,
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}`, ...options.headers },
    })
    const body = await response.json()
    if (!response.ok) {
      if (response.status === 401) throw new Error('La sesión no es válida para este backend. Cierre sesión e ingrese nuevamente.')
      throw new Error(body.detail?.message || (typeof body.detail === 'string' ? body.detail : 'La operación no pudo completarse.'))
    }
    return body
  } catch (error) {
    if (error.name === 'AbortError') throw new Error('La operación superó el tiempo de espera. No se completó la verificación.')
    throw error
  } finally { clearTimeout(timer) }
}
