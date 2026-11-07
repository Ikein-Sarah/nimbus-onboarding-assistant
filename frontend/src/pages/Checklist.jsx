import ChecklistCard from '../components/ChecklistCard'

export default function Checklist({ data, onToggle }) {
  return (
    <section>
      <ChecklistCard items={data.checklist} onToggle={onToggle} />
    </section>
  )
}
