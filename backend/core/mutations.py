"""GraphQL mutations for project management system."""
import graphene
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Organization, Project, Task, TaskComment, ProjectStatus, TaskStatus
from .types import (
    OrganizationType,
    ProjectType,
    TaskType,
    TaskCommentType,
    CreateOrganizationInput,
    CreateProjectInput,
    UpdateProjectInput,
    CreateTaskInput,
    UpdateTaskInput,
    CreateCommentInput,
    ErrorType,
)


# Organization Mutations
class OrganizationPayload(graphene.ObjectType):
    """Payload for organization mutations."""
    organization = graphene.Field(OrganizationType)
    errors = graphene.List(ErrorType)


class CreateOrganization(graphene.Mutation):
    """Create a new organization."""
    
    class Arguments:
        input = CreateOrganizationInput(required=True)
    
    Output = OrganizationPayload

    def mutate(self, info, input):
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError as DjangoValidationError
        from django.utils.text import slugify
        
        errors = []
        
        # Validate email
        try:
            validate_email(input.contact_email)
        except DjangoValidationError:
            errors.append(ErrorType(field='contact_email', message='Invalid email format'))
            return OrganizationPayload(organization=None, errors=errors)
        
        # Validate slug uniqueness
        slug = slugify(input.slug)
        if Organization.objects.filter(slug=slug).exists():
            errors.append(ErrorType(field='slug', message='Organization with this slug already exists'))
            return OrganizationPayload(organization=None, errors=errors)
        
        # Create organization
        organization = Organization.objects.create(
            name=input.name,
            slug=slug,
            contact_email=input.contact_email,
        )
        
        return OrganizationPayload(organization=organization, errors=[])


# Project Mutations
class ProjectPayload(graphene.ObjectType):
    """Payload for project mutations."""
    project = graphene.Field(ProjectType)
    errors = graphene.List(ErrorType)


class CreateProject(graphene.Mutation):
    """Create a new project."""
    
    class Arguments:
        input = CreateProjectInput(required=True)
    
    Output = ProjectPayload

    def mutate(self, info, input):
        errors = []
        
        # Validate organization exists
        try:
            organization = Organization.objects.get(slug=input.organization_slug)
        except Organization.DoesNotExist:
            errors.append(ErrorType(field='organization_slug', message='Organization not found'))
            return ProjectPayload(project=None, errors=errors)
        
        # Validate status if provided
        status = input.status or ProjectStatus.ACTIVE
        if status not in [s.value for s in ProjectStatus]:
            errors.append(ErrorType(field='status', message=f'Invalid status. Must be one of: {", ".join([s.value for s in ProjectStatus])}'))
            return ProjectPayload(project=None, errors=errors)
        
        # Create project
        project = Project.objects.create(
            organization=organization,
            name=input.name,
            description=input.description or '',
            status=status,
            due_date=input.due_date,
        )
        
        return ProjectPayload(project=project, errors=[])


class UpdateProject(graphene.Mutation):
    """Update an existing project."""
    
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateProjectInput(required=True)
    
    Output = ProjectPayload

    def mutate(self, info, id, input):
        errors = []
        
        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist:
            errors.append(ErrorType(field='id', message='Project not found'))
            return ProjectPayload(project=None, errors=errors)
        
        # Validate status if provided
        if input.status:
            if input.status not in [s.value for s in ProjectStatus]:
                errors.append(ErrorType(field='status', message=f'Invalid status. Must be one of: {", ".join([s.value for s in ProjectStatus])}'))
                return ProjectPayload(project=None, errors=errors)
            project.status = input.status
        
        if input.name is not None:
            project.name = input.name
        if input.description is not None:
            project.description = input.description
        if input.due_date is not None:
            project.due_date = input.due_date
        
        project.save()
        return ProjectPayload(project=project, errors=[])


class DeletePayload(graphene.ObjectType):
    """Payload for delete mutations."""
    success = graphene.Boolean()
    errors = graphene.List(ErrorType)


class DeleteProject(graphene.Mutation):
    """Delete a project."""
    
    class Arguments:
        id = graphene.ID(required=True)
    
    Output = DeletePayload

    def mutate(self, info, id):
        try:
            project = Project.objects.get(id=id)
            project.delete()
            return DeletePayload(success=True, errors=[])
        except Project.DoesNotExist:
            return DeletePayload(
                success=False,
                errors=[ErrorType(field='id', message='Project not found')]
            )


# Task Mutations
class TaskPayload(graphene.ObjectType):
    """Payload for task mutations."""
    task = graphene.Field(TaskType)
    errors = graphene.List(ErrorType)


