import { useEffect, useState } from 'react'

export const PAGES = ['home', 'goals', 'checklist', 'feedback']

function pageFromHash() {
  const page = window.location.hash.replace(/^#\/?/, '')
  return PAGES.includes(page) ? page : 'home'
}

// Each page has its own URL (#/goals), so refresh and the back button work.
export function usePage() {
  const [page, setPage] = useState(pageFromHash)

  useEffect(() => {
    const onChange = () => {
      setPage(pageFromHash())
      window.scrollTo(0, 0)
    }
    window.addEventListener('hashchange', onChange)
    return () => window.removeEventListener('hashchange', onChange)
  }, [])

  return page
}

export function href(page) {
  return `#/${page}`
}
