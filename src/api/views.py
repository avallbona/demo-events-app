from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.serializers import EventSerializer
from events.models import Event, EventAttendee


class EventApiViewSet(
    LoginRequiredMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        """overwritten queryset in order to only allow
        modification/deletion of an event by its owner"""
        if self.request.method in ["PATCH", "PUT", "DELETE"]:
            return super().get_queryset().filter(owner=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        """when creating an event always setting the user as owner"""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='sign-in')
    def sign_in(self, request, pk):
        """signing in into an event"""
        event = get_object_or_404(Event, pk=pk)
        if EventAttendee.objects.filter(event=event, user=request.user).exists():
            return Response(
                data={"status": "already signed in"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        EventAttendee.objects.create(event=event, user=request.user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def withdraw(self, request, pk):
        """withdrawing from an event"""
        event = get_object_or_404(Event, pk=pk)
        qs = EventAttendee.objects.filter(event=event, user=request.user)
        if not qs.exists():
            return Response(
                data={"status": "not signed in"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
