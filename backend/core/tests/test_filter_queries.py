"""
Property-based tests for filter query correctness.

**Feature: project-management-system, Property 9: Filter Query Correctness**
**Validates: Requirements 13.2**

For any filter criteria (status, date range, search text) applied to a query,
all returned results shall match the specified criteria, and no matching 
results shall be excluded.
"""
import pytest
from hypothesis import given, strategies as st, settings
from django.test import TransactionTestCase
from core.models import Organization, Project, Task, TaskComment, ProjectStatus, TaskStatus


class TestFilterQueryCorrectness(TransactionTestCase):
    """Property-based tests for filter query correctness."""

    @given(
        num_projects=st.integers(min_value=3, max_value=10),
        filter_status=st.sampled_from([ProjectStatus.ACTIVE, ProjectStatus.COMPLETED, ProjectStatus.ON_HOLD]),
    )
    @settings(max_examples=100, deadline=None)
    def test_project_status_filter_returns_only_matching(self, num_projects, filter_status):
        """
        **Feature: project-management-system, Property 9: Filter Query Correctness**
        **Validates: Requirements 13.2**
        
        For any status filter, all returned projects shall have that status.
        """
        import uuid
        import random
        
        slug = f"org-{uuid.uuid4().hex[:8]}"
        org = Organization.objects.create(
            name="Test Org",
            slug=slug,
            contact_email="test@example.com"
        )
        
        # Create projects with random statuses
        statuses = [ProjectStatus.ACTIVE, ProjectStatus.COMPLETED, ProjectStatus.ON_HOLD]
        for i in range(num_projects):
            Project.objects.create(
                organization=org,
                name=f"Project {i}",
                status=random.choice(statuses)
            )
        
        # Filter by status
        filtered = Project.objects.for_organization(slug).filter(status=filter_status)
        
        # Verify all returned projects have the correct status
        for project in filtered:
            assert project.status == filter_status, \
                f"Expected status {filter_status}, got {project.status}"

    @given(
        num_projects=st.integers(min_value=3, max_value=10),
        filter_status=st.sampled_from([ProjectStatus.ACTIVE, ProjectStatus.COMPLETED, ProjectStatus.ON_HOLD]),
    )
    @settings(max_examples=100, deadline=None)
    def test_project_status_filter_includes_all_matching(self, num_projects, filter_status):
        """
        **Feature: project-management-system, Property 9: Filter Query Correctness**
        **Validates: Requirements 13.2**
        
        For any status filter, no matching projects shall be excluded.
        """
        import uuid
        import random
        
        slug = f"org-{uuid.uuid4().hex[:8]}"
        org = Organization.objects.create(
            name="Test Org",
            slug=slug,
            contact_email="test@example.com"
        )
        
        # Create projects with random statuses, track expected matches
        statuses = [ProjectStatus.ACTIVE, ProjectStatus.COMPLETED, ProjectStatus.ON_HOLD]
        expected_ids = set()
        for i in range(num_projects):
            status = random.choice(statuses)
            project = Project.objects.create(
                organization=org,
                name=f"Project {i}",
                status=status
            )
            if status == filter_status:
                expected_ids.add(project.id)
        
        # Filter by status
        filtered = Project.objects.for_organization(slug).filter(status=filter_status)
        actual_ids = set(p.id for p in filtered)
        
        # Verify all matching projects are included
        assert actual_ids == expected_ids, \
            f"Expected {len(expected_ids)} projects, got {len(actual_ids)}"

    @given(
        num_tasks=st.integers(min_value=3, max_value=10),
        filter_status=st.sampled_from([TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]),
    )
    @settings(max_examples=100, deadline=None)
    def test_task_status_filter_correctness(self, num_tasks, filter_status):
        """
        **Feature: project-management-system, Property 9: Filter Query Correctness**
        **Validates: Requirements 13.2**
        
        For any task status filter, all returned tasks shall have that status
        and no matching tasks shall be excluded.
        """
        import uuid
        import random
        
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
        
        # Create tasks with random statuses
        statuses = [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]
        expected_ids = set()
        for i in range(num_tasks):
            status = random.choice(statuses)
            task = Task.objects.create(
                project=project,
                title=f"Task {i}",
                status=status
            )
            if status == filter_status:
                expected_ids.add(task.id)
        
        # Filter by status
        filtered = Task.objects.for_project(project.id).filter(status=filter_status)
        actual_ids = set(t.id for t in filtered)
        
        # Verify correctness
        assert actual_ids == expected_ids
        for task in filtered:
            assert task.status == filter_status

    @given(
        search_term=st.text(min_size=3, max_size=10, alphabet=st.characters(whitelist_categories=('L',))),
    )
    @settings(max_examples=100, deadline=None)
    def test_search_filter_returns_matching_projects(self, search_term):
        """
        **Feature: project-management-system, Property 9: Filter Query Correctness**
        **Validates: Requirements 13.2**
        
        For any search text, all returned projects shall contain that text
        in their name or description.
        """
        import uuid
        from django.db.models import Q
        
        slug = f"org-{uuid.uuid4().hex[:8]}"
        org = Organization.objects.create(
            name="Test Org",
            slug=slug,
            contact_email="test@example.com"
        )
        
        # Create projects - some with search term, some without
        Project.objects.create(
            organization=org,
            name=f"Project with {search_term} in name",
            status=ProjectStatus.ACTIVE
        )
        Project.objects.create(
            organization=org,
            name="Other Project",
            description=f"Has {search_term} in description",
            status=ProjectStatus.ACTIVE
        )
        Project.objects.create(
            organization=org,
            name="Unrelated Project",
            description="No match here",
            status=ProjectStatus.ACTIVE
        )
        
        # Search
        filtered = Project.objects.for_organization(slug).filter(
            Q(name__icontains=search_term) | Q(description__icontains=search_term)
        )
        
        # Verify all results contain the search term
        for project in filtered:
            assert (search_term.lower() in project.name.lower() or 
                    search_term.lower() in project.description.lower()), \
                f"Project {project.name} doesn't contain search term {search_term}"
