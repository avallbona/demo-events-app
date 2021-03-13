from rest_framework import viewsets

from api.serializers import EventSerializer
from events.models import Event


class EventApiViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
