import { ProjectStatus, TaskStatus } from '../../types'

interface BadgeProps {
  status: ProjectStatus | TaskStatus
  size?: 'sm' | 'md'
}

const statusConfig: Record<string, { label: string; className: string }> = {
  ACTIVE: { label: 'Active', className: 'badge-active' },
  COMPLETED: { label: 'Completed', className: 'badge-completed' },
  ON_HOLD: { label: 'On Hold', className: 'badge-on-hold' },
  TODO: { label: 'To Do', className: 'badge-todo' },
  IN_PROGRESS: { label: 'In Progress', className: 'badge-in-progress' },
  DONE: { label: 'Done', className: 'badge-done' },
}

export default function Badge({ status, size = 'sm' }: BadgeProps) {
  const config = statusConfig[status] || { label: status, className: 'badge-todo' }
  const sizeClass = size === 'sm' ? 'text-xs px-2 py-0.5' : 'text-sm px-2.5 py-1'
  
  return (
    <span className={`badge ${config.className} ${sizeClass}`}>
      {config.label}
    </span>
  )
}