class CreateTask(graphene.Mutation):
    """Create a new task."""
    
    class Arguments:
        input = CreateTaskInput(required=True)
    
    Output = TaskPayload

    def mutate(self, info, input):
        errors = []
        
        # Validate project exists
        try:
            project = Project.objects.get(id=input.project_id)
        except Project.DoesNotExist:
            errors.append(ErrorType(field='project_id', message='Project not found'))
            return TaskPayload(task=None, errors=errors)
        
        # Validate status if provided
        status = input.status or TaskStatus.TODO
        if status not in [s.value for s in TaskStatus]:
            errors.append(ErrorType(field='status', message=f'Invalid status. Must be one of: {", ".join([s.value for s in TaskStatus])}'))
            return TaskPayload(task=None, errors=errors)
        
        # Validate email if provided
        if input.assignee_email:
            try:
                validate_email(input.assignee_email)
            except ValidationError:
                errors.append(ErrorType(field='assignee_email', message='Invalid email format'))
                return TaskPayload(task=None, errors=errors)
        
        # Create task
        task = Task.objects.create(
            project=project,
            title=input.title,
            description=input.description or '',
            status=status,
            assignee_email=input.assignee_email or '',
            due_date=input.due_date,
        )
        
        # Broadcast task update via WebSocket
        broadcast_task_update(project.id, task)
        
        return TaskPayload(task=task, errors=[])


class UpdateTask(graphene.Mutation):
    """Update an existing task."""
    
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateTaskInput(required=True)
    
    Output = TaskPayload

    def mutate(self, info, id, input):
        errors = []
        
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            errors.append(ErrorType(field='id', message='Task not found'))
            return TaskPayload(task=None, errors=errors)
        
        # Validate status if provided
        if input.status:
            if input.status not in [s.value for s in TaskStatus]:
                errors.append(ErrorType(field='status', message=f'Invalid status. Must be one of: {", ".join([s.value for s in TaskStatus])}'))
                return TaskPayload(task=None, errors=errors)
            task.status = input.status
        
        # Validate email if provided
        if input.assignee_email:
            try:
                validate_email(input.assignee_email)
            except ValidationError:
                errors.append(ErrorType(field='assignee_email', message='Invalid email format'))
                return TaskPayload(task=None, errors=errors)
            task.assignee_email = input.assignee_email
        
        if input.title is not None:
            task.title = input.title
        if input.description is not None:
            task.description = input.description
        if input.due_date is not None:
            task.due_date = input.due_date
        
        task.save()
        
        # Broadcast task update via WebSocket
        broadcast_task_update(task.project.id, task)
        
        return TaskPayload(task=task, errors=[])


class DeleteTask(graphene.Mutation):
    """Delete a task."""
    
    class Arguments:
        id = graphene.ID(required=True)
    
    Output = DeletePayload

    def mutate(self, info, id):
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return DeletePayload(success=True, errors=[])
        except Task.DoesNotExist:
            return DeletePayload(
                success=False,
                errors=[ErrorType(field='id', message='Task not found')]
            )


# Comment Mutations
class CommentPayload(graphene.ObjectType):
    """Payload for comment mutations."""
    comment = graphene.Field(TaskCommentType)
    errors = graphene.List(ErrorType)


class CreateComment(graphene.Mutation):
    """Create a new comment on a task."""
    
    class Arguments:
        input = CreateCommentInput(required=True)
    
    Output = CommentPayload

    def mutate(self, info, input):
        errors = []
        
        # Validate task exists
        try:
            task = Task.objects.get(id=input.task_id)
        except Task.DoesNotExist:
            errors.append(ErrorType(field='task_id', message='Task not found'))
            return CommentPayload(comment=None, errors=errors)
        
        # Validate email
        try:
            validate_email(input.author_email)
        except ValidationError:
            errors.append(ErrorType(field='author_email', message='Invalid email format'))
            return CommentPayload(comment=None, errors=errors)
        
        # Create comment
        comment = TaskComment.objects.create(
            task=task,
            content=input.content,
            author_email=input.author_email,
        )
        
        # Broadcast comment via WebSocket
        broadcast_comment_added(task.id, comment)
        
        return CommentPayload(comment=comment, errors=[])


def broadcast_task_update(project_id, task):
    """Broadcast task update to WebSocket subscribers."""
    try:
        channel_layer = get_channel_layer()
        group_name = f'project_{project_id}_tasks'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'subscription_update',
                'data': {
                    'taskUpdated': {
                        'id': str(task.id),
                        'title': task.title,
                        'description': task.description,
                        'status': task.status,
                        'assigneeEmail': task.assignee_email,
                        'dueDate': task.due_date.isoformat() if task.due_date else None,
                    }
                }
            }
        )
    except Exception:
        pass  # Silently fail if channel layer not available


def broadcast_comment_added(task_id, comment):
    """Broadcast new comment to WebSocket subscribers."""
    try:
        channel_layer = get_channel_layer()
        group_name = f'task_{task_id}_comments'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'subscription_update',
                'data': {
                    'commentAdded': {
                        'id': str(comment.id),
                        'content': comment.content,
                        'authorEmail': comment.author_email,
                        'createdAt': comment.created_at.isoformat(),
                    }
                }
            }
        )
    except Exception:
        pass  # Silently fail if channel layer not available


class Mutation(graphene.ObjectType):
    """Root mutation type."""
    create_organization = CreateOrganization.Field()
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()
    create_comment = CreateComment.Field()
