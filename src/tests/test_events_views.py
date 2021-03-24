from django.urls import reverse


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


def test_edit_other_event(my_client, other_single_event):
    url = reverse("edit-event", kwargs={"pk": other_single_event.pk})
    response = my_client.get(url)
    assert response.status_code == 404


def test_add_new_event(my_client, single_event):
    url = reverse("new-event")
    response = my_client.get(url)
    assert response.status_code == 200
