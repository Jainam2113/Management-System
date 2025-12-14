"""
Property-based tests for email format validation.

**Feature: project-management-system, Property 5: Email Format Validation**
**Validates: Requirements 3.5, 4.4**

For any string provided as assignee_email or author_email, the system shall 
accept it if and only if it matches a valid email format.
"""
import pytest
from hypothesis import given, strategies as st, settings
from hypothesis.strategies import emails
from django.test import TransactionTestCase
from django.core.exceptions import ValidationError
from core.models import Organization, Project, Task, TaskComment, ProjectStatus, TaskStatus


class TestEmailFormatValidation(TransactionTestCase):
    """Property-based tests for email format validation."""

    @given(
        email=emails(),
    )
    @settings(max_examples=100, deadline=None)
    def test_valid_email_accepted_for_task_assignee(self, email):
        """
        **Feature: project-management-system, Property 5: Email Format Validation**
        **Validates: Requirements 3.5**
        
        For any valid email format, the system shall accept it as assignee_email.
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
        
        # Should not raise an exception
        task = Task.objects.create(
            project=project,
            title="Test Task",
            status=TaskStatus.TODO,
            assignee_email=email
        )
        
        assert task.assignee_email == email

    @given(
        invalid_email=st.text(min_size=1, max_size=50).filter(
            lambda x: x.strip() and '@' not in x
        ),
    )
    @settings(max_examples=100, deadline=None)
    def test_invalid_email_rejected_for_task_assignee(self, invalid_email):
        """
        **Feature: project-management-system, Property 5: Email Format Validation**
        **Validates: Requirements 3.5**
        
        For any invalid email format (no @), the system shall reject it.
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
        
        task = Task(
            project=project,
            title="Test Task",
            status=TaskStatus.TODO,
            assignee_email=invalid_email
        )
        
        # full_clean should raise ValidationError for invalid email
        with pytest.raises(ValidationError):
            task.full_clean()

    @given(
        email=emails(),
    )
    @settings(max_examples=100, deadline=None)
    def test_valid_email_accepted_for_comment_author(self, email):
        """
        **Feature: project-management-system, Property 5: Email Format Validation**
        **Validates: Requirements 4.4**
        
        For any valid email format, the system shall accept it as author_email.
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
        
        # Should not raise an exception
        comment = TaskComment.objects.create(
            task=task,
            content="Test comment",
            author_email=email
        )
        
        assert comment.author_email == email

    @given(
        invalid_email=st.text(min_size=1, max_size=50).filter(
            lambda x: x.strip() and '@' not in x
        ),
    )
    @settings(max_examples=100, deadline=None)
    def test_invalid_email_rejected_for_comment_author(self, invalid_email):
        """
        **Feature: project-management-system, Property 5: Email Format Validation**
        **Validates: Requirements 4.4**
        
        For any invalid email format (no @), the system shall reject it.
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
        
        comment = TaskComment(
            task=task,
            content="Test comment",
            author_email=invalid_email
        )
        
        # full_clean should raise ValidationError for invalid email
        with pytest.raises(ValidationError):
            comment.full_clean()
