import { useEffect, useState } from 'react'

const THEME_KEY = 'nimbus_theme'

function savedTheme() {
  try {
    return localStorage.getItem(THEME_KEY) === 'light' ? 'light' : 'dark'
  } catch {
    return 'dark'
  }
}

// Light or dark, remembered in this browser. index.html applies it before
// React loads; this keeps it in sync after that.
export function useTheme() {
  const [theme, setTheme] = useState(savedTheme)

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    try {
      localStorage.setItem(THEME_KEY, theme)
    } catch {
      // Private mode or blocked storage: the switch still works for this visit.
    }
  }, [theme])

  return [theme, setTheme]
}
