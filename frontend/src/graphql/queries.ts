import { gql } from '@apollo/client'

export const GET_ORGANIZATIONS = gql`
  query GetOrganizations {
    organizations {
      id
      name
      slug
      contactEmail
    }
  }
`

export const GET_PROJECTS = gql`
  query GetProjects($organizationSlug: String!, $status: String, $search: String) {
    projects(organizationSlug: $organizationSlug, status: $status, search: $search) {
      id
      name
      description
      status
      dueDate
      createdAt
      taskCount
      completedTasks
    }
  }
`

export const GET_PROJECT = gql`
  query GetProject($id: ID!) {
    project(id: $id) {
      id
      name
      description
      status
      dueDate
      createdAt
      taskCount
      completedTasks
    }
  }
`

export const GET_TASKS = gql`
  query GetTasks($projectId: ID!, $status: String, $search: String) {
    tasks(projectId: $projectId, status: $status, search: $search) {
      id
      title
      description
      status
      assigneeEmail
      dueDate
      createdAt
    }
  }
`

export const GET_TASK = gql`
  query GetTask($id: ID!) {
    task(id: $id) {
      id
      title
      description
      status
      assigneeEmail
      dueDate
      createdAt
      comments {
        id
        content
        authorEmail
        createdAt
      }
    }
  }
`

export const GET_COMMENTS = gql`
  query GetComments($taskId: ID!) {
    comments(taskId: $taskId) {
      id
      content
      authorEmail
      createdAt
    }
  }
`

export const GET_PROJECT_STATISTICS = gql`
  query GetProjectStatistics($projectId: ID!) {
    projectStatistics(projectId: $projectId) {
      totalTasks
      completedTasks
      inProgressTasks
      todoTasks
      completionRate
    }
  }
`
