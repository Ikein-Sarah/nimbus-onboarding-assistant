// Line icons from the design file. They take their colour from the text.
function Icon({ children, strokeWidth = 2 }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={strokeWidth}
      strokeLinejoin="round" aria-hidden="true">
      {children}
    </svg>
  )
}

export const HomeIcon = () => <Icon><path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z" /></Icon>
export const GoalsIcon = () => <Icon><circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="5" /><circle cx="12" cy="12" r="1.5" /></Icon>
export const ChecklistIcon = () => <Icon><path d="M4 6h3M4 12h3M4 18h3M10 6h10M10 12h10M10 18h10" /></Icon>
export const FeedbackIcon = () => <Icon><path d="M4 5h16v11H9l-5 4z" /></Icon>
export const CalendarIcon = () => <Icon><rect x="3" y="5" width="18" height="16" rx="2" /><path d="M3 10h18M8 3v4M16 3v4" /></Icon>
export const TargetIcon = () => <Icon><circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="4" /></Icon>
export const TickIcon = () => <Icon><path d="M5 12l4 4L19 6" /></Icon>
export const SunIcon = () => <Icon><circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" /></Icon>
export const MoonIcon = () => <Icon><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z" /></Icon>
export const ChatIcon = () => <Icon strokeWidth={2.2}><path d="M4 5h16v11H9l-5 4z" /></Icon>
