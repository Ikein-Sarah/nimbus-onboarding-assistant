import { MoonIcon, SunIcon } from './Icons'

export default function ThemeSwitch({ theme, onChange }) {
  return (
    <div className="mode" role="group" aria-label="Theme">
      <button className={theme === 'light' ? 'on' : undefined} aria-pressed={theme === 'light'}
        onClick={() => onChange('light')}>
        <SunIcon />Light
      </button>
      <button className={theme === 'dark' ? 'on' : undefined} aria-pressed={theme === 'dark'}
        onClick={() => onChange('dark')}>
        <MoonIcon />Dark
      </button>
    </div>
  )
}
