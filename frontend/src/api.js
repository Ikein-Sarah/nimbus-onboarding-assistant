const TOKEN_KEY = 'nimbus_token'

export function getToken() {
  return sessionStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  if (token) sessionStorage.setItem(TOKEN_KEY, token)
  else sessionStorage.removeItem(TOKEN_KEY)
}

export class AuthError extends Error {}

export async function request(path, { method = 'GET', body } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`

  const response = await fetch(`/api${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })

  const data = await response.json().catch(() => ({}))
  if (response.status === 401) throw new AuthError(data.detail || 'Please log in again')
  if (!response.ok) {
    const detail = typeof data.detail === 'string' ? data.detail : 'Something went wrong'
    throw new Error(detail)
  }
  return data
}
