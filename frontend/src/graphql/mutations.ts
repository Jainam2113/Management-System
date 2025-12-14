import { gql } from '@apollo/client'

export const CREATE_ORGANIZATION = gql`
  mutation CreateOrganization($input: CreateOrganizationInput!) {
    createOrganization(input: $input) {
      organization {
        id
        name
        slug
        contactEmail
      }
      errors {
        field
        message
      }
    }
  }
`

export const CREATE_PROJECT = gql`
  mutation CreateProject($input: CreateProjectInput!) {
    createProject(input: $input) {
      project {
        id
        name
        description
        status
        dueDate
        createdAt
        taskCount
        completedTasks
      }
      errors {
        field
        message
      }
    }
  }
`

export const UPDATE_PROJECT = gql`
  mutation UpdateProject($id: ID!, $input: UpdateProjectInput!) {
    updateProject(id: $id, input: $input) {
      project {
        id
        name
        description
        status
        dueDate
      }
      errors {
        field
        message
      }
    }
  }
`

export const DELETE_PROJECT = gql`
  mutation DeleteProject($id: ID!) {
    deleteProject(id: $id) {
      success
      errors {
        field
        message
      }
    }
  }
`

export const CREATE_TASK = gql`
  mutation CreateTask($input: CreateTaskInput!) {
    createTask(input: $input) {
      task {
        id
        title
        description
        status
        assigneeEmail
        dueDate
        createdAt
      }
      errors {
        field
        message
      }
    }
  }
`

export const UPDATE_TASK = gql`
  mutation UpdateTask($id: ID!, $input: UpdateTaskInput!) {
    updateTask(id: $id, input: $input) {
      task {
        id
        title
        description
        status
        assigneeEmail
        dueDate
      }
      errors {
        field
        message
      }
    }
  }
`

export const DELETE_TASK = gql`
  mutation DeleteTask($id: ID!) {
    deleteTask(id: $id) {
      success
      errors {
        field
        message
      }
    }
  }
`

export const CREATE_COMMENT = gql`
  mutation CreateComment($input: CreateCommentInput!) {
    createComment(input: $input) {
      comment {
        id
        content
        authorEmail
        createdAt
      }
      errors {
        field
        message
      }
    }
  }
`
