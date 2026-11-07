export default function Avatar({ name, className = '' }) {
  return <div className={`av ${className}`} aria-hidden="true">{name?.[0]?.toUpperCase() || '?'}</div>
}
