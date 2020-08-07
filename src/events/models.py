from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from events.managers import ActiveManager


class Event(models.Model):

    title = models.CharField(max_length=180, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    event_date = models.DateField(verbose_name=_('Date'))
    owner = models.ForeignKey(
        get_user_model(), verbose_name=_('Owner'), on_delete=models.CASCADE, related_name='owner_events'
    )

    objects = models.Manager()
    actives = ActiveManager()

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ('event_date',)

    def __str__(self):
        return f'{self.title} - {self.event_date} - {self.owner.username}'


class EventAttendee(models.Model):
    event = models.ForeignKey(
        Event, verbose_name=_('Event'), related_name='attendees', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        get_user_model(), verbose_name=_('User'), related_name='events', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Attendee')
        verbose_name_plural = _('Attendees')
        unique_together = ('event', 'user')
