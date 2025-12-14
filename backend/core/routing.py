"""WebSocket routing for GraphQL subscriptions."""
from django.urls import path
from core.consumers import GraphQLSubscriptionConsumer

websocket_urlpatterns = [
    path('graphql/', GraphQLSubscriptionConsumer.as_asgi()),
]
