# -*- encoding: utf-8 -*-

from django.conf.urls import url

from .views import HomeView, NewEventView, EditEventView

urlpatterns = [

    # list events on home
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^new$', NewEventView.as_view(), name='new-event'),
    url(r'^edit/(?P<id>[0-9]+)$', EditEventView.as_view(), name='edit-event'),



]
