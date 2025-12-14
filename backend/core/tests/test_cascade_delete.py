"""
Property-based tests for cascade delete integrity.

**Feature: project-management-system, Property 4: Cascade Delete Integrity**
**Validates: Requirements 2.4, 3.4, 4.3**

For any organization with projects, deleting the organization shall result in 
zero projects remaining for that organization. For any project with tasks, 
deleting the project shall result in zero tasks remaining for that project.
For any task with comments, deleting the task shall result in zero comments 
remaining for that task.
"""
import pytest
from hypothesis import given, strategies as st, settings
from django.test import TransactionTestCase
from core.models import Organization, Project, Task, TaskComment, ProjectStatus, TaskStatus


class TestCascadeDeleteIntegrity(TransactionTestCase):
    """Property-based tests for cascade delete behavior."""

    @given(
        org_name=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
        num_projects=st.integers(min_value=1, max_value=5),
    )
    @settings(max_examples=100, deadline=None)
    def test_organization_delete_cascades_to_projects(self, org_name, num_projects):
        """
        **Feature: project-management-system, Property 4: Cascade Delete Integrity**
        **Validates: Requirements 2.4**
        
        For any organization with projects, deleting the organization shall 
        result in zero projects remaining for that organization.
        """
        # Create organization with unique slug
        import uuid
        slug = f"test-{uuid.uuid4().hex[:8]}"
        org = Organization.objects.create(
            name=org_name[:100],
            slug=slug,
            contact_email="test@example.com"
        )
        
        # Create projects for this organization
        project_ids = []
        for i in range(num_projects):
            project = Project.objects.create(
                organization=org,
                name=f"Project {i}",
                status=ProjectStatus.ACTIVE
            )
            project_ids.append(project.id)
        
        # Verify projects exist
        assert Project.objects.filter(id__in=project_ids).count() == num_projects
        
        # Delete organization
        org.delete()
        
        # Verify all projects are deleted
        assert Project.objects.filter(id__in=project_ids).count() == 0

    @given(
        project_name=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
        num_tasks=st.integers(min_value=1, max_value=5),
    )
    @settings(max_examples=100, deadline=None)
    def test_project_delete_cascades_to_tasks(self, project_name, num_tasks):
        """
        **Feature: project-management-system, Property 4: Cascade Delete Integrity**
        **Validates: Requirements 3.4**
        
        For any project with tasks, deleting the project shall result in 
        zero tasks remaining for that project.
        """
        import uuid
        slug = f"test-{uuid.uuid4().hex[:8]}"
        org = Organization.objects.create(
            name="Test Org",
            slug=slug,
            contact_email="test@example.com"
        )
        
        project = Project.objects.create(
            organization=org,
            name=project_name[:200],
            status=ProjectStatus.ACTIVE
        )
        
        # Create tasks for this project
        task_ids = []
        for i in range(num_tasks):
            task = Task.objects.create(
                project=project,
                title=f"Task {i}",
                status=TaskStatus.TODO
            )
            task_ids.append(task.id)
        
        # Verify tasks exist
        assert Task.objects.filter(id__in=task_ids).count() == num_tasks
        
        # Delete project
        project.delete()
        
        # Verify all tasks are deleted
        assert Task.objects.filter(id__in=task_ids).count() == 0

    @given(
        task_title=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
        num_comments=st.integers(min_value=1, max_value=5),
    )
    @settings(max_examples=100, deadline=None)
    def test_task_delete_cascades_to_comments(self, task_title, num_comments):
        """
        **Feature: project-management-system, Property 4: Cascade Delete Integrity**
        **Validates: Requirements 4.3**
        
        For any task with comments, deleting the task shall result in 
        zero comments remaining for that task.
        """
        import uuid
        slug = f"test-{uuid.uuid4().hex[:8]}"
        org = Organization.objects.create(
            name="Test Org",
            slug=slug,
            contact_email="test@example.com"
        )
        
        project = Project.objects.create(
            organization=org,
            name="Test Project",
            status=ProjectStatus.ACTIVE
        )
        
        task = Task.objects.create(
            project=project,
            title=task_title[:200],
            status=TaskStatus.TODO
        )
        
        # Create comments for this task
        comment_ids = []
        for i in range(num_comments):
            comment = TaskComment.objects.create(
                task=task,
                content=f"Comment {i}",
                author_email="author@example.com"
            )
            comment_ids.append(comment.id)
        
        # Verify comments exist
        assert TaskComment.objects.filter(id__in=comment_ids).count() == num_comments
        
        # Delete task
        task.delete()
        
        # Verify all comments are deleted
        assert TaskComment.objects.filter(id__in=comment_ids).count() == 0
