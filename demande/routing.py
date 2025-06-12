# colis/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/livraison/(?P<livraison_id>\w+)/$', consumers.LivreurTrackingConsumer.as_asgi()),
]