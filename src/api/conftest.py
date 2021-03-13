import pytest
from model_bakery import baker, seq

from events.models import Event


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
    return baker.make(Event, title=seq("Title "), owner=my_user, _quantity=3)


@pytest.fixture
def single_event(my_user):
    return baker.make(
        Event, title="Title 1", description="description 1", owner=my_user
    )


@pytest.fixture
def other_events():
    return baker.make(Event, title=seq("Title "), _quantity=3)


@pytest.fixture
def other_single_event():
    return baker.make(Event, title="Title 1", description="description 1")
