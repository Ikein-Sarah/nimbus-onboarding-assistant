import FeedbackCard from '../components/FeedbackCard'

export default function Feedback({ data }) {
  return (
    <section>
      <div className="fbs">
        {data.feedback.length === 0 && <div className="card muted">No feedback yet.</div>}
        {data.feedback.map((note) => <FeedbackCard key={note.id} note={note} />)}
      </div>
    </section>
  )
}
