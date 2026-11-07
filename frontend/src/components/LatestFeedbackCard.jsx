import { ago } from '../dates'
import { href } from '../router'
import Avatar from './Avatar'

export default function LatestFeedbackCard({ note }) {
  return (
    <div className="card fbmini">
      <h3>Latest feedback <a href={href('feedback')}>See all</a></h3>
      {note ? (
        <>
          <p>&ldquo;{note.text}&rdquo;</p>
          <div className="who"><Avatar name={note.from_name} />{note.from_name} · {ago(note.date)}</div>
        </>
      ) : (
        <p className="muted">No feedback yet.</p>
      )}
    </div>
  )
}
