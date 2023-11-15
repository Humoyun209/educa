from django.urls import re_path
from chat import consumers


websocket_patterns = [
    re_path('ws/chat/room/(?P<course_id>\d+)/$', 
            consumers.ChatConsumer.as_asgi())
]