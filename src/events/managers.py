from datetime import datetime as dt

from django.db.models import Count, Manager


class ActiveManager(Manager):
    def get_queryset(self):
        """
        return only the upcoming events

        :return:
        """
        return (
            super()
            .get_queryset()
            .filter(event_date__gte=dt.now())
            .annotate(num_attendees=Count("attendees"))
            .select_related("owner")
        )
