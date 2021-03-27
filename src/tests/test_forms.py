from datetime import timedelta

from django.utils import timezone

from events import SIGNUP, WITHDRAW
from events.forms import ActionForm, EditForm
from events.models import Event, EventAttendee

offset = timedelta(days=1)
now = timezone.now()
next_day = now + offset
past_day = now - offset


def test_edit_form_is_valid(my_user):
    data = {
        "title": "title event",
        "description": "description event",
        "owner": my_user,
        "event_date": next_day,
    }
    form = EditForm(data)
    assert form.is_valid()

    event = form.save()
    assert isinstance(event, Event)


def test_edit_form_not_valid_date(my_user):
    data = {
        "title": "title event",
        "description": "description event",
        "owner": my_user,
        "event_date": past_day,
    }
    form = EditForm(data)
    assert not form.is_valid()
    assert "event_date" in form.errors


def test_action_form_sign_in_ok(single_event, my_user):
    send_data = {"event_id": single_event.pk, "action": SIGNUP}
    form = ActionForm(data=send_data, user=my_user)
    assert form.is_valid()


def test_action_form_already_signed_in(single_event, my_user):
    EventAttendee.objects.create(event=single_event, user=my_user)
    send_data = {"event_id": single_event.pk, "action": SIGNUP}
    form = ActionForm(data=send_data, user=my_user)
    assert not form.is_valid()
    assert "already signed" in str(form.errors).lower()


def test_action_form_withdraw_ok(single_event, my_user):
    EventAttendee.objects.create(event=single_event, user=my_user)
    send_data = {"event_id": single_event.pk, "action": WITHDRAW}
    form = ActionForm(data=send_data, user=my_user)
    assert form.is_valid()


def test_action_form_already_withdrawed(single_event, my_user):
    send_data = {"event_id": single_event.pk, "action": WITHDRAW}
    form = ActionForm(data=send_data, user=my_user)
    assert not form.is_valid()
    assert "already withdrawed" in str(form.errors).lower()


def test_action_form_wrong_action(single_event, my_user):
    send_data = {"event_id": single_event.pk, "action": "WRONG_ACTION"}
    form = ActionForm(data=send_data, user=my_user)
    assert not form.is_valid()
    assert "select a valid choice" in str(form.errors).lower()
