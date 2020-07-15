from django.contrib import admin
from django.db.models import Count

from events.models import Event, EventAttendee


class EventAttendeeInline(admin.TabularInline):
    model = EventAttendee


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'num_attendees')
    inlines = [EventAttendeeInline, ]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(num_attendees=Count('attendees'))

    @staticmethod
    def num_attendees(obj):
        return obj.num_attendees
