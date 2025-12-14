"""URL configuration for project management system."""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt


def health_check(request):
    """Health check endpoint for Docker."""
    return JsonResponse({'status': 'healthy'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('health/', health_check, name='health_check'),
]
