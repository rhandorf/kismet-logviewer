from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path("eventbus/events.ws", consumers.EventbusConsumer.as_asgi()),
]
