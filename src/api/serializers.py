from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ("owner",)

    @staticmethod
    def validate_event_date(value):
        if value < timezone.now().date():
            raise ValidationError(_("not allowed to create events in the past"))
        return value


