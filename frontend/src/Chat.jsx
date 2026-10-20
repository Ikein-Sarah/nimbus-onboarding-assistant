import { useEffect, useRef, useState } from 'react'
import { AuthError, request } from './api'
import { BRAND_GRADIENT, colorFor, folderOf } from './colors'
import { DepartmentBadge, Logo } from './theme'

const ROUTES = [
  { id: 'vector', label: 'Vector search' },
  { id: 'file_agent', label: 'File agent' },
]

const EXAMPLES = [
  { emoji: '🌴', text: 'How many days of annual leave do I get?', card: 'bg-teal-50 ring-teal-200 hover:bg-teal-100' },
  { emoji: '✈️', text: 'Can I work from another country?', card: 'bg-violet-50 ring-violet-200 hover:bg-violet-100' },
  { emoji: '🗓️', text: 'What should I do in my first week?', card: 'bg-orange-50 ring-orange-200 hover:bg-orange-100' },
  { emoji: '💰', text: 'What are the salary bands?', card: 'bg-pink-50 ring-pink-200 hover:bg-pink-100' },
]

export default function Chat({ user, onLogout }) {
  const [messages, setMessages] = useState([])
  const [question, setQuestion] = useState('')
  const [route, setRoute] = useState('vector')
  const [busy, setBusy] = useState(false)
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, busy])

  async function ask(text) {
    const q = text.trim()
    if (!q || busy) return
    setQuestion('')
    setBusy(true)
    setMessages((m) => [...m, { role: 'user', text: q }])
    try {
      const data = await request('/ask', { method: 'POST', body: { question: q, route } })
      setMessages((m) => [...m, { role: 'assistant', ...data }])
    } catch (err) {
      if (err instanceof AuthError) return onLogout()
      setMessages((m) => [...m, { role: 'error', text: err.message }])
    } finally {
      setBusy(false)
    }
  }

  function onKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      ask(question)
    }
  }

  const firstName = user.name.split(' ')[0]

  return (
    <div className="flex h-dvh flex-col bg-slate-50">
      <header className={`${BRAND_GRADIENT} shadow-md`}>
        <div className="mx-auto flex max-w-3xl items-center justify-between gap-3 px-4 py-3">
          <div className="flex items-center gap-2.5 text-white">
            <Logo />
            <span className="text-lg font-bold tracking-tight">Nimbus</span>
          </div>
          <div className="flex min-w-0 items-center gap-2.5">
            <span className="hidden truncate text-sm font-medium text-white sm:inline">{user.name}</span>
            <DepartmentBadge department={user.department} />
            <button
              onClick={onLogout}
              className="rounded-lg bg-white/15 px-3 py-1.5 text-sm font-medium text-white ring-1 ring-white/30 transition hover:bg-white/25"
            >
              Log out
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-3xl space-y-5 px-4 py-6">
          {messages.length === 0 && (
            <div className="pt-6 sm:pt-12">
              <h1 className="text-3xl font-bold tracking-tight text-slate-900">Hi {firstName} 👋</h1>
              <p className="mt-2 text-slate-600">
                Ask me anything about how Nimbus Labs works. I only answer from documents you can see.
              </p>
              <div className="mt-8 grid grid-cols-1 gap-3 sm:grid-cols-2">
                {EXAMPLES.map((example) => (
                  <button
                    key={example.text}
                    onClick={() => ask(example.text)}
                    className={`flex items-start gap-3 rounded-2xl p-4 text-left ring-1 ring-inset transition hover:-translate-y-0.5 hover:shadow-md ${example.card}`}
                  >
                    <span className="text-2xl leading-none" aria-hidden="true">{example.emoji}</span>
                    <span className="font-medium text-slate-800">{example.text}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((message, i) => <Message key={i} message={message} />)}

          {busy && (
            <div className="flex items-center gap-3">
              <Avatar />
              <div className="flex items-center gap-1.5 rounded-2xl bg-white px-4 py-3.5 shadow-sm ring-1 ring-slate-200">
                <Dot delay="0ms" /><Dot delay="150ms" /><Dot delay="300ms" />
                <span className="ml-2 text-sm text-slate-500">
                  {route === 'file_agent' ? 'Searching the folders…' : 'Searching…'}
                </span>
              </div>
            </div>
          )}
          <div ref={endRef} />
        </div>
      </main>

      <footer className="border-t border-slate-200 bg-white/90 backdrop-blur">
        <div className="mx-auto max-w-3xl px-4 pb-[max(0.75rem,env(safe-area-inset-bottom))] pt-3">
          <div className="mb-2.5 inline-flex rounded-xl bg-slate-100 p-1" role="radiogroup" aria-label="Retrieval route">
            {ROUTES.map((r) => (
              <button
                key={r.id}
                role="radio"
                aria-checked={route === r.id}
                onClick={() => setRoute(r.id)}
                className={`rounded-lg px-3 py-1 text-sm font-medium transition ${
                  route === r.id ? 'bg-white text-violet-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {r.label}
              </button>
            ))}
          </div>
          <form onSubmit={(e) => { e.preventDefault(); ask(question) }} className="flex items-end gap-2">
            <textarea
              rows={1}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={onKeyDown}
              maxLength={1000}
              placeholder="Ask a question…"
              className="max-h-40 min-h-12 flex-1 resize-none rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 outline-none transition focus:border-violet-500 focus:bg-white focus:ring-4 focus:ring-violet-100"
            />
            <button
              type="submit"
              disabled={busy || !question.trim()}
              aria-label="Ask"
              className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl text-white shadow-lg shadow-violet-700/25 transition hover:brightness-110 disabled:opacity-40 disabled:shadow-none ${BRAND_GRADIENT}`}
            >
              <svg viewBox="0 0 20 20" fill="currentColor" className="h-5 w-5" aria-hidden="true">
                <path d="M3.1 2.3a.75.75 0 0 0-.9 1l2.4 6.7-2.4 6.7a.75.75 0 0 0 .9 1l14.5-7a.75.75 0 0 0 0-1.4l-14.5-7Z" />
              </svg>
            </button>
          </form>
        </div>
      </footer>
    </div>
  )
}

function Dot({ delay }) {
  return <span className="h-2 w-2 animate-bounce rounded-full bg-violet-500" style={{ animationDelay: delay }} />
}

function Avatar() {
  return (
    <div className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-xl text-sm font-bold text-white ${BRAND_GRADIENT}`}>
      N
    </div>
  )
}

function Message({ message }) {
  if (message.role === 'user') {
    return (
      <div className="flex justify-end">
        <div className={`max-w-[85%] whitespace-pre-wrap rounded-3xl rounded-br-lg px-4 py-2.5 text-white shadow-md shadow-violet-700/20 ${BRAND_GRADIENT}`}>
          {message.text}
        </div>
      </div>
    )
  }

  if (message.role === 'error') {
    return <div className="rounded-2xl bg-red-50 px-4 py-3 text-sm text-red-700 ring-1 ring-red-200">{message.text}</div>
  }

  const routeLabel = ROUTES.find((r) => r.id === message.route)?.label
  return (
    <div className="flex items-start gap-3">
      <Avatar />
      <div className="min-w-0 flex-1 rounded-3xl rounded-tl-lg bg-white px-5 py-4 shadow-sm ring-1 ring-slate-200">
        <p className="whitespace-pre-wrap leading-relaxed text-slate-800">{message.answer}</p>
        {message.sources.length > 0 && (
          <ul className="mt-4 flex flex-wrap gap-1.5">
            {message.sources.map((source) => (
              <li
                key={source}
                className={`break-all rounded-full px-2.5 py-0.5 font-mono text-xs ring-1 ring-inset ${colorFor(folderOf(source))}`}
              >
                {source.replace(/^data\//, '')}
              </li>
            ))}
          </ul>
        )}
        <div className="mt-3 text-xs text-slate-500">
          {routeLabel} · {message.seconds}s
        </div>
      </div>
    </div>
  )
}
