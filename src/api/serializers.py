from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    num_attendees = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        exclude = ("owner",)

    @staticmethod
    def validate_event_date(value):
        if value < timezone.now().date():
            raise ValidationError(_("not allowed to create events in the past"))
        return value

    @staticmethod
    def get_num_attendees(obj):
        try:
            return obj.num_attendees
        except AttributeError:
            return 0
