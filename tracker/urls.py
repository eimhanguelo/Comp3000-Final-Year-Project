from django.urls import path
from .views import TrackerCreateView, TrackerUpdateView, TrackerListView, TrackerDetailView, TrackerDeleteView  # Import TrackerDeleteView

urlpatterns = [
    path('tracker/create/', TrackerCreateView.as_view(), name='tracker_create'),
    path('tracker/update/<int:pk>/', TrackerUpdateView.as_view(), name='tracker_update'),
    path('tracker/list/', TrackerListView.as_view(), name='tracker_list'),  # List view for trackers
    path('tracker/detail/<int:pk>/', TrackerDetailView.as_view(), name='tracker_detail'),
    path('tracker/delete/<int:pk>/', TrackerDeleteView.as_view(), name='tracker_delete'),  # Now properly use TrackerDeleteView

]
