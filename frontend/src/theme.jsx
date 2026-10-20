import { colorFor } from './colors'

export function DepartmentBadge({ department }) {
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold capitalize ring-1 ring-inset ${colorFor(department)}`}>
      {department}
    </span>
  )
}

export function Logo({ className = 'h-9 w-9 text-lg' }) {
  return (
    <div className={`flex items-center justify-center rounded-xl bg-white/15 font-bold text-white ring-1 ring-white/30 backdrop-blur ${className}`}>
      N
    </div>
  )
}
