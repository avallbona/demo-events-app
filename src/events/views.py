from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import FormMixin

from events import SIGNUP, WITHDRAW
from events.forms import ActionForm, EditForm
from events.models import Event, EventAttendee


class EditEventMixin:
    """
    common attributes por new and edit event view
    """

    template_name = "events/edit.html"
    model = Event
    form_class = EditForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        """
        overwriting form valid in order to assure
        the owner of the event will be the logged user
        and avoid a possible form manipulation

        :param form:
        :return:
        """
        ret = super().form_valid(form)
        self.object.owner = self.request.user
        self.object.save()
        return ret

    def get_success_url(self):
        """
        after adding or modifying an event
        we go to edit event view

        :return:
        """
        return reverse_lazy("edit-event", kwargs={"pk": self.object.id})


class HomeView(LoginRequiredMixin, ListView):
    """
    home view, list paginated events
    """

    template_name = "events/list.html"
    queryset = Event.actives.all().order_by("event_date")
    paginate_by = 10


class NewEventView(LoginRequiredMixin, SuccessMessageMixin, EditEventMixin, CreateView):
    """
    new event view, available for any logged user
    """

    success_message = _("Event created successfully")

    def get_initial(self):
        initial = super().get_initial()
        initial["owner"] = self.request.user
        return initial


class EditEventView(
    LoginRequiredMixin, SuccessMessageMixin, EditEventMixin, UpdateView
):
    """
    edit event view with the restriction edition of own events
    """

    success_message = _("Event Updated successfully")

    def get_queryset(self):
        """
        overwrite of the queryset method in order
        to avoid the edition of another user event

        :return:
        """
        return super().get_queryset().filter(owner=self.request.user)


class DetailEventView(LoginRequiredMixin, SuccessMessageMixin, FormMixin, DetailView):
    """
    view that manages the view of the event detail
    and the actions to be taken on it, signup and withdraw
    """

    template_name = "events/detail.html"
    queryset = Event.actives.all()
    form_class = ActionForm
    success_url = reverse_lazy("home")

    @property
    def event_id(self):
        return self.kwargs.get("pk")

    @property
    def already_signed_for_event(self):
        return EventAttendee.objects.filter(
            user=self.request.user, event_id=self.event_id
        ).exists()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["already_signed_to_event"] = self.already_signed_for_event
        return ctx

    def get_initial(self):
        """
        overwrite initial in order to inject
        the proper action into the form

        :return:
        """
        initial = super().get_initial()
        initial["action"] = WITHDRAW if self.already_signed_for_event else SIGNUP
        initial["event_id"] = self.event_id
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        event_id = form.cleaned_data["event_id"]
        action = form.cleaned_data["action"]
        if action == SIGNUP:
            event_attendee, created = EventAttendee.objects.get_or_create(
                user=self.request.user, event_id=event_id
            )
            if created:
                self.success_message = _(
                    f"Signed to event {event_attendee.event.title} successfully"
                )
            else:
                self.success_message = _(
                    f"Already signed to {event_attendee.event.title}"
                )
        elif action == WITHDRAW:
            try:
                event_attendee = EventAttendee.objects.get(
                    event_id=event_id, user=self.request.user
                )
                self.success_message = _(
                    f"Withdrawed from event {event_attendee.event.title} successfully"
                )
                event_attendee.delete()
            except EventAttendee.DoesNotExist:
                try:
                    event = Event.objects.get(pk=event_id)
                    title = event.title
                except Event.DoesNotExist:
                    title = ""
                self.success_message = _(f"Already withdrawed from event {title}")
        else:
            self.success_message = _("Wrong action")
        self.success_url = reverse_lazy("detail-event", kwargs={"pk": event_id})

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            self.object = Event.objects.get(pk=self.event_id)
            return self.form_invalid(form)
