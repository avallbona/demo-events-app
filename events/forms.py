from datetime import datetime as dt

from django import forms
from django.core.exceptions import ValidationError
from django.forms import HiddenInput
from django.utils.translation import ugettext_lazy as _

from events import SIGNUP, WITHDRAW
from events.models import Event, EventAttendee


class EditForm(forms.ModelForm):

    event_date = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = Event
        fields = ('title', 'description', 'event_date', 'owner')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].widget = HiddenInput()

    def clean_event_date(self):
        if self.cleaned_data['event_date'] < dt.now().date():
            raise ValidationError(_("Event date can't be lower than the current date"))
        return self.cleaned_data['event_date']


class ActionForm(forms.Form):
    event_id = forms.CharField(required=True, widget=forms.HiddenInput())
    action = forms.ChoiceField(
        required=True, widget=forms.HiddenInput(),
        choices=(
            (SIGNUP, SIGNUP),
            (WITHDRAW, WITHDRAW),
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')

        if action not in [SIGNUP, WITHDRAW]:
            raise ValidationError(_('Wrong action'))

        event_id = cleaned_data.get('event_id')
        already_signed = EventAttendee.objects.filter(user=self.user, event_id=event_id).exists()

        if action == SIGNUP and already_signed:
            raise ValidationError(_('Wrong action, already signed'))
        elif action == WITHDRAW and not already_signed:
            raise ValidationError(_('Wrong action, already withdrawed'))
