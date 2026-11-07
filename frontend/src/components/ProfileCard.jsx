import { shortDate } from '../dates'
import Avatar from './Avatar'

export default function ProfileCard({ profile }) {
  const rows = [
    ['Role', profile.title],
    ['Team', profile.department[0].toUpperCase() + profile.department.slice(1)],
    ['Manager', profile.manager?.name || '—'],
    ['Started', shortDate(profile.start_date)],
  ]

  return (
    <div className="card prof">
      <Avatar name={profile.name} />
      <h4>{profile.name}</h4>
      <div className="r">{profile.email}</div>
      <dl>
        {rows.map(([label, value]) => (
          <div key={label}><dt>{label}</dt><dd>{value}</dd></div>
        ))}
      </dl>
    </div>
  )
}
