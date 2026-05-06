from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/register/', views.register_for_event, name='register_for_event'),
    path('my-events/', views.my_events, name='my_events'),
    path('create-event/', views.create_event, name='create_event'),
    path('my-organized-events/', views.my_organized_events, name='my_organized_events'),
]