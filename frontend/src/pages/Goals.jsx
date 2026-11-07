import PhaseCard from '../components/PhaseCard'

export default function Goals({ data, onStatus }) {
  return (
    <section>
      <div className="phases">
        {[30, 60, 90].map((phase) => (
          <PhaseCard key={phase} phase={phase} currentPhase={data.stats.current_phase}
            goals={data.goals.filter((g) => g.phase === phase)} onStatus={onStatus} />
        ))}
      </div>
      <p className="hint">Click a goal to move it on: not started, in progress, done.</p>
    </section>
  )
}
