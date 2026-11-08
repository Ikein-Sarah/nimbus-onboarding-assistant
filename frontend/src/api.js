const TOKEN_KEY = 'nimbus_token'

// The hosted site calls the API at VITE_API_URL. Locally it is unset, and
// /api goes through the Vite dev proxy to the FastAPI server.
const API_URL = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '')

export const LIMIT_MESSAGE = 'This demo has a daily question limit. Please try again tomorrow.'

export function getToken() {
  return sessionStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  if (token) sessionStorage.setItem(TOKEN_KEY, token)
  else sessionStorage.removeItem(TOKEN_KEY)
}

export class AuthError extends Error {}
export class LimitError extends Error {}

export async function request(path, { method = 'GET', body } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`

  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })

  const data = await response.json().catch(() => ({}))
  if (response.status === 401) throw new AuthError(data.detail || 'Please log in again')
  if (response.status === 429) throw new LimitError(LIMIT_MESSAGE)
  if (!response.ok) {
    const detail = typeof data.detail === 'string' ? data.detail : 'Something went wrong'
    throw new Error(detail)
  }
  return data
}
