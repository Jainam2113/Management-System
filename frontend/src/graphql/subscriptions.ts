import { gql } from '@apollo/client'

export const TASK_UPDATED = gql`
  subscription OnTaskUpdated($projectId: ID!) {
    taskUpdated(projectId: $projectId) {
      id
      title
      description
      status
      assigneeEmail
      dueDate
    }
  }
`

export const COMMENT_ADDED = gql`
  subscription OnCommentAdded($taskId: ID!) {
    commentAdded(taskId: $taskId) {
      id
      content
      authorEmail
      createdAt
    }
  }
`
