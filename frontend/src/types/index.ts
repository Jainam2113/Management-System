// Organization types
export interface Organization {
  id: string
  name: string
  slug: string
  contactEmail: string
  createdAt: string
}

// Project types
export type ProjectStatus = 'ACTIVE' | 'COMPLETED' | 'ON_HOLD'

export interface Project {
  id: string
  name: string
  description: string
  status: ProjectStatus
  dueDate?: string
  createdAt: string
  taskCount: number
  completedTasks: number
}

export interface CreateProjectInput {
  name: string
  description?: string
  status: ProjectStatus
  dueDate?: string
  organizationSlug: string
}

export interface UpdateProjectInput {
  name?: string
  description?: string
  status?: ProjectStatus
  dueDate?: string
}

// Task types
export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'DONE'

export interface Task {
  id: string
  title: string
  description: string
  status: TaskStatus
  assigneeEmail?: string
  dueDate?: string
  createdAt: string
  comments?: TaskComment[]
}

export interface CreateTaskInput {
  projectId: string
  title: string
  description?: string
  status: TaskStatus
  assigneeEmail?: string
  dueDate?: string
}

export interface UpdateTaskInput {
  title?: string
  description?: string
  status?: TaskStatus
  assigneeEmail?: string
  dueDate?: string
}

// Comment types
export interface TaskComment {
  id: string
  content: string
  authorEmail: string
  createdAt: string
}

export interface CreateCommentInput {
  taskId: string
  content: string
  authorEmail: string
}

// Statistics types
export interface ProjectStatistics {
  totalTasks: number
  completedTasks: number
  inProgressTasks: number
  todoTasks: number
  completionRate: number
}

// GraphQL payload types
export interface MutationPayload<T> {
  data?: T
  errors?: Array<{
    field: string
    message: string
  }>
}
