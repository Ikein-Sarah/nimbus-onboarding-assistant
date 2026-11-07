import { useEffect, useRef, useState } from 'react'

// The round initial in the top right. Opens a small menu with sign out.
export default function UserMenu({ user, onLogout }) {
  const [open, setOpen] = useState(false)
  const ref = useRef(null)

  useEffect(() => {
    if (!open) return
    const close = (event) => {
      if (event.type === 'keydown' ? event.key === 'Escape' : !ref.current?.contains(event.target)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', close)
    document.addEventListener('keydown', close)
    return () => {
      document.removeEventListener('mousedown', close)
      document.removeEventListener('keydown', close)
    }
  }, [open])

  return (
    <div ref={ref}>
      <button className="av" aria-label="Account" aria-expanded={open} onClick={() => setOpen(!open)}>
        {user.name[0].toUpperCase()}
      </button>
      {open && (
        <div className="card menu">
          <b>{user.name}</b>
          <small>{user.email}</small>
          <button onClick={onLogout}>Sign out</button>
        </div>
      )}
    </div>
  )
}
