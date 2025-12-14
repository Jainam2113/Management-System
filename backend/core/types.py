"""GraphQL types for project management system."""
import graphene
from graphene_django import DjangoObjectType
from .models import Organization, Project, Task, TaskComment, TaskStatus


class OrganizationType(DjangoObjectType):
    """GraphQL type for Organization model."""
    
    class Meta:
        model = Organization
        fields = ('id', 'name', 'slug', 'contact_email', 'created_at')


class ProjectStatisticsType(graphene.ObjectType):
    """GraphQL type for project statistics."""
    total_tasks = graphene.Int()
    completed_tasks = graphene.Int()
    in_progress_tasks = graphene.Int()
    todo_tasks = graphene.Int()
    completion_rate = graphene.Float()


class ProjectType(DjangoObjectType):
    """GraphQL type for Project model."""
    task_count = graphene.Int()
    completed_tasks = graphene.Int()
    completion_rate = graphene.Float()
    
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'status', 'due_date', 'created_at', 'organization')

    def resolve_task_count(self, info):
        return self.task_count

    def resolve_completed_tasks(self, info):
        return self.completed_tasks

    def resolve_completion_rate(self, info):
        return self.completion_rate


class TaskCommentType(DjangoObjectType):
    """GraphQL type for TaskComment model."""
    
    class Meta:
        model = TaskComment
        fields = ('id', 'content', 'author_email', 'created_at', 'task')


class TaskType(DjangoObjectType):
    """GraphQL type for Task model."""
    comments = graphene.List(TaskCommentType)
    
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'assignee_email', 'due_date', 'created_at', 'project')

    def resolve_comments(self, info):
        return self.comments.all()


# Input types for mutations
class CreateOrganizationInput(graphene.InputObjectType):
    """Input type for creating an organization."""
    name = graphene.String(required=True)
    slug = graphene.String(required=True)
    contact_email = graphene.String(required=True)


class CreateProjectInput(graphene.InputObjectType):
    """Input type for creating a project."""
    organization_slug = graphene.String(required=True)
    name = graphene.String(required=True)
    description = graphene.String()
    status = graphene.String()
    due_date = graphene.Date()


class UpdateProjectInput(graphene.InputObjectType):
    """Input type for updating a project."""
    name = graphene.String()
    description = graphene.String()
    status = graphene.String()
    due_date = graphene.Date()


class CreateTaskInput(graphene.InputObjectType):
    """Input type for creating a task."""
    project_id = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String()
    status = graphene.String()
    assignee_email = graphene.String()
    due_date = graphene.DateTime()


class UpdateTaskInput(graphene.InputObjectType):
    """Input type for updating a task."""
    title = graphene.String()
    description = graphene.String()
    status = graphene.String()
    assignee_email = graphene.String()
    due_date = graphene.DateTime()


class CreateCommentInput(graphene.InputObjectType):
    """Input type for creating a comment."""
    task_id = graphene.ID(required=True)
    content = graphene.String(required=True)
    author_email = graphene.String(required=True)


# Error type for mutations
class ErrorType(graphene.ObjectType):
    """Error type for mutation responses."""
    field = graphene.String()
    message = graphene.String()
