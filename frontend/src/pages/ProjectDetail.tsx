import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation } from '@apollo/client'
import { GET_PROJECT, GET_TASKS, GET_COMMENTS } from '../graphql/queries'
import { CREATE_TASK, UPDATE_TASK, CREATE_COMMENT } from '../graphql/mutations'
import { TaskBoard, TaskForm } from '../components/tasks'
import { CommentList, CommentForm } from '../components/comments'
import { Button, Modal, Badge, LoadingSpinner } from '../components/ui'
import { Task, TaskStatus, CreateTaskInput } from '../types'

export default function ProjectDetail() {
  const { projectId } = useParams<{ projectId: string }>()
  const navigate = useNavigate()
  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false)
  const [selectedTask, setSelectedTask] = useState<Task | null>(null)
  const [isTaskDetailOpen, setIsTaskDetailOpen] = useState(false)

  const { data: projectData, loading: projectLoading } = useQuery(GET_PROJECT, {
    variables: { id: projectId },
    skip: !projectId,
  })

  const { data: tasksData, loading: tasksLoading, refetch: refetchTasks } = useQuery(GET_TASKS, {
    variables: { projectId },
    skip: !projectId,
  })

  const { data: commentsData, loading: commentsLoading, refetch: refetchComments } = useQuery(GET_COMMENTS, {
    variables: { taskId: selectedTask?.id },
    skip: !selectedTask?.id,
  })

  const [createTask, { loading: creatingTask }] = useMutation(CREATE_TASK, {
    onCompleted: () => {
      setIsTaskModalOpen(false)
      refetchTasks()
    },
  })

  const [updateTask] = useMutation(UPDATE_TASK, {
    onCompleted: () => {
      refetchTasks()
    },
  })

  const [createComment, { loading: creatingComment }] = useMutation(CREATE_COMMENT, {
    onCompleted: () => {
      refetchComments()
    },
  })

  const handleCreateTask = (input: CreateTaskInput) => {
    createTask({ variables: { input } })
  }

  const handleTaskStatusChange = (taskId: string, newStatus: TaskStatus) => {
    updateTask({
      variables: {
        id: taskId,
        input: { status: newStatus },
      },
      optimisticResponse: {
        updateTask: {
          __typename: 'TaskPayload',
          task: {
            __typename: 'TaskType',
            id: taskId,
            status: newStatus,
          },
          errors: [],
        },
      },
    })
  }

  const handleTaskClick = (task: Task) => {
    setSelectedTask(task)
    setIsTaskDetailOpen(true)
  }

  const handleAddComment = (content: string, authorEmail: string) => {
    if (!selectedTask) return
    createComment({
      variables: {
        input: {
          taskId: selectedTask.id,
          content,
          authorEmail,
        },
      },
    })
  }

  if (projectLoading) {
    return <LoadingSpinner size="lg" className="py-12" />
  }

  const project = projectData?.project
  const tasks: Task[] = tasksData?.tasks || []
  const comments = commentsData?.comments || []

  if (!project) {
    return (
      <div className="text-center py-12">
        <p className="text-light-text-secondary dark:text-dark-text-secondary mb-4">
          Project not found
        </p>
        <Button onClick={() => navigate('/')}>Back to Dashboard</Button>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={() => navigate('/')}
          className="p-2 rounded-md hover:bg-light-bg-secondary dark:hover:bg-dark-bg-secondary transition-colors"
          aria-label="Back to dashboard"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-semibold">{project.name}</h2>
            <Badge status={project.status} />
          </div>
          {project.description && (
            <p className="text-sm text-light-text-secondary dark:text-dark-text-secondary mt-1">
              {project.description}
            </p>
          )}
        </div>
        <Button onClick={() => setIsTaskModalOpen(true)}>+ Add Task</Button>
      </div>

      {tasksLoading ? (
        <LoadingSpinner size="lg" className="py-12" />
      ) : (
        <TaskBoard
          tasks={tasks}
          onTaskStatusChange={handleTaskStatusChange}
          onTaskClick={handleTaskClick}
        />
      )}

      <Modal
        isOpen={isTaskModalOpen}
        onClose={() => setIsTaskModalOpen(false)}
        title="Create New Task"
      >
        <TaskForm
          projectId={projectId!}
          onSubmit={handleCreateTask}
          onCancel={() => setIsTaskModalOpen(false)}
          isLoading={creatingTask}
        />
      </Modal>

      <Modal
        isOpen={isTaskDetailOpen}
        onClose={() => {
          setIsTaskDetailOpen(false)
          setSelectedTask(null)
        }}
        title={selectedTask?.title || 'Task Details'}
      >
        {selectedTask && (
          <div className="space-y-4">
            <div>
              <Badge status={selectedTask.status} />
            </div>
            {selectedTask.description && (
              <p className="text-sm text-light-text-secondary dark:text-dark-text-secondary">
                {selectedTask.description}
              </p>
            )}
            {selectedTask.assigneeEmail && (
              <p className="text-sm">
                <span className="text-light-text-secondary dark:text-dark-text-secondary">Assignee: </span>
                {selectedTask.assigneeEmail}
              </p>
            )}
            
            <div className="border-t border-light-border dark:border-dark-border pt-4">
              <h4 className="font-medium mb-3">Comments</h4>
              <CommentList comments={comments} loading={commentsLoading} />
              <div className="mt-4">
                <CommentForm onSubmit={handleAddComment} isLoading={creatingComment} />
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  )
}
