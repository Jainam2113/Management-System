"""GraphQL schema for project management system."""
import graphene
from django.db.models import Q
from .models import Organization, Project, Task, TaskComment, TaskStatus
from .types import (
    OrganizationType,
    ProjectType,
    TaskType,
    TaskCommentType,
    ProjectStatisticsType,
)
from .mutations import Mutation


class Query(graphene.ObjectType):
    """Root query type for GraphQL API."""
    
    # Organization queries
    organizations = graphene.List(OrganizationType)
    organization = graphene.Field(OrganizationType, slug=graphene.String(required=True))
    
    # Project queries
    projects = graphene.List(
        ProjectType,
        organization_slug=graphene.String(required=True),
        status=graphene.String(),
        search=graphene.String(),
    )
    project = graphene.Field(ProjectType, id=graphene.ID(required=True))
    project_statistics = graphene.Field(
        ProjectStatisticsType,
        project_id=graphene.ID(required=True)
    )
    
    # Task queries
    tasks = graphene.List(
        TaskType,
        project_id=graphene.ID(required=True),
        status=graphene.String(),
        search=graphene.String(),
    )
    task = graphene.Field(TaskType, id=graphene.ID(required=True))
    
    # Comment queries
    comments = graphene.List(TaskCommentType, task_id=graphene.ID(required=True))

    def resolve_organizations(self, info):
        """List all organizations."""
        return Organization.objects.all()

    def resolve_organization(self, info, slug):
        """Get organization by slug."""
        try:
            return Organization.objects.get(slug=slug)
        except Organization.DoesNotExist:
            return None

    def resolve_projects(self, info, organization_slug, status=None, search=None):
        """
        List projects for an organization with optional filtering.
        Enforces organization-based data isolation.
        """
        queryset = Project.objects.for_organization(organization_slug)
        
        if status:
            queryset = queryset.filter(status=status)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset

    def resolve_project(self, info, id):
        """Get project by ID."""
        # Get organization context from request if available
        org_slug = getattr(info.context, 'organization_slug', None)
        
        try:
            project = Project.objects.get(id=id)
            # Verify organization access if context is available
            if org_slug and project.organization.slug != org_slug:
                return None
            return project
        except Project.DoesNotExist:
            return None

    def resolve_project_statistics(self, info, project_id):
        """Get statistics for a project."""
        try:
            project = Project.objects.get(id=project_id)
            tasks = project.tasks.all()
            total = tasks.count()
            completed = tasks.filter(status=TaskStatus.DONE).count()
            in_progress = tasks.filter(status=TaskStatus.IN_PROGRESS).count()
            todo = tasks.filter(status=TaskStatus.TODO).count()
            
            return ProjectStatisticsType(
                total_tasks=total,
                completed_tasks=completed,
                in_progress_tasks=in_progress,
                todo_tasks=todo,
                completion_rate=round((completed / total * 100), 1) if total > 0 else 0
            )
        except Project.DoesNotExist:
            return None

    def resolve_tasks(self, info, project_id, status=None, search=None):
        """
        List tasks for a project with optional filtering.
        """
        queryset = Task.objects.for_project(project_id)
        
        if status:
            queryset = queryset.filter(status=status)
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset

    def resolve_task(self, info, id):
        """Get task by ID."""
        try:
            return Task.objects.get(id=id)
        except Task.DoesNotExist:
            return None

    def resolve_comments(self, info, task_id):
        """List comments for a task, ordered by created_at descending."""
        return TaskComment.objects.for_task(task_id).order_by('-created_at')


schema = graphene.Schema(query=Query, mutation=Mutation)
