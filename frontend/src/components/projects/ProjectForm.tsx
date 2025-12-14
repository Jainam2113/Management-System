import { useState, FormEvent } from 'react'
import { Project, ProjectStatus, CreateProjectInput } from '../../types'
import { Button, Input, Select } from '../ui'

interface ProjectFormProps {
  project?: Project
  onSubmit: (data: CreateProjectInput) => void
  onCancel: () => void
  isLoading?: boolean
  organizationSlug: string
}

const statusOptions = [
  { value: 'ACTIVE', label: 'Active' },
  { value: 'COMPLETED', label: 'Completed' },
  { value: 'ON_HOLD', label: 'On Hold' },
]

export default function ProjectForm({ project, onSubmit, onCancel, isLoading, organizationSlug }: ProjectFormProps) {
  const [name, setName] = useState(project?.name || '')
  const [description, setDescription] = useState(project?.description || '')
  const [status, setStatus] = useState<ProjectStatus>(project?.status || 'ACTIVE')
  const [dueDate, setDueDate] = useState(project?.dueDate || '')
  const [errors, setErrors] = useState<Record<string, string>>({})

  const validate = () => {
    const newErrors: Record<string, string> = {}
    if (!name.trim()) {
      newErrors.name = 'Project name is required'
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!validate()) return

    onSubmit({
      organizationSlug,
      name,
      description,
      status,
      dueDate: dueDate || undefined,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Project Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        error={errors.name}
        placeholder="Enter project name"
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
          placeholder="Enter project description"
        />
      </div>
      
      <Select
        label="Status"
        value={status}
        onChange={(e) => setStatus(e.target.value as ProjectStatus)}
        options={statusOptions}
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
          {project ? 'Update Project' : 'Create Project'}
        </Button>
      </div>
    </form>
  )
}
