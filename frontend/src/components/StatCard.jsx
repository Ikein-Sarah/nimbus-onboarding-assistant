// One of the four cards at the top of Home. With `to` it links to that page;
// `highlight` is the caramel card, which isn't a link.
export default function StatCard({ icon, label, value, unit, progress, to, highlight }) {
  const body = (
    <>
      <div className="ic">{icon}</div>
      <div>
        <div className="lb">{label}</div>
        <div className="n">{value}{unit && <> <small>{unit}</small></>}</div>
      </div>
      {progress !== undefined && (
        <div className="bar"><i style={{ width: `${Math.round(progress * 100)}%` }} /></div>
      )}
    </>
  )

  if (highlight || !to) return <div className={`card kpi${highlight ? ' hl' : ''}`}>{body}</div>
  return <a className="card kpi" href={to}>{body}</a>
}
