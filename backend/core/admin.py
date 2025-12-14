"""Django admin configuration."""
from django.contrib import admin
from .models import Organization, Project, Task, TaskComment


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'contact_email', 'created_at']
    search_fields = ['name', 'slug', 'contact_email']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'organization']
    search_fields = ['name', 'description']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'status', 'assignee_email', 'due_date', 'created_at']
    list_filter = ['status', 'project__organization']
    search_fields = ['title', 'description', 'assignee_email']


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'author_email', 'created_at']
    list_filter = ['task__project__organization']
    search_fields = ['content', 'author_email']
