import { ago } from '../dates'
import Avatar from './Avatar'

export default function FeedbackCard({ note }) {
  return (
    <div className="card fb">
      <Avatar name={note.from_name} />
      <div>
        <p>{note.text}</p>
        <small>{note.from_name} · {ago(note.date)}</small>
      </div>
    </div>
  )
}
