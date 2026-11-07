import { useState } from 'react'
import { request, setToken } from '../api'

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError('')
    try {
      const data = await request('/login', { method: 'POST', body: { email, password } })
      setToken(data.access_token)
      onLogin(data.user)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="login">
      <div className="brand">
        <div className="logo"><i />Nimbus</div>
        <div>
          <h1>Everything you need for your first 90 days.</h1>
          <p>Your goals, your onboarding steps, and answers about how things work here, all in one place.</p>
        </div>
        <small>Nimbus Labs</small>
      </div>
      <form onSubmit={submit}>
        <h2>Welcome back</h2>
        <p className="sub">Sign in with your work email.</p>
        <label htmlFor="email">Work email</label>
        <input id="email" type="email" autoComplete="username" placeholder="you@nimbuslabs.io"
          required value={email} onChange={(e) => setEmail(e.target.value)} />
        <label htmlFor="password">Password</label>
        <input id="password" type="password" autoComplete="current-password" placeholder="••••••••"
          required value={password} onChange={(e) => setPassword(e.target.value)} />
        {error && <p className="error" role="alert">{error}</p>}
        <button className="btn" type="submit" disabled={busy}>{busy ? 'Signing in…' : 'Sign in'}</button>
        <p className="note">New here? Your HR team will send you an invite.</p>
      </form>
    </div>
  )
}
