import { useCallback, useEffect, useRef, useState } from 'react'
import { AuthError, LimitError, request } from './api'
import ChatButton from './components/ChatButton'
import ChatPanel from './components/ChatPanel'
import Sidebar from './components/Sidebar'
import TopBar from './components/TopBar'
import { greeting, longToday } from './dates'
import Checklist from './pages/Checklist'
import Feedback from './pages/Feedback'
import Goals from './pages/Goals'
import Home from './pages/Home'
import { usePage } from './router'
import { useTheme } from './theme'

// Wait this long after the last tick before refreshing, so ticking several
// items in a row asks for one new AI summary instead of one each.
const REFRESH_DELAY_MS = 1000

// Counts for the stat cards, worked out locally so they move as soon as you tick.
function withStats(data) {
  const phaseGoals = data.goals.filter((g) => g.phase === data.stats.current_phase)
  return {
    ...data,
    stats: {
      ...data.stats,
      goals_done: phaseGoals.filter((g) => g.status === 'done').length,
      checklist_done: data.checklist.filter((c) => c.done).length,
    },
  }
}

export default function Shell({ user, onLogout }) {
  const page = usePage()
  const [theme, setTheme] = useTheme()
  const [data, setData] = useState(null)
  const [loadError, setLoadError] = useState('')
  const [chatOpen, setChatOpen] = useState(false)
  const [messages, setMessages] = useState([])
  const [busy, setBusy] = useState(false)

  // Bumped on every local change, so a refresh that started before the
  // latest tick can't overwrite it with older data.
  const version = useRef(0)
  const refreshTimer = useRef(null)

  const fail = useCallback((err) => {
    if (err instanceof AuthError) onLogout()
    else setLoadError(err.message)
  }, [onLogout])

  const load = useCallback(() => {
    const started = version.current
    return request('/dashboard')
      .then((fresh) => {
        if (version.current === started) setData(fresh)
        setLoadError('')
      })
      .catch(fail)
  }, [fail])

  useEffect(() => {
    load()
    return () => clearTimeout(refreshTimer.current)
  }, [load])

  function change(update, path, body) {
    version.current += 1
    setData((d) => withStats(update(d)))
    clearTimeout(refreshTimer.current)
    request(path, { method: 'POST', body })
      .then(() => { refreshTimer.current = setTimeout(load, REFRESH_DELAY_MS) })
      .catch((err) => {
        fail(err)
        version.current += 1
        load() // put back what the server actually has
      })
  }

  function toggleItem(id) {
    change(
      (d) => ({ ...d, checklist: d.checklist.map((c) => (c.id === id ? { ...c, done: !c.done } : c)) }),
      `/checklist/${id}/toggle`,
    )
  }

  function setGoalStatus(id, status) {
    change(
      (d) => ({ ...d, goals: d.goals.map((g) => (g.id === id ? { ...g, status } : g)) }),
      `/goals/${id}/status`,
      { status },
    )
  }

  async function ask(question) {
    setBusy(true)
    setMessages((m) => [...m, { role: 'user', text: question }])
    try {
      const result = await request('/ask', { method: 'POST', body: { question } })
      setMessages((m) => [...m, { role: 'bot', text: result.answer, sources: result.sources }])
    } catch (err) {
      if (err instanceof AuthError) return onLogout()
      const text = err instanceof LimitError ? err.message : `Sorry, something went wrong: ${err.message}`
      setMessages((m) => [...m, { role: 'bot', text }])
    } finally {
      setBusy(false)
    }
  }

  const closeChat = useCallback(() => setChatOpen(false), [])

  const firstName = user.name.split(' ')[0]
  const manager = data?.profile.manager?.name.split(' ')[0]
  const titles = {
    home: [`${greeting()}, ${firstName}`, `${longToday()} · here's your week at a glance`],
    goals: ['My goals', manager ? `Your 30-60-90 day plan, set with ${manager}.` : 'Your 30-60-90 day plan.'],
    checklist: ['Onboarding checklist', 'Tick things off as you go.'],
    feedback: ['Feedback', 'Notes from your manager.'],
  }
  const [title, lead] = titles[page]

  let content
  if (!data) {
    content = <p className="muted" style={{ marginTop: 24 }}>{loadError || 'Loading your week…'}</p>
  } else if (page === 'goals') {
    content = <Goals data={data} onStatus={setGoalStatus} />
  } else if (page === 'checklist') {
    content = <Checklist data={data} onToggle={toggleItem} />
  } else if (page === 'feedback') {
    content = <Feedback data={data} />
  } else {
    content = <Home data={data} />
  }

  return (
    <div className={chatOpen ? 'chat-open' : undefined}>
      <div className="app">
        <Sidebar page={page} />
        <main className="main">
          <TopBar title={title} lead={lead} theme={theme} onTheme={setTheme} user={user} onLogout={onLogout} />
          {data && loadError && <p className="error" role="alert">{loadError}</p>}
          {content}
        </main>
      </div>

      {chatOpen ? (
        <ChatPanel firstName={firstName} messages={messages} busy={busy} onAsk={ask} onClose={closeChat} />
      ) : (
        <ChatButton onClick={() => setChatOpen(true)} />
      )}
    </div>
  )
}
