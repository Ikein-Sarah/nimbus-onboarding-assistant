export default function ChecklistCard({ items, onToggle }) {
  const done = items.filter((item) => item.done).length
  const percent = items.length ? Math.round((done / items.length) * 100) : 0

  return (
    <div className="card check">
      <h3>Progress <small>{done} of {items.length} done</small></h3>
      <div className="bar"><i style={{ width: `${percent}%` }} /></div>
      <ul className="list">
        {items.map((item) => (
          <li key={item.id} className={item.done ? 'done' : undefined}>
            <button role="checkbox" aria-checked={item.done} onClick={() => onToggle(item.id)}>
              <div className="tick">{item.done ? '✓' : ''}</div>
              <span>{item.title}</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
