import LatestFeedbackCard from '../components/LatestFeedbackCard'
import ProfileCard from '../components/ProfileCard'
import StatCard from '../components/StatCard'
import SummaryCard from '../components/SummaryCard'
import UpNextCard from '../components/UpNextCard'
import { CalendarIcon, FeedbackIcon, TargetIcon, TickIcon } from '../components/Icons'
import { href } from '../router'

export default function Home({ data }) {
  const { stats } = data
  const ratio = (done, total) => (total ? done / total : 0)

  return (
    <section>
      <div className="kpis">
        <StatCard highlight icon={<CalendarIcon />} label="Days at Nimbus" value={stats.days_at_nimbus} />
        <StatCard to={href('goals')} icon={<TargetIcon />} label="Goals this month"
          value={stats.goals_done} unit={`/ ${stats.goals_total}`}
          progress={ratio(stats.goals_done, stats.goals_total)} />
        <StatCard to={href('checklist')} icon={<TickIcon />} label="Checklist"
          value={stats.checklist_done} unit={`/ ${stats.checklist_total}`}
          progress={ratio(stats.checklist_done, stats.checklist_total)} />
        <StatCard to={href('feedback')} icon={<FeedbackIcon />} label="New feedback"
          value={stats.new_feedback} unit={stats.new_feedback === 1 ? 'note' : 'notes'} />
      </div>

      <div className="row">
        <SummaryCard summary={data.summary} />
        <ProfileCard profile={data.profile} />
      </div>

      <div className="row">
        <UpNextCard items={data.up_next} />
        <LatestFeedbackCard note={data.feedback[0]} />
      </div>
    </section>
  )
}
