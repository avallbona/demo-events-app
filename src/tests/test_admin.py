from django.urls import reverse


def test_events_admin(admin_client, events, settings):
    settings.DEBUG = True
    url = reverse("admin:events_event_changelist")
    response = admin_client.get(url)
    assert response.status_code == 200
