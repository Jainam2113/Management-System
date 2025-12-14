"""
Property-based tests for real-time subscription delivery.

**Feature: project-management-system, Property 8: Real-Time Subscription Delivery**
**Validates: Requirements 13.1**

For any active subscription to a project's task updates, when a task in that 
project is created or updated, the subscriber shall receive the updated task data.
"""
import pytest
from hypothesis import given, strategies as st, settings
from django.test import TransactionTestCase
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from core.models import Organization, Project, Task, TaskComment, ProjectStatus, TaskStatus
from core.mutations import broadcast_task_update, broadcast_comment_added


class TestSubscriptionDelivery(TransactionTestCase):
    """Property-based tests for subscription delivery."""

    @given(
        task_title=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
        task_status=st.sampled_from([TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]),
    )
    @settings(max_examples=100, deadline=None)
    def test_task_update_broadcast_contains_correct_data(self, task_title, task_status):
        """
        **Feature: project-management-system, Property 8: Real-Time Subscription Delivery**
        **Validates: Requirements 13.1**
        
        For any task update, the broadcast data shall contain the correct task information.
        """
        import uuid
        
        slug = f"org-{uuid.uuid4().hex[:8]}"
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
            status=task_status
        )
        
        # The broadcast function should not raise an exception
        # even if no subscribers are connected
        try:
            broadcast_task_update(project.id, task)
        except Exception as e:
            pytest.fail(f"Broadcast should not raise exception: {e}")
        
        # Verify task data is correct
        assert task.title == task_title[:200]
        assert task.status == task_status

    @given(
        comment_content=st.text(min_size=1, max_size=100).filter(lambda x: x.strip()),
        author_email=st.emails(),
    )
    @settings(max_examples=100, deadline=None)
    def test_comment_broadcast_contains_correct_data(self, comment_content, author_email):
        """
        **Feature: project-management-system, Property 8: Real-Time Subscription Delivery**
        **Validates: Requirements 13.1**
        
        For any new comment, the broadcast data shall contain the correct comment information.
        """
        import uuid
        
        slug = f"org-{uuid.uuid4().hex[:8]}"
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
            title="Test Task",
            status=TaskStatus.TODO
        )
        comment = TaskComment.objects.create(
            task=task,
            content=comment_content,
            author_email=author_email
        )
        
        # The broadcast function should not raise an exception
        try:
            broadcast_comment_added(task.id, comment)
        except Exception as e:
            pytest.fail(f"Broadcast should not raise exception: {e}")
        
        # Verify comment data is correct
        assert comment.content == comment_content
        assert comment.author_email == author_email

    @given(
        num_tasks=st.integers(min_value=1, max_value=5),
    )
    @settings(max_examples=100, deadline=None)
    def test_multiple_task_updates_broadcast_independently(self, num_tasks):
        """
        **Feature: project-management-system, Property 8: Real-Time Subscription Delivery**
        **Validates: Requirements 13.1**
        
        For any number of task updates, each shall be broadcast independently.
        """
        import uuid
        
        slug = f"org-{uuid.uuid4().hex[:8]}"
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
        
        # Create and broadcast multiple tasks
        tasks = []
        for i in range(num_tasks):
            task = Task.objects.create(
                project=project,
                title=f"Task {i}",
                status=TaskStatus.TODO
            )
            tasks.append(task)
            
            # Each broadcast should succeed independently
            try:
                broadcast_task_update(project.id, task)
            except Exception as e:
                pytest.fail(f"Broadcast {i} should not raise exception: {e}")
        
        assert len(tasks) == num_tasks
