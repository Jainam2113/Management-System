"""WebSocket consumer for GraphQL subscriptions."""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class GraphQLSubscriptionConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for handling GraphQL subscriptions."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        self.subscriptions = {}
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        for group_name in self.subscriptions.values():
            await self.channel_layer.group_discard(group_name, self.channel_name)
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        data = json.loads(text_data)
        msg_type = data.get('type')
        
        if msg_type == 'connection_init':
            await self.send(json.dumps({'type': 'connection_ack'}))
        elif msg_type == 'subscribe':
            await self.handle_subscribe(data)
        elif msg_type == 'complete':
            await self.handle_unsubscribe(data)
    
    async def handle_subscribe(self, data):
        """Handle subscription request."""
        sub_id = data.get('id')
        payload = data.get('payload', {})
        query = payload.get('query', '')
        variables = payload.get('variables', {})
        
        # Determine subscription type and group
        if 'taskUpdated' in query:
            project_id = variables.get('projectId')
            group_name = f'project_{project_id}_tasks'
        elif 'commentAdded' in query:
            task_id = variables.get('taskId')
            group_name = f'task_{task_id}_comments'
        else:
            return
        
        self.subscriptions[sub_id] = group_name
        await self.channel_layer.group_add(group_name, self.channel_name)
    
    async def handle_unsubscribe(self, data):
        """Handle unsubscribe request."""
        sub_id = data.get('id')
        if sub_id in self.subscriptions:
            group_name = self.subscriptions.pop(sub_id)
            await self.channel_layer.group_discard(group_name, self.channel_name)
    
    async def subscription_update(self, event):
        """Send subscription update to client."""
        await self.send(json.dumps({
            'type': 'next',
            'id': event.get('subscription_id'),
            'payload': {'data': event.get('data')}
        }))
