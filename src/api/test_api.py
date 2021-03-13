import pytest
from model_bakery import baker, seq
from rest_framework.reverse import reverse
from events.models import Event


def test_smoke():
    assert True

# todo test 
#   - add event
#   - DONE - detail event
#   - DONE - list events
#   - signup event
#   - withdraw event
#   - delete event


@pytest.fixture
def events():
    return baker.make(Event, title=seq('Title '), _quantity=3)


@pytest.fixture
def single_event():
    return baker.make(Event, title='Title 1', description="description 1")


@pytest.mark.django_db
def test_list_events(client, events):
    url = reverse('event-list')
    response = client.get(url)
    assert response.status_code, 200
    assert len(response.data) == 3


@pytest.mark.django_db
def test_detail_event(client, single_event):
    url = reverse('event-detail', kwargs={'pk': single_event.id})
    response = client.get(url)
    assert response.status_code, 200
    assert response.data['id'] == single_event.id
    assert response.data['title'] == single_event.title
    assert response.data['description'] == single_event.description

