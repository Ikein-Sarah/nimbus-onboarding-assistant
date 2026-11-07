import { dueWhen, PHASE_NAMES } from '../dates'

const NEXT_STATUS = { not_started: 'in_progress', in_progress: 'done', done: 'not_started' }
const STATUS_TEXT = { not_started: 'Not started', in_progress: 'In progress', done: 'Done' }
const STATUS_CLASS = { not_started: '', in_progress: ' mid', done: ' ok' }

function badge(phase, current) {
  if (phase === current) return <em>Now</em>
  if (phase < current) return <em className="later">Earlier</em>
  return <em className="later">{phase - current === 30 ? 'Next' : 'Later'}</em>
}

// One 30/60/90 column. Clicking a goal moves it on: not started, in progress, done.
export default function PhaseCard({ phase, currentPhase, goals, onStatus }) {
  return (
    <div className={`card ph${phase === currentPhase ? ' now' : ''}`}>
      <h3>{PHASE_NAMES[phase]} {badge(phase, currentPhase)}</h3>
      {goals.map((goal) => {
        let detail = STATUS_TEXT[goal.status]
        if (goal.status === 'in_progress' && goal.due_date) detail += ` · due ${dueWhen(goal.due_date)}`
        return (
          <button key={goal.id} className={`goal${STATUS_CLASS[goal.status]}`}
            onClick={() => onStatus(goal.id, NEXT_STATUS[goal.status])}
            title={`Mark as ${STATUS_TEXT[NEXT_STATUS[goal.status]].toLowerCase()}`}>
            <div className="dot" />
            <div>{goal.title}<small>{detail}</small></div>
          </button>
        )
      })}
    </div>
  )
}
