from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'events/list.html'


class NewEventView(LoginRequiredMixin, CreateView):
    pass


class EditEventView(LoginRequiredMixin, UpdateView):
    pass
