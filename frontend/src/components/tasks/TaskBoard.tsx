import { DndContext, DragEndEvent, closestCenter, PointerSensor, useSensor, useSensors } from '@dnd-kit/core'
import { Task, TaskStatus } from '../../types'
import TaskColumn from './TaskColumn'

interface TaskBoardProps {
  tasks: Task[]
  onTaskStatusChange: (taskId: string, newStatus: TaskStatus) => void
  onTaskClick: (task: Task) => void
}

const columns: TaskStatus[] = ['TODO', 'IN_PROGRESS', 'DONE']

export default function TaskBoard({ tasks, onTaskStatusChange, onTaskClick }: TaskBoardProps) {
  // Handler for status change from TaskCard buttons
  const handleCardStatusChange = (taskId: string, newStatus: string) => {
    onTaskStatusChange(taskId, newStatus as TaskStatus)
  }
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  )

  const getTasksByStatus = (status: TaskStatus) => {
    return tasks.filter(task => task.status === status)
  }

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    
    if (!over) return
    
    const taskId = active.id as string
    const newStatus = over.id as TaskStatus
    
    // Check if dropped on a column
    if (columns.includes(newStatus)) {
      const task = tasks.find(t => t.id === taskId)
      if (task && task.status !== newStatus) {
        onTaskStatusChange(taskId, newStatus)
      }
    }
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <div className="flex gap-4 overflow-x-auto pb-4">
        {columns.map((status) => (
          <TaskColumn
            key={status}
            status={status}
            tasks={getTasksByStatus(status)}
            onTaskClick={onTaskClick}
            onStatusChange={handleCardStatusChange}
          />
        ))}
      </div>
    </DndContext>
  )
}
