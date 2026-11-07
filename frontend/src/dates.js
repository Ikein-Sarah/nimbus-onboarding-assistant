// Dates from the API are "YYYY-MM-DD". Parse them as local dates, not UTC,
// so they don't shift by a day.
export function parseDate(value) {
  const [y, m, d] = value.split('-').map(Number)
  return new Date(y, m - 1, d)
}

function today() {
  const now = new Date()
  return new Date(now.getFullYear(), now.getMonth(), now.getDate())
}

export function daysFromToday(value) {
  return Math.round((parseDate(value) - today()) / 86400000)
}

export function weekday(value) {
  return parseDate(value).toLocaleDateString('en-GB', { weekday: 'long' })
}

// "26 Oct 2026"
export function shortDate(value) {
  return parseDate(value).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
}

// "Saturday, 7 November"
export function longToday() {
  const now = new Date()
  const day = now.toLocaleDateString('en-GB', { weekday: 'long' })
  return `${day}, ${now.toLocaleDateString('en-GB', { day: 'numeric', month: 'long' })}`
}

export function greeting() {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 18) return 'Good afternoon'
  return 'Good evening'
}

// "today", "yesterday", "2 days ago"
export function ago(value) {
  const days = -daysFromToday(value)
  if (days <= 0) return 'today'
  if (days === 1) return 'yesterday'
  return `${days} days ago`
}

// "Friday", "tomorrow", "12 Dec", for "due ..." text.
export function dueWhen(value) {
  const days = daysFromToday(value)
  if (days < 0) return 'overdue'
  if (days === 0) return 'today'
  if (days === 1) return 'tomorrow'
  if (days < 7) return weekday(value)
  return parseDate(value).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })
}

// The pill on an "Up next" item: { text, urgent }.
export function duePill(value, inProgress) {
  if (!value) return null
  const days = daysFromToday(value)
  if (days < 0) return { text: 'Overdue', urgent: true }
  if (days <= 2 || (inProgress && days < 7)) return { text: `Due ${dueWhen(value)}`, urgent: true }
  if (days < 7) return { text: 'This week', urgent: false }
  if (days < 14) return { text: 'Next week', urgent: false }
  return { text: `Due ${dueWhen(value)}`, urgent: false }
}

export const PHASE_NAMES = { 30: 'First 30 days', 60: 'Days 31-60', 90: 'Days 61-90' }
