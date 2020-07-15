from django import forms
from django.forms import HiddenInput

from events import SIGNUP, WITHDRAW
from events.models import Event


class EditForm(forms.ModelForm):

    event_date = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = Event
        fields = ('title', 'description', 'event_date', 'owner')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].widget = HiddenInput()


class ActionForm(forms.Form):
    event_id = forms.CharField(required=True, widget=forms.HiddenInput())
    action = forms.ChoiceField(
        required=True, widget=forms.HiddenInput(),
        choices=(
            (SIGNUP, SIGNUP),
            (WITHDRAW, WITHDRAW),
        )
    )
