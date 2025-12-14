import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { Task } from '../../types'

interface TaskCardProps {
  task: Task
  onClick: () => void
  onStatusChange?: (taskId: string, newStatus: string) => void
}

const statusOptions = [
  { value: 'TODO', label: 'To Do', color: 'bg-status-todo' },
  { value: 'IN_PROGRESS', label: 'In Progress', color: 'bg-status-in-progress' },
  { value: 'DONE', label: 'Done', color: 'bg-status-done' },
]

export default function TaskCard({ task, onClick, onStatusChange }: TaskCardProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: task.id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  }

  const handleStatusClick = (e: React.MouseEvent, newStatus: string) => {
    e.stopPropagation()
    if (onStatusChange && newStatus !== task.status) {
      onStatusChange(task.id, newStatus)
    }
  }

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={`glass-card p-3 cursor-grab active:cursor-grabbing group hover:shadow-md transition-all duration-200 hover:scale-[1.01] ${
        isDragging ? 'shadow-lg ring-2 ring-primary/30' : ''
      }`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && onClick()}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <h4 className="text-sm font-medium text-light-text dark:text-dark-text line-clamp-2 group-hover:text-primary transition-colors">
          {task.title}
        </h4>
      </div>
      
      {task.description && (
        <p className="text-xs text-light-text-secondary dark:text-dark-text-secondary line-clamp-2 mb-2">
          {task.description}
        </p>
      )}

      {/* Status change buttons */}
      {onStatusChange && (
        <div className="flex gap-1 mb-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          {statusOptions.map((status) => (
            <button
              key={status.value}
              onClick={(e) => handleStatusClick(e, status.value)}
              className={`flex-1 text-[10px] py-1 px-1.5 rounded transition-all duration-200 ${
                task.status === status.value
                  ? `${status.color} text-white font-medium shadow-sm`
                  : 'bg-light-bg-secondary dark:bg-dark-bg hover:bg-light-border dark:hover:bg-dark-border text-light-text-secondary dark:text-dark-text-secondary'
              }`}
              title={`Move to ${status.label}`}
            >
              {status.label}
            </button>
          ))}
        </div>
      )}
      
      <div className="flex items-center justify-between">
        {task.assigneeEmail && (
          <span className="text-xs text-light-text-secondary dark:text-dark-text-secondary truncate max-w-[120px] flex items-center gap-1">
            <span className="w-4 h-4 rounded-full bg-primary/20 flex items-center justify-center text-[10px] text-primary font-medium">
              {task.assigneeEmail.charAt(0).toUpperCase()}
            </span>
            {task.assigneeEmail.split('@')[0]}
          </span>
        )}
        {task.dueDate && (
          <span className="text-xs text-light-text-secondary dark:text-dark-text-secondary flex items-center gap-1">
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {new Date(task.dueDate).toLocaleDateString()}
          </span>
        )}
      </div>
    </div>
  )
}
