from django.contrib import admin
from django.db.models import Count

from events.models import Event, EventAssistant


class EventAssistantInline(admin.TabularInline):
    model = EventAssistant


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'num_assistants')
    inlines = [EventAssistantInline, ]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(num_assistants=Count('assistants'))

    @staticmethod
    def num_assistants(obj):
        return obj.num_assistants
