from django.urls import reverse

from events import SIGNUP, WITHDRAW
from events.models import Event, EventAttendee
from tests.conftest import default_date


def test_home_with_own_editable_events(my_client, events):
    url = reverse("home")
    response = my_client.get(url)
    assert response.status_code == 200
    html = response.content.decode()
    for it in events:
        assert it.title in html
        assert f"edit/{it.pk}" in html
    assert response.context["object_list"].count() == len(events)


def test_home_with_other_non_editable_events(my_client, other_events):
    url = reverse("home")
    response = my_client.get(url)
    assert response.status_code == 200
    html = response.content.decode()
    for it in other_events:
        assert it.title in html
        assert f"edit/{it.pk}" not in html
    assert response.context["object_list"].count() == len(other_events)


def test_home_not_showing_passed_events(my_client, passed_events):
    url = reverse("home")
    response = my_client.get(url)
    assert response.status_code == 200
    html = response.content.decode()
    for it in passed_events:
        assert it.title not in html
        assert f"edit/{it.pk}" not in html
    assert response.context["object_list"].count() == 0


def test_event_detail(my_client, single_event):
    url = reverse("detail-event", kwargs={"pk": single_event.pk})
    response = my_client.get(url)
    assert response.status_code == 200
    html = response.content.decode()

    assert single_event.title in html
    assert single_event.description in html
    assert str(single_event.owner) in html
    assert "Back" in html
    assert "Sign up" in html


def test_passed_event_detail_not_found(my_client, passed_single_event):
    url = reverse("detail-event", kwargs={"pk": passed_single_event.pk})
    response = my_client.get(url)
    assert response.status_code == 404


def test_edit_own_event(my_client, single_event):
    url = reverse("edit-event", kwargs={"pk": single_event.pk})
    response = my_client.get(url)
    assert response.status_code == 200


def test_post_edit_own_event(my_client, single_event, my_user):
    url = reverse("edit-event", kwargs={"pk": single_event.pk})
    new_title, new_desc = ("edited title", "edited description")
    send_data = {
        "title": new_title,
        "description": new_desc,
        "event_date": default_date.strftime("%Y-%m-%d"),
        "owner": my_user.id,
    }
    response = my_client.post(url, data=send_data)
    assert response.status_code == 302
    assert response.url == url
    assert Event.objects.filter(
        owner=my_user, id=single_event.id, title=new_title, description=new_desc
    ).exists()


def test_edit_other_event(my_client, other_single_event):
    url = reverse("edit-event", kwargs={"pk": other_single_event.pk})
    response = my_client.get(url)
    assert response.status_code == 404


def test_add_new_event(my_client, single_event):
    url = reverse("new-event")
    response = my_client.get(url)
    assert response.status_code == 200


def test_post_event_signin(my_client, single_event, my_user):
    url = reverse("detail-event", kwargs={"pk": single_event.pk})
    send_data = {
        "event_id": single_event.id,
        "action": SIGNUP,
    }
    response = my_client.post(url, data=send_data)
    assert response.status_code == 302
    assert EventAttendee.objects.filter(event_id=single_event.id, user=my_user).exists()


def test_post_event_signin_already_existing(my_client, single_event, my_user):
    EventAttendee.objects.create(event=single_event, user=my_user)
    url = reverse("detail-event", kwargs={"pk": single_event.pk})
    send_data = {
        "event_id": single_event.id,
        "action": SIGNUP,
    }
    response = my_client.post(url, data=send_data)
    assert response.status_code == 200
    assert "Wrong action, already signed" in response.content.decode()


def test_post_event_signin_already_existing_overriding_form(
    my_client, single_event, my_user, mocker
):
    mocker.patch("events.forms.ActionForm.is_valid", return_value=True)
    mocker.patch(
        "events.views.DetailEventView.get_data",
        return_value=(single_event.id, SIGNUP),
    )
    EventAttendee.objects.create(event=single_event, user=my_user)
    url = reverse("detail-event", kwargs={"pk": single_event.pk})
    send_data = {
        "event_id": single_event.id,
        "action": SIGNUP,
    }
    response = my_client.post(url, data=send_data)
    assert response.status_code == 302
    # assert "Wrong action, already signed" in response.content.decode()


def test_post_event_withdraw(my_client, single_event, my_user):
    EventAttendee.objects.create(event=single_event, user=my_user)
    url = reverse("detail-event", kwargs={"pk": single_event.pk})
    send_data = {
        "event_id": single_event.id,
        "action": WITHDRAW,
    }
    response = my_client.post(url, data=send_data)
    assert response.status_code == 302
    assert not EventAttendee.objects.filter(
        event_id=single_event.id, user=my_user
    ).exists()


def test_post_event_withdraw_not_existing(my_client, single_event, my_user):
    url = reverse("detail-event", kwargs={"pk": single_event.pk})
    send_data = {
        "event_id": single_event.id,
        "action": WITHDRAW,
    }
    response = my_client.post(url, data=send_data)
    assert response.status_code == 200
    assert "Wrong action, already withdrawed" in response.content.decode()


def test_post_event_withdraw_not_existing_overriding_form(
    my_client, single_event, my_user, mocker
):

    mocker.patch("events.forms.ActionForm.is_valid", return_value=True)
    mocker.patch(
        "events.views.DetailEventView.get_data",
        return_value=(single_event.id, WITHDRAW),
    )

    url = reverse("detail-event", kwargs={"pk": single_event.pk})
    send_data = {
        "event_id": single_event.id,
        "action": WITHDRAW,
    }
    response = my_client.post(url, data=send_data)
    assert response.status_code == 302


def test_post_event_wrong_action(my_client, single_event, my_user, mocker):
    mocker.patch("events.forms.ActionForm.is_valid", return_value=True)
    mocker.patch(
        "events.views.DetailEventView.get_data",
        return_value=(single_event.id, "WRONG_ACTION"),
    )
    url = reverse("detail-event", kwargs={"pk": single_event.pk})
    send_data = {
        "event_id": single_event.id,
        "action": "WRONG_ACTION",
    }
    response = my_client.post(url, data=send_data)
    assert response.status_code == 302
