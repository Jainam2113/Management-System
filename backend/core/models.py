"""Django models for project management system."""
import uuid
from django.db import models
from django.core.validators import EmailValidator
from .managers import (
    ProjectTenantManager,
    TaskTenantManager,
    CommentTenantManager,
)


class Organization(models.Model):
    """
    Organization model - represents a tenant in the multi-tenant system.
    All data is isolated by organization.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, db_index=True)
    contact_email = models.EmailField(validators=[EmailValidator()])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProjectStatus(models.TextChoices):
    """Project status choices."""
    ACTIVE = 'ACTIVE', 'Active'
    COMPLETED = 'COMPLETED', 'Completed'
    ON_HOLD = 'ON_HOLD', 'On Hold'


class Project(models.Model):
    """
    Project model - belongs to an organization.
    Contains tasks and tracks project status.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='projects',
        db_index=True
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.ACTIVE,
        db_index=True
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ProjectTenantManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def task_count(self):
        """Return total number of tasks."""
        return self.tasks.count()

    @property
    def completed_tasks(self):
        """Return number of completed tasks."""
        return self.tasks.filter(status=TaskStatus.DONE).count()

    @property
    def completion_rate(self):
        """Return completion rate as percentage."""
        total = self.task_count
        if total == 0:
            return 0
        return round((self.completed_tasks / total) * 100, 1)


class TaskStatus(models.TextChoices):
    """Task status choices."""
    TODO = 'TODO', 'To Do'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    DONE = 'DONE', 'Done'


class Task(models.Model):
    """
    Task model - belongs to a project.
    Represents a work item with status tracking.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        db_index=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
        db_index=True
    )
    assignee_email = models.EmailField(
        blank=True,
        default='',
        validators=[EmailValidator()]
    )
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TaskTenantManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        """Validate assignee_email only if provided."""
        if self.assignee_email:
            validator = EmailValidator()
            validator(self.assignee_email)


class TaskComment(models.Model):
    """
    TaskComment model - belongs to a task.
    Allows collaboration through comments.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        db_index=True
    )
    content = models.TextField()
    author_email = models.EmailField(validators=[EmailValidator()])
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = CommentTenantManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author_email} on {self.task.title}"
