import { useState, FormEvent } from 'react'
import { Task, TaskStatus, CreateTaskInput } from '../../types'
import { Button, Input, Select } from '../ui'

interface TaskFormProps {
  task?: Task
  projectId: string
  onSubmit: (data: CreateTaskInput) => void
  onCancel: () => void
  isLoading?: boolean
}

const statusOptions = [
  { value: 'TODO', label: 'To Do' },
  { value: 'IN_PROGRESS', label: 'In Progress' },
  { value: 'DONE', label: 'Done' },
]

export default function TaskForm({ task, projectId, onSubmit, onCancel, isLoading }: TaskFormProps) {
  const [title, setTitle] = useState(task?.title || '')
  const [description, setDescription] = useState(task?.description || '')
  const [status, setStatus] = useState<TaskStatus>(task?.status || 'TODO')
  const [assigneeEmail, setAssigneeEmail] = useState(task?.assigneeEmail || '')
  const [dueDate, setDueDate] = useState(task?.dueDate?.split('T')[0] || '')
  const [errors, setErrors] = useState<Record<string, string>>({})

  const validate = () => {
    const newErrors: Record<string, string> = {}
    if (!title.trim()) {
      newErrors.title = 'Task title is required'
    }
    if (assigneeEmail && !assigneeEmail.includes('@')) {
      newErrors.assigneeEmail = 'Invalid email format'
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!validate()) return

    onSubmit({
      projectId,
      title,
      description,
      status,
      assigneeEmail: assigneeEmail || undefined,
      dueDate: dueDate ? new Date(dueDate).toISOString() : undefined,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Task Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        error={errors.title}
        placeholder="Enter task title"
        required
      />
      
      <div>
        <label className="block text-sm font-medium text-light-text-secondary dark:text-dark-text-secondary mb-1">
          Description
        </label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="input min-h-[80px] resize-none"
          placeholder="Enter task description"
        />
      </div>
      
      <Select
        label="Status"
        value={status}
        onChange={(e) => setStatus(e.target.value as TaskStatus)}
        options={statusOptions}
      />
      
      <Input
        label="Assignee Email"
        type="email"
        value={assigneeEmail}
        onChange={(e) => setAssigneeEmail(e.target.value)}
        error={errors.assigneeEmail}
        placeholder="assignee@example.com"
      />
      
      <Input
        label="Due Date"
        type="date"
        value={dueDate}
        onChange={(e) => setDueDate(e.target.value)}
      />
      
      <div className="flex justify-end gap-3 pt-2">
        <Button type="button" variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit" isLoading={isLoading}>
          {task ? 'Update Task' : 'Create Task'}
        </Button>
      </div>
    </form>
  )
}
