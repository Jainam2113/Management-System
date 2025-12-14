"""Management command to seed the database with sample data."""
from django.core.management.base import BaseCommand
from core.models import Organization, Project, Task, TaskComment, ProjectStatus, TaskStatus


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create organizations
        demo_org, created = Organization.objects.get_or_create(
            slug='demo-org',
            defaults={
                'name': 'Demo Organization',
                'contact_email': 'demo@example.com'
            }
        )
        if created:
            self.stdout.write(f'Created organization: {demo_org.name}')
        
        acme_org, created = Organization.objects.get_or_create(
            slug='acme-corp',
            defaults={
                'name': 'Acme Corporation',
                'contact_email': 'contact@acme.com'
            }
        )
        if created:
            self.stdout.write(f'Created organization: {acme_org.name}')
        
        # Create projects for Demo Organization
        projects_data = [
            {
                'name': 'Website Redesign',
                'description': 'Complete overhaul of the company website with modern design',
                'status': ProjectStatus.ACTIVE,
            },
            {
                'name': 'Mobile App Development',
                'description': 'Build iOS and Android apps for customer engagement',
                'status': ProjectStatus.ACTIVE,
            },
            {
                'name': 'Q4 Marketing Campaign',
                'description': 'Holiday season marketing initiatives',
                'status': ProjectStatus.COMPLETED,
            },
            {
                'name': 'Infrastructure Upgrade',
                'description': 'Migrate to cloud infrastructure',
                'status': ProjectStatus.ON_HOLD,
            },
        ]
        
        for proj_data in projects_data:
            project, created = Project.objects.get_or_create(
                organization=demo_org,
                name=proj_data['name'],
                defaults={
                    'description': proj_data['description'],
                    'status': proj_data['status'],
                }
            )
            if created:
                self.stdout.write(f'Created project: {project.name}')
                
                # Create tasks for each project
                tasks_data = [
                    {'title': 'Research and Planning', 'status': TaskStatus.DONE},
                    {'title': 'Design Mockups', 'status': TaskStatus.DONE},
                    {'title': 'Development Phase 1', 'status': TaskStatus.IN_PROGRESS},
                    {'title': 'Testing', 'status': TaskStatus.TODO},
                    {'title': 'Deployment', 'status': TaskStatus.TODO},
                ]
                
                for task_data in tasks_data:
                    task, task_created = Task.objects.get_or_create(
                        project=project,
                        title=task_data['title'],
                        defaults={
                            'description': f"Task for {task_data['title']}",
                            'status': task_data['status'],
                            'assignee_email': 'developer@example.com',
                        }
                    )
                    if task_created:
                        # Add a comment to each task
                        TaskComment.objects.create(
                            task=task,
                            content=f"Initial planning for {task_data['title']}",
                            author_email='manager@example.com'
                        )
        
        # Create a project for Acme Corp
        acme_project, created = Project.objects.get_or_create(
            organization=acme_org,
            name='Product Launch',
            defaults={
                'description': 'Launch new product line',
                'status': ProjectStatus.ACTIVE,
            }
        )
        if created:
            self.stdout.write(f'Created project: {acme_project.name}')
            Task.objects.create(
                project=acme_project,
                title='Market Research',
                status=TaskStatus.IN_PROGRESS,
                assignee_email='analyst@acme.com'
            )
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
