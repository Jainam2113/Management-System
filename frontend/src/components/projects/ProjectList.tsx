import { Project } from '../../types'
import { LoadingSpinner } from '../ui'
import ProjectCard from './ProjectCard'

interface ProjectListProps {
  projects: Project[]
  loading: boolean
  error?: string
}

export default function ProjectList({ projects, loading, error }: ProjectListProps) {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="glass-card p-6 text-center">
        <p className="text-red-500 mb-2">Error loading projects</p>
        <p className="text-sm text-light-text-secondary dark:text-dark-text-secondary">{error}</p>
      </div>
    )
  }

  if (projects.length === 0) {
    return (
      <div className="glass-card p-6 text-center">
        <p className="text-light-text-secondary dark:text-dark-text-secondary">
          No projects yet. Create your first project to get started!
        </p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {projects.map((project) => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  )
}
