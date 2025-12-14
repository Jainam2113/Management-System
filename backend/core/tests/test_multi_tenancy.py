"""
Property-based tests for multi-tenant data isolation.

**Feature: project-management-system, Property 2: Multi-Tenant Data Isolation**
**Validates: Requirements 1.2, 2.5, 5.8, 6.1, 6.2, 6.3, 6.4, 6.5**

For any organization and any query operation, the system shall only return 
resources (projects, tasks, comments) that belong to that organization's 
hierarchy. Resources from other organizations shall never be included.
"""
import pytest
from hypothesis import given, strategies as st, settings
from django.test import TransactionTestCase
from core.models import Organization, Project, Task, TaskComment, ProjectStatus, TaskStatus


class TestMultiTenantDataIsolation(TransactionTestCase):
    """Property-based tests for multi-tenant data isolation."""

    @given(
        num_orgs=st.integers(min_value=2, max_value=4),
        projects_per_org=st.integers(min_value=1, max_value=3),
    )
    @settings(max_examples=100, deadline=None)
    def test_project_isolation_by_organization(self, num_orgs, projects_per_org):
        """
        **Feature: project-management-system, Property 2: Multi-Tenant Data Isolation**
        **Validates: Requirements 2.5, 6.2**
        
        For any organization, querying projects shall only return projects 
        belonging to that organization.
        """
        import uuid
        
        # Create multiple organizations with projects
        orgs_data = []
        for i in range(num_orgs):
            slug = f"org-{uuid.uuid4().hex[:8]}"
            org = Organization.objects.create(
                name=f"Org {i}",
                slug=slug,
                contact_email=f"org{i}@example.com"
            )
            project_ids = []
            for j in range(projects_per_org):
                project = Project.objects.create(
                    organization=org,
                    name=f"Project {j}",
                    status=ProjectStatus.ACTIVE
                )
                project_ids.append(project.id)
            orgs_data.append({'org': org, 'project_ids': project_ids})
        
        # For each organization, verify isolation
        for org_data in orgs_data:
            org = org_data['org']
            expected_ids = set(org_data['project_ids'])
            
            # Query projects for this organization
            projects = Project.objects.for_organization(org.slug)
            actual_ids = set(p.id for p in projects)
            
            # Verify only this org's projects are returned
            assert actual_ids == expected_ids, \
                f"Expected {expected_ids}, got {actual_ids}"
            
            # Verify no other org's projects are included
            other_project_ids = set()
            for other_data in orgs_data:
                if other_data['org'].id != org.id:
                    other_project_ids.update(other_data['project_ids'])
            
            assert actual_ids.isdisjoint(other_project_ids), \
                "Projects from other organizations were returned"

    @given(
        num_orgs=st.integers(min_value=2, max_value=3),
        tasks_per_project=st.integers(min_value=1, max_value=3),
    )
    @settings(max_examples=100, deadline=None)
    def test_task_isolation_by_organization(self, num_orgs, tasks_per_project):
        """
        **Feature: project-management-system, Property 2: Multi-Tenant Data Isolation**
        **Validates: Requirements 6.3**
        
        For any organization, querying tasks shall only return tasks from 
        projects belonging to that organization.
        """
        import uuid
        
        # Create organizations with projects and tasks
        orgs_data = []
        for i in range(num_orgs):
            slug = f"org-{uuid.uuid4().hex[:8]}"
            org = Organization.objects.create(
                name=f"Org {i}",
                slug=slug,
                contact_email=f"org{i}@example.com"
            )
            project = Project.objects.create(
                organization=org,
                name=f"Project {i}",
                status=ProjectStatus.ACTIVE
            )
            task_ids = []
            for j in range(tasks_per_project):
                task = Task.objects.create(
                    project=project,
                    title=f"Task {j}",
                    status=TaskStatus.TODO
                )
                task_ids.append(task.id)
            orgs_data.append({'org': org, 'task_ids': task_ids})
        
        # For each organization, verify task isolation
        for org_data in orgs_data:
            org = org_data['org']
            expected_ids = set(org_data['task_ids'])
            
            # Query tasks for this organization
            tasks = Task.objects.for_organization(org.slug)
            actual_ids = set(t.id for t in tasks)
            
            # Verify only this org's tasks are returned
            assert actual_ids == expected_ids
            
            # Verify no other org's tasks are included
            other_task_ids = set()
            for other_data in orgs_data:
                if other_data['org'].id != org.id:
                    other_task_ids.update(other_data['task_ids'])
            
            assert actual_ids.isdisjoint(other_task_ids)

    @given(
        num_orgs=st.integers(min_value=2, max_value=3),
        comments_per_task=st.integers(min_value=1, max_value=3),
    )
    @settings(max_examples=100, deadline=None)
    def test_comment_isolation_by_organization(self, num_orgs, comments_per_task):
        """
        **Feature: project-management-system, Property 2: Multi-Tenant Data Isolation**
        **Validates: Requirements 6.4**
        
        For any organization, querying comments shall only return comments 
        from tasks within that organization's projects.
        """
        import uuid
        
        # Create organizations with projects, tasks, and comments
        orgs_data = []
        for i in range(num_orgs):
            slug = f"org-{uuid.uuid4().hex[:8]}"
            org = Organization.objects.create(
                name=f"Org {i}",
                slug=slug,
                contact_email=f"org{i}@example.com"
            )
            project = Project.objects.create(
                organization=org,
                name=f"Project {i}",
                status=ProjectStatus.ACTIVE
            )
            task = Task.objects.create(
                project=project,
                title=f"Task {i}",
                status=TaskStatus.TODO
            )
            comment_ids = []
            for j in range(comments_per_task):
                comment = TaskComment.objects.create(
                    task=task,
                    content=f"Comment {j}",
                    author_email="author@example.com"
                )
                comment_ids.append(comment.id)
            orgs_data.append({'org': org, 'comment_ids': comment_ids})
        
        # For each organization, verify comment isolation
        for org_data in orgs_data:
            org = org_data['org']
            expected_ids = set(org_data['comment_ids'])
            
            # Query comments for this organization
            comments = TaskComment.objects.for_organization(org.slug)
            actual_ids = set(c.id for c in comments)
            
            # Verify only this org's comments are returned
            assert actual_ids == expected_ids
            
            # Verify no other org's comments are included
            other_comment_ids = set()
            for other_data in orgs_data:
                if other_data['org'].id != org.id:
                    other_comment_ids.update(other_data['comment_ids'])
            
            assert actual_ids.isdisjoint(other_comment_ids)
