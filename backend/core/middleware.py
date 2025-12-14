"""Multi-tenancy middleware for organization context."""
from django.http import JsonResponse


class OrganizationMiddleware:
    """Middleware to extract and validate organization context from requests."""
    
    EXEMPT_PATHS = ['/health/', '/admin/', '/graphql/']
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip middleware for exempt paths
        if any(request.path.startswith(path) for path in self.EXEMPT_PATHS):
            # Still extract org slug if present for GraphQL
            org_slug = request.headers.get('X-Organization-Slug')
            request.organization_slug = org_slug
            return self.get_response(request)
        
        org_slug = request.headers.get('X-Organization-Slug')
        if not org_slug:
            return JsonResponse(
                {'error': 'X-Organization-Slug header is required'},
                status=400
            )
        
        request.organization_slug = org_slug
        return self.get_response(request)
