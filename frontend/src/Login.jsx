import { useState } from 'react'
import { request, setToken } from './api'
import { Logo } from './theme'

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
    <main className="relative flex min-h-dvh items-center justify-center overflow-hidden bg-linear-to-br from-indigo-700 via-violet-700 to-teal-600 px-4 py-12">
      {/* Soft glow shapes behind the card. */}
      <div className="pointer-events-none absolute -left-24 -top-24 h-80 w-80 rounded-full bg-fuchsia-400/30 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-32 -right-16 h-96 w-96 rounded-full bg-teal-300/30 blur-3xl" />

      <div className="relative w-full max-w-sm">
        <div className="mb-8 flex flex-col items-center text-center text-white">
          <Logo className="h-14 w-14 text-2xl" />
          <h1 className="mt-4 text-3xl font-bold tracking-tight">Nimbus</h1>
          <p className="mt-1 text-white/85">Your onboarding assistant</p>
        </div>

        <form onSubmit={submit} className="rounded-3xl bg-white p-7 shadow-2xl shadow-indigo-950/30">
          <h2 className="text-lg font-semibold text-slate-900">Sign in</h2>
          <p className="mt-1 text-sm text-slate-500">Use your Nimbus Labs account.</p>

          <label className="mt-6 block text-sm font-medium text-slate-700" htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            autoComplete="username"
            placeholder="you@nimbuslabs.io"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2.5 outline-none transition focus:border-violet-500 focus:bg-white focus:ring-4 focus:ring-violet-100"
          />

          <label className="mt-4 block text-sm font-medium text-slate-700" htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            autoComplete="current-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2.5 outline-none transition focus:border-violet-500 focus:bg-white focus:ring-4 focus:ring-violet-100"
          />

          {error && <p className="mt-4 rounded-xl bg-red-50 px-3.5 py-2.5 text-sm text-red-700">{error}</p>}

          <button
            type="submit"
            disabled={busy}
            className="mt-6 w-full rounded-xl bg-linear-to-r from-indigo-700 via-violet-700 to-teal-700 py-3 font-semibold text-white shadow-lg shadow-violet-700/25 transition hover:brightness-110 disabled:opacity-60"
          >
            {busy ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-white/80">
          You only see documents your role allows.
        </p>
      </div>
    </main>
  )
}
