import { duePill, PHASE_NAMES } from '../dates'
import { href } from '../router'

export default function UpNextCard({ items }) {
  return (
    <div className="card">
      <h3>Up next <a href={href('goals')}>View all goals</a></h3>
      {items.length === 0 ? (
        <p className="muted" style={{ marginTop: 12 }}>You're all caught up.</p>
      ) : (
        <ul className="next">
          {items.map((item) => {
            const pill = duePill(item.due_date, item.status === 'in_progress')
            const kind = item.kind === 'goal' ? `Goal · ${PHASE_NAMES[item.phase].toLowerCase()}` : 'Checklist'
            return (
              <li key={`${item.kind}-${item.id}`}>
                <div className="t">{item.title}<small>{kind}</small></div>
                {pill && <span className={`pill${pill.urgent ? ' due' : ''}`}>{pill.text}</span>}
              </li>
            )
          })}
        </ul>
      )}
    </div>
  )
}
