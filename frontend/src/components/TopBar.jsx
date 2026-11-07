import ThemeSwitch from './ThemeSwitch'
import UserMenu from './UserMenu'

export default function TopBar({ title, lead, theme, onTheme, user, onLogout }) {
  return (
    <div className="topbar">
      <div>
        <h1>{title}</h1>
        <p className="lead">{lead}</p>
      </div>
      <div className="tools">
        <ThemeSwitch theme={theme} onChange={onTheme} />
        <UserMenu user={user} onLogout={onLogout} />
      </div>
    </div>
  )
}
