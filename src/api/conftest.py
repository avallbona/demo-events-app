from datetime import datetime

import pytest
from django.utils import timezone
from model_bakery import baker, seq

from events.models import Event

today = timezone.now().date()
default_date = datetime(today.year, today.month, today.day + 1, hour=13, minute=0)


@pytest.fixture
def my_user(django_user_model):
    username = "user1"
    password = "bar"
    yield django_user_model.objects.create_user(username=username, password=password)


@pytest.fixture
def my_client(client, my_user):
    client.force_login(my_user)
    return client


@pytest.fixture
def events(my_user):
    return baker.make(
        Event, title=seq("Title "), owner=my_user, event_date=default_date, _quantity=3
    )


@pytest.fixture
def single_event(my_user):
    return baker.make(
        Event,
        title="Title 1",
        description="description 1",
        owner=my_user,
        event_date=default_date,
    )


@pytest.fixture
def other_events():
    return baker.make(Event, title=seq("Title "), event_date=default_date, _quantity=3)


@pytest.fixture
def other_single_event():
    return baker.make(
        Event, title="Title 1", description="description 1", event_date=default_date
    )
