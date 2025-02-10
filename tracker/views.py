from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tracker
from .forms import TrackerForm

# Class-based view to create a new Tracker
class TrackerCreateView(CreateView):
    model = Tracker
    form_class = TrackerForm
    template_name = 'tracker_form.html'  # Template for the form
    success_url = reverse_lazy('tracker_list')  # Redirect to the Tracker list after successful creation

    # Override the form_valid method to set the 'created_by' field
    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Set the logged-in user as the creator
        return super().form_valid(form)

    # Optionally, you can define a custom get_context_data method if you want to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create Tracker'
        return context


# Class-based view to update an existing Tracker
class TrackerUpdateView(UpdateView):
    model = Tracker
    form_class = TrackerForm  # Use the TrackerForm
    template_name = 'tracker_form.html'  # Template for the form
    success_url = reverse_lazy('tracker_list')  # Redirect to the Tracker list after successful update

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update Tracker'
        return context

# Class-based view to list all Trackers
class TrackerListView(ListView):
    model = Tracker
    template_name = 'tracker_list.html'  # Template to display the list of trackers
    context_object_name = 'trackers'  # The name of the context variable
    # paginate_by = 10  # Optional: Number of trackers per page

# Class-based view to display details of a specific Tracker
class TrackerDetailView(DetailView):
    model = Tracker
    template_name = 'tracker_detail.html'  # Template for displaying the details
    context_object_name = 'tracker'  # This defines the name of the object in the template

from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import Tracker
from django.contrib.auth.mixins import LoginRequiredMixin

class TrackerDeleteView(LoginRequiredMixin, DeleteView):
    model = Tracker
    template_name = 'tracker_confirm_delete.html'
    context_object_name = 'tracker'
    success_url = reverse_lazy('tracker_list')
