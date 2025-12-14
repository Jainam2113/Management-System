import { TaskComment } from '../../types'
import { LoadingSpinner } from '../ui'

interface CommentListProps {
  comments: TaskComment[]
  loading?: boolean
}

export default function CommentList({ comments, loading }: CommentListProps) {
  if (loading) {
    return <LoadingSpinner size="sm" className="py-4" />
  }

  if (comments.length === 0) {
    return (
      <p className="text-sm text-light-text-secondary dark:text-dark-text-secondary py-4 text-center">
        No comments yet
      </p>
    )
  }

  return (
    <div className="space-y-3">
      {comments.map((comment) => (
        <div 
          key={comment.id} 
          className="p-3 rounded-lg bg-light-bg-secondary dark:bg-dark-bg-secondary/50"
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium">{comment.authorEmail}</span>
            <span className="text-xs text-light-text-secondary dark:text-dark-text-secondary">
              {new Date(comment.createdAt).toLocaleString()}
            </span>
          </div>
          <p className="text-sm text-light-text-secondary dark:text-dark-text-secondary">
            {comment.content}
          </p>
        </div>
      ))}
    </div>
  )
}
