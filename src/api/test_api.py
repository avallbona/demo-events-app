from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.reverse import reverse

from events.models import Event, EventAttendee


@pytest.mark.django_db
def test_list_events(my_client, events):
    url = reverse("event-list")
    response = my_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3


def test_list_events_other_user(my_client, other_events):
    url = reverse("event-list")
    response = my_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3


@pytest.mark.django_db
def test_detail_event(my_client, single_event):
    url = reverse("event-detail", kwargs={"pk": single_event.id})
    response = my_client.get(url)
    assert response.status_code == 200
    assert response.data["id"] == single_event.id
    assert response.data["title"] == single_event.title
    assert response.data["description"] == single_event.description


@pytest.mark.django_db
def test_detail_other_event(my_client, other_single_event):
    url = reverse("event-detail", kwargs={"pk": other_single_event.id})
    response = my_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_event(my_client, single_event):
    data = {"title": "new title", "description": "new description"}
    url = reverse("event-detail", kwargs={"pk": single_event.id})
    response = my_client.patch(url, data=data, content_type="application/json")
    assert response.status_code == 200
    assert response.data["title"] == "new title"
    assert response.data["description"] == "new description"


@pytest.mark.django_db
def test_update_other_event(my_client, other_single_event):
    data = {"title": "new title", "description": "new description"}
    url = reverse("event-detail", kwargs={"pk": other_single_event.id})
    response = my_client.patch(url, data=data, content_type="application/json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_add_event(my_client, my_user):
    """test that the user can add an event and that the event owner is the user"""
    data = {
        "title": "new title",
        "description": "new description",
        "event_date": timezone.now().strftime("%Y-%m-%d"),
    }
    url = reverse("event-list")
    response = my_client.post(url, data=data, content_type="application/json")
    assert response.status_code == 201
    assert response.data["title"] == "new title"
    assert response.data["description"] == "new description"
    event = Event.objects.get(title="new title")
    event.owner_id = my_user.id


@pytest.mark.django_db
def test_not_allowed_event_in_the_past(my_client, my_user):
    """test that the user can add an event and that the event owner is the user"""
    data = {
        "title": "new title",
        "description": "new description",
        "event_date": (timezone.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
    }
    url = reverse("event-list")
    response = my_client.post(url, data=data, content_type="application/json")
    assert response.status_code == 400
    assert Event.objects.all().count() == 0
    assert (
        response.json().get("event_date")[0]
        == "not allowed to create events in the past"
    )


@pytest.mark.django_db
def test_delete_event(my_client, single_event):
    """test to delete an owned event"""
    url = reverse("event-detail", kwargs={"pk": single_event.id})
    response = my_client.delete(url)
    assert response.status_code == 204
    assert Event.objects.all().count() == 0


@pytest.mark.django_db
def test_delete_other_event(my_client, other_single_event):
    """test to delete an NON owned event"""
    url = reverse("event-detail", kwargs={"pk": other_single_event.id})
    response = my_client.delete(url)
    assert response.status_code == 404
    assert Event.objects.all().count() == 1


@pytest.mark.django_db
def test_sign_in_event(my_client, single_event, my_user):
    """test sign in an event"""
    url = reverse("event-sign-in", kwargs={"pk": single_event.id})
    response = my_client.post(url)
    assert response.status_code == 200
    assert EventAttendee.objects.filter(user=my_user).count() == 1


@pytest.mark.django_db
def test_sign_in_event_in_an_already_signed_in_event(my_client, single_event, my_user):
    """test sign in an already signed in event"""
    EventAttendee.objects.create(event=single_event, user=my_user)

    url = reverse("event-sign-in", kwargs={"pk": single_event.id})
    response = my_client.post(url)

    assert response.status_code == 400
    assert response.json().get("status") == "already signed in"
    assert EventAttendee.objects.filter(user=my_user, event=single_event).count() == 1


@pytest.mark.django_db
def test_withdraw_event_signed_in(my_client, single_event, my_user):
    """test withdraw from an event signed in"""
    EventAttendee.objects.create(event=single_event, user=my_user)
    url = reverse("event-withdraw", kwargs={"pk": single_event.id})
    response = my_client.delete(url)
    assert response.status_code == 204
    assert EventAttendee.objects.filter(event=single_event, user=my_user).count() == 0


@pytest.mark.django_db
def test_withdraw_event_not_signed_in(my_client, single_event, my_user):
    """test withdraw from an event not signed in"""
    url = reverse("event-withdraw", kwargs={"pk": single_event.id})
    response = my_client.delete(url)
    assert response.status_code == 400
    assert response.json().get("status") == "not signed in"
    assert not EventAttendee.objects.filter(event=single_event, user=my_user).exists()
