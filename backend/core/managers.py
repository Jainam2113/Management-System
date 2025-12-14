"""Tenant-aware model managers for multi-tenancy support."""
from django.db import models


class TenantQuerySet(models.QuerySet):
    """QuerySet with tenant filtering capabilities."""

    def for_organization(self, organization_slug):
        """Filter queryset by organization slug."""
        return self.filter(organization__slug=organization_slug)


class TenantManager(models.Manager):
    """Manager with tenant-aware methods."""

    def get_queryset(self):
        return TenantQuerySet(self.model, using=self._db)

    def for_organization(self, organization_slug):
        """Get objects for a specific organization."""
        return self.get_queryset().for_organization(organization_slug)


class ProjectTenantQuerySet(models.QuerySet):
    """QuerySet for Project with tenant filtering."""

    def for_organization(self, organization_slug):
        """Filter projects by organization slug."""
        return self.filter(organization__slug=organization_slug)

    def with_stats(self):
        """Annotate projects with task statistics."""
        from django.db.models import Count, Q
        from core.models import TaskStatus
        return self.annotate(
            task_count_annotated=Count('tasks'),
            completed_tasks_annotated=Count(
                'tasks',
                filter=Q(tasks__status=TaskStatus.DONE)
            )
        )


class ProjectTenantManager(models.Manager):
    """Manager for Project with tenant-aware methods."""

    def get_queryset(self):
        return ProjectTenantQuerySet(self.model, using=self._db)

    def for_organization(self, organization_slug):
        """Get projects for a specific organization."""
        return self.get_queryset().for_organization(organization_slug)

    def with_stats(self):
        """Get projects with task statistics."""
        return self.get_queryset().with_stats()


class TaskTenantQuerySet(models.QuerySet):
    """QuerySet for Task with tenant filtering."""

    def for_organization(self, organization_slug):
        """Filter tasks by organization slug (through project)."""
        return self.filter(project__organization__slug=organization_slug)

    def for_project(self, project_id):
        """Filter tasks by project."""
        return self.filter(project_id=project_id)

    def by_status(self, status):
        """Filter tasks by status."""
        return self.filter(status=status)


class TaskTenantManager(models.Manager):
    """Manager for Task with tenant-aware methods."""

    def get_queryset(self):
        return TaskTenantQuerySet(self.model, using=self._db)

    def for_organization(self, organization_slug):
        """Get tasks for a specific organization."""
        return self.get_queryset().for_organization(organization_slug)

    def for_project(self, project_id):
        """Get tasks for a specific project."""
        return self.get_queryset().for_project(project_id)


class CommentTenantQuerySet(models.QuerySet):
    """QuerySet for TaskComment with tenant filtering."""

    def for_organization(self, organization_slug):
        """Filter comments by organization slug (through task->project)."""
        return self.filter(task__project__organization__slug=organization_slug)

    def for_task(self, task_id):
        """Filter comments by task."""
        return self.filter(task_id=task_id)


class CommentTenantManager(models.Manager):
    """Manager for TaskComment with tenant-aware methods."""

    def get_queryset(self):
        return CommentTenantQuerySet(self.model, using=self._db)

    def for_organization(self, organization_slug):
        """Get comments for a specific organization."""
        return self.get_queryset().for_organization(organization_slug)

    def for_task(self, task_id):
        """Get comments for a specific task."""
        return self.get_queryset().for_task(task_id)
