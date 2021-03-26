def test_event_model(single_event):
    assert (
        str(single_event)
        == f"{single_event.title} - {single_event.event_date} - {single_event.owner.username}"
    )
