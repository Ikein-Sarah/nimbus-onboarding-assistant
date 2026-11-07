export default function SummaryCard({ summary }) {
  return (
    <div className="card ai">
      <h3>Your week so far <span className="tag">AI summary</span></h3>
      {summary ? (
        <>
          <p>{summary.overview}</p>
          <ul>
            {summary.items.map((item, i) => (
              <li key={i}><b>{item.tag}</b> {item.text}</li>
            ))}
          </ul>
        </>
      ) : (
        <p className="muted">Your summary isn't available right now. Try again in a minute.</p>
      )}
    </div>
  )
}
