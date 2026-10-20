// Brand gradient. The 700 shades keep white text readable on top of it.
export const BRAND_GRADIENT = 'bg-linear-to-r from-indigo-700 via-violet-700 to-teal-700'

const COLORS = {
  engineering: 'bg-blue-100 text-blue-800 ring-blue-200',
  growth: 'bg-orange-100 text-orange-800 ring-orange-200',
  people: 'bg-pink-100 text-pink-800 ring-pink-200',
  finance: 'bg-green-100 text-green-800 ring-green-200',
  general: 'bg-violet-100 text-violet-800 ring-violet-200',
  personal: 'bg-teal-100 text-teal-800 ring-teal-200',
}

export function colorFor(name) {
  return COLORS[name] || 'bg-slate-100 text-slate-700 ring-slate-200'
}

// "data/people/salary-bands.md" -> "people"
export function folderOf(path) {
  return path.replace(/^data\//, '').split('/')[0]
}
