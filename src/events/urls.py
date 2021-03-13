from django.urls import re_path

from .views import HomeView, NewEventView, EditEventView, DetailEventView

urlpatterns = [

    # list events on home
    re_path(r'^$', HomeView.as_view(), name='home'),

    # new event view
    re_path(r'^new$', NewEventView.as_view(), name='new-event'),

    # edit event view
    re_path(r'^edit/(?P<pk>[0-9]+)/$', EditEventView.as_view(), name='edit-event'),

    # detail event, signup and withdraw actions
    re_path(r'^detail/(?P<pk>[0-9]+)/$', DetailEventView.as_view(), name='detail-event'),

]
