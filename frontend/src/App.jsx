import { useEffect, useState } from 'react'
import { getToken, request, setToken } from './api'
import Login from './pages/Login'
import Shell from './Shell'

export default function App() {
  const [user, setUser] = useState(null)
  const [checking, setChecking] = useState(Boolean(getToken()))

  // On reload, ask the server who the stored token belongs to.
  useEffect(() => {
    if (!getToken()) return
    request('/me')
      .then(setUser)
      .catch(() => setToken(null))
      .finally(() => setChecking(false))
  }, [])

  function logout() {
    setToken(null)
    setUser(null)
  }

  if (checking) return null
  if (!user) return <Login onLogin={setUser} />
  return <Shell user={user} onLogout={logout} />
}
