import { useEffect, useRef, useState } from 'react'

// "data/general/leave-policy.md" -> "leave-policy.md"
const fileName = (path) => path.split('/').pop()

// The Ask Nimbus side panel. Messages live in the parent, so they survive
// closing and reopening the panel.
export default function ChatPanel({ firstName, messages, busy, onAsk, onClose }) {
  const [question, setQuestion] = useState('')
  const endRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    inputRef.current?.focus()
    const onKey = (event) => event.key === 'Escape' && onClose()
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [onClose])

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages, busy])

  function submit(event) {
    event.preventDefault()
    const q = question.trim()
    if (!q || busy) return
    setQuestion('')
    onAsk(q)
  }

  return (
    <aside className="chat" aria-label="Ask Nimbus">
      <div className="hd">
        <div className="av">N</div>
        <div><b>Ask Nimbus</b><small>Answers from documents you can see</small></div>
        <button onClick={onClose} aria-label="Close chat">×</button>
      </div>
      <div className="msgs" aria-live="polite">
        <div className="m bot">Hi {firstName}! Ask me anything about working at Nimbus.</div>
        {messages.map((message, i) => (
          <div key={i} className={`m ${message.role === 'user' ? 'you' : 'bot'}`}>
            {message.text}
            {message.sources?.length > 0 && (
              <>
                <br />
                <span className="src">Source: {message.sources.map(fileName).join(', ')}</span>
              </>
            )}
          </div>
        ))}
        {busy && <div className="m bot wait">Searching your documents…</div>}
        <div ref={endRef} />
      </div>
      <form className="in" onSubmit={submit}>
        <input ref={inputRef} value={question} onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your question..." maxLength={1000} aria-label="Your question" />
        <button type="submit" disabled={busy || !question.trim()}>Send</button>
      </form>
    </aside>
  )
}
