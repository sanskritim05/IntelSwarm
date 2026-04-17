const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function startResearch(company) {
  const response = await fetch(`${API_BASE}/research`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ company }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || 'Unable to start research job.')
  }

  return response.json()
}

export function streamResearch(jobId, handlers) {
  const source = new EventSource(`${API_BASE}/research/${jobId}/stream`)

  source.onmessage = (event) => {
    const payload = JSON.parse(event.data)
    handlers.onEvent?.(payload)
    if (payload.status === 'done') {
      handlers.onDone?.(payload)
      source.close()
    }
    if (payload.status === 'error') {
      handlers.onError?.(new Error(payload.message || 'Research failed.'))
      source.close()
    }
  }

  source.onerror = () => {
    handlers.onError?.(new Error('Streaming connection failed.'))
    source.close()
  }

  return () => source.close()
}

export async function fetchReports() {
  const response = await fetch(`${API_BASE}/reports`)
  if (!response.ok) {
    throw new Error('Unable to load saved reports.')
  }
  return response.json()
}

export async function fetchReport(filename) {
  const response = await fetch(`${API_BASE}/reports/${filename}`)
  if (!response.ok) {
    throw new Error('Unable to load report.')
  }
  return response.text()
}

