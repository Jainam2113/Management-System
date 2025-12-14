import { useNavigate } from 'react-router-dom'
import { Project } from '../../types'
import { Card, Badge } from '../ui'

interface ProjectCardProps {
  project: Project
}

export default function ProjectCard({ project }: ProjectCardProps) {
  const navigate = useNavigate()
  const completionRate = project.taskCount > 0 
    ? Math.round((project.completedTasks / project.taskCount) * 100) 
    : 0

  return (
    <Card 
      hoverable 
      onClick={() => navigate(`/projects/${project.id}`)}
      className="flex flex-col gap-3 group animate-fadeIn"
    >
      <div className="flex items-start justify-between">
        <h3 className="font-medium text-light-text dark:text-dark-text truncate pr-2 group-hover:text-primary transition-colors">
          {project.name}
        </h3>
        <Badge status={project.status} />
      </div>
      
      {project.description && (
        <p className="text-sm text-light-text-secondary dark:text-dark-text-secondary line-clamp-2">
          {project.description}
        </p>
      )}
      
      <div className="flex items-center justify-between text-xs text-light-text-secondary dark:text-dark-text-secondary">
        <span className="flex items-center gap-1">
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          {project.taskCount} tasks
        </span>
        <span className="font-medium">{completionRate}%</span>
      </div>
      
      {/* Progress bar */}
      <div className="w-full h-2 bg-light-border dark:bg-dark-border rounded-full overflow-hidden">
        <div 
          className="h-full bg-gradient-to-r from-primary to-primary-dark transition-all duration-500 ease-out"
          style={{ width: `${completionRate}%` }}
        />
      </div>
      
      {project.dueDate && (
        <div className="text-xs text-light-text-secondary dark:text-dark-text-secondary flex items-center gap-1">
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          Due: {new Date(project.dueDate).toLocaleDateString()}
        </div>
      )}
    </Card>
  )
}
