# -*- encoding: utf-8 -*-

from django.conf.urls import url

from .views import HomeView, NewEventView, EditEventView, DetailEventView

urlpatterns = [

    # list events on home
    url(r'^$', HomeView.as_view(), name='home'),

    # new event view
    url(r'^new$', NewEventView.as_view(), name='new-event'),

    # edit event view
    url(r'^edit/(?P<pk>[0-9]+)/$', EditEventView.as_view(), name='edit-event'),

    # detail event, signup and withdraw actions
    url(r'^detail/(?P<pk>[0-9]+)/$', DetailEventView.as_view(), name='detail-event'),

]
