"""
Property-based tests for status validation.

**Feature: project-management-system, Property 3: Status Validation**
**Validates: Requirements 2.3, 3.3**

For any project status value, the system shall accept it if and only if it is 
one of (ACTIVE, COMPLETED, ON_HOLD). For any task status value, the system 
shall accept it if and only if it is one of (TODO, IN_PROGRESS, DONE).
"""
import pytest
from hypothesis import given, strategies as st, settings
from django.test import TransactionTestCase
from core.models import Organization, Project, Task, ProjectStatus, TaskStatus


# Valid status values
VALID_PROJECT_STATUSES = [s.value for s in ProjectStatus]
VALID_TASK_STATUSES = [s.value for s in TaskStatus]


class TestStatusValidation(TransactionTestCase):
    """Property-based tests for status validation."""

    @given(
        status=st.sampled_from(VALID_PROJECT_STATUSES),
    )
    @settings(max_examples=100, deadline=None)
    def test_valid_project_status_accepted(self, status):
        """
        **Feature: project-management-system, Property 3: Status Validation**
        **Validates: Requirements 2.3**
        
        For any valid project status, the system shall accept it.
        """
        import uuid
        
        slug = f"org-{uuid.uuid4().hex[:8]}"
        org = Organization.objects.create(
            name="Test Org",
            slug=slug,
            contact_email="test@example.com"
        )
        
        # Should not raise an exception
        project = Project.objects.create(
            organization=org,
            name="Test Project",
            status=status
        )
        
        assert project.status == status
        assert project.status in VALID_PROJECT_STATUSES

    @given(
        invalid_status=st.text(min_size=1, max_size=20).filter(
            lambda x: x.strip() and x not in VALID_PROJECT_STATUSES
        ),
    )
    @settings(max_examples=100, deadline=None)
    def test_invalid_project_status_rejected(self, invalid_status):
        """
        **Feature: project-management-system, Property 3: Status Validation**
        **Validates: Requirements 2.3**
        
        For any invalid project status, the system shall reject it.
        """
        import uuid
        from django.core.exceptions import ValidationError
        
        slug = f"org-{uuid.uuid4().hex[:8]}"
        org = Organization.objects.create(
            name="Test Org",
            slug=slug,
            contact_email="test@example.com"
        )
        
        project = Project(
            organization=org,
            name="Test Project",
            status=invalid_status
        )
        
        # full_clean should raise ValidationError for invalid status
        with pytest.raises(ValidationError):
            project.full_clean()

    @given(
        status=st.sampled_from(VALID_TASK_STATUSES),
    )
    @settings(max_examples=100, deadline=None)
    def test_valid_task_status_accepted(self, status):
        """
        **Feature: project-management-system, Property 3: Status Validation**
        **Validates: Requirements 3.3**
        
        For any valid task status, the system shall accept it.
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
            status=status
        )
        
        assert task.status == status
        assert task.status in VALID_TASK_STATUSES

    @given(
        invalid_status=st.text(min_size=1, max_size=20).filter(
            lambda x: x.strip() and x not in VALID_TASK_STATUSES
        ),
    )
    @settings(max_examples=100, deadline=None)
    def test_invalid_task_status_rejected(self, invalid_status):
        """
        **Feature: project-management-system, Property 3: Status Validation**
        **Validates: Requirements 3.3**
        
        For any invalid task status, the system shall reject it.
        """
        import uuid
        from django.core.exceptions import ValidationError
        
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
            status=invalid_status
        )
        
        # full_clean should raise ValidationError for invalid status
        with pytest.raises(ValidationError):
            task.full_clean()
