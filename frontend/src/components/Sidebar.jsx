import { href } from '../router'
import { ChecklistIcon, FeedbackIcon, GoalsIcon, HomeIcon } from './Icons'

const LINKS = [
  { page: 'home', label: 'Home', Icon: HomeIcon },
  { page: 'goals', label: 'My goals', Icon: GoalsIcon },
  { page: 'checklist', label: 'Checklist', Icon: ChecklistIcon },
  { page: 'feedback', label: 'Feedback', Icon: FeedbackIcon },
]

export default function Sidebar({ page }) {
  return (
    <aside className="side">
      <div className="logo"><i />Nimbus</div>
      <nav aria-label="Main">
        {LINKS.map(({ page: p, label, Icon }) => (
          <a key={p} href={href(p)} className={page === p ? 'on' : undefined}
            aria-current={page === p ? 'page' : undefined}>
            <Icon />{label}
          </a>
        ))}
      </nav>
    </aside>
  )
}
