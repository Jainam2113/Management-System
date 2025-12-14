# API Documentation

## GraphQL Endpoint

- **URL**: `http://localhost:8000/graphql/`
- **WebSocket**: `ws://localhost:8000/graphql/`
- **GraphQL Playground**: Available at the same URL in browser

## Headers

All requests require the organization context header:

```
X-Organization-Slug: demo-org
```

## Schema

### Types

```graphql
type Organization {
  id: ID!
  name: String!
  slug: String!
  contactEmail: String!
  createdAt: DateTime!
}

type Project {
  id: ID!
  name: String!
  description: String!
  status: String!  # ACTIVE, COMPLETED, ON_HOLD
  dueDate: Date
  createdAt: DateTime!
  taskCount: Int!
  completedTasks: Int!
  completionRate: Float!
}

type Task {
  id: ID!
  title: String!
  description: String!
  status: String!  # TODO, IN_PROGRESS, DONE
  assigneeEmail: String
  dueDate: DateTime
  createdAt: DateTime!
  comments: [TaskComment!]!
}

type TaskComment {
  id: ID!
  content: String!
  authorEmail: String!
  createdAt: DateTime!
}

type ProjectStatistics {
  totalTasks: Int!
  completedTasks: Int!
  inProgressTasks: Int!
  todoTasks: Int!
  completionRate: Float!
}
```

### Queries

#### List Projects
```graphql
query GetProjects($organizationSlug: String!, $status: String, $search: String) {
  projects(organizationSlug: $organizationSlug, status: $status, search: $search) {
    id
    name
    description
    status
    dueDate
    taskCount
    completedTasks
  }
}
```

#### Get Project
```graphql
query GetProject($id: ID!) {
  project(id: $id) {
    id
    name
    description
    status
    dueDate
    taskCount
    completedTasks
  }
}
```

#### List Tasks
```graphql
query GetTasks($projectId: ID!, $status: String, $search: String) {
  tasks(projectId: $projectId, status: $status, search: $search) {
    id
    title
    description
    status
    assigneeEmail
    dueDate
  }
}
```

#### Get Task with Comments
```graphql
query GetTask($id: ID!) {
  task(id: $id) {
    id
    title
    description
    status
    assigneeEmail
    comments {
      id
      content
      authorEmail
      createdAt
    }
  }
}
```

#### Project Statistics
```graphql
query GetProjectStatistics($projectId: ID!) {
  projectStatistics(projectId: $projectId) {
    totalTasks
    completedTasks
    inProgressTasks
    todoTasks
    completionRate
  }
}
```

### Mutations

#### Create Project
```graphql
mutation CreateProject($input: CreateProjectInput!) {
  createProject(input: $input) {
    project {
      id
      name
      status
    }
    errors {
      field
      message
    }
  }
}

# Variables
{
  "input": {
    "organizationSlug": "demo-org",
    "name": "New Project",
    "description": "Project description",
    "status": "ACTIVE",
    "dueDate": "2024-12-31"
  }
}
```

#### Update Project
```graphql
mutation UpdateProject($id: ID!, $input: UpdateProjectInput!) {
  updateProject(id: $id, input: $input) {
    project {
      id
      name
      status
    }
    errors {
      field
      message
    }
  }
}
```

#### Create Task
```graphql
mutation CreateTask($input: CreateTaskInput!) {
  createTask(input: $input) {
    task {
      id
      title
      status
    }
    errors {
      field
      message
    }
  }
}

# Variables
{
  "input": {
    "projectId": "project-uuid",
    "title": "New Task",
    "description": "Task description",
    "status": "TODO",
    "assigneeEmail": "developer@example.com"
  }
}
```

#### Update Task
```graphql
mutation UpdateTask($id: ID!, $input: UpdateTaskInput!) {
  updateTask(id: $id, input: $input) {
    task {
      id
      status
    }
    errors {
      field
      message
    }
  }
}
```

#### Create Comment
```graphql
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

# Variables
{
  "input": {
    "taskId": "task-uuid",
    "content": "This is a comment",
    "authorEmail": "user@example.com"
  }
}
```

### Subscriptions

#### Task Updates
```graphql
subscription OnTaskUpdated($projectId: ID!) {
  taskUpdated(projectId: $projectId) {
    id
    title
    status
    assigneeEmail
  }
}
```

#### Comment Added
```graphql
subscription OnCommentAdded($taskId: ID!) {
  commentAdded(taskId: $taskId) {
    id
    content
    authorEmail
    createdAt
  }
}
```

## Error Handling

All mutations return an `errors` array with field-specific error messages:

```json
{
  "data": {
    "createProject": {
      "project": null,
      "errors": [
        {
          "field": "name",
          "message": "Project name is required"
        }
      ]
    }
  }
}
```

## Multi-Tenancy

All data is isolated by organization. The `X-Organization-Slug` header determines which organization's data is accessible. Attempting to access data from another organization will return empty results or a permission error.
