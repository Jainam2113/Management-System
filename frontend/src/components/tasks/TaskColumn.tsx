import { useDroppable } from '@dnd-kit/core'
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable'
import { Task, TaskStatus } from '../../types'
import TaskCard from './TaskCard'

interface TaskColumnProps {
  status: TaskStatus
  tasks: Task[]
  onTaskClick: (task: Task) => void
  onStatusChange?: (taskId: string, newStatus: string) => void
}

const columnConfig: Record<TaskStatus, { title: string; color: string }> = {
  TODO: { title: 'To Do', color: 'bg-status-todo' },
  IN_PROGRESS: { title: 'In Progress', color: 'bg-status-in-progress' },
  DONE: { title: 'Done', color: 'bg-status-done' },
}

export default function TaskColumn({ status, tasks, onTaskClick, onStatusChange }: TaskColumnProps) {
  const { setNodeRef, isOver } = useDroppable({ id: status })
  const config = columnConfig[status]

  return (
    <div className="flex flex-col min-w-[280px] max-w-[320px]">
      <div className="flex items-center gap-2 mb-3">
        <div className={`w-2 h-2 rounded-full ${config.color}`} />
        <h3 className="font-medium text-sm">{config.title}</h3>
        <span className="text-xs text-light-text-secondary dark:text-dark-text-secondary">
          ({tasks.length})
        </span>
      </div>
      
      <div
        ref={setNodeRef}
        className={`flex-1 p-2 rounded-lg transition-colors ${
          isOver 
            ? 'bg-primary/10 border-2 border-dashed border-primary' 
            : 'bg-light-bg-secondary dark:bg-dark-bg-secondary/50'
        }`}
      >
        <SortableContext items={tasks.map(t => t.id)} strategy={verticalListSortingStrategy}>
          <div className="space-y-2">
            {tasks.map((task) => (
              <TaskCard 
                key={task.id} 
                task={task} 
                onClick={() => onTaskClick(task)}
                onStatusChange={onStatusChange}
              />
            ))}
            {tasks.length === 0 && (
              <p className="text-xs text-center text-light-text-secondary dark:text-dark-text-secondary py-4">
                No tasks
              </p>
            )}
          </div>
        </SortableContext>
      </div>
    </div>
  )
}
