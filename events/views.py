from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Event, EventRegistration
from .forms import EventForm

@login_required
def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registration = EventRegistration.objects.filter(event=event, user=request.user).first()
    is_registered = registration is not None
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered,
        'registration': registration,
    })

@login_required
def register_for_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Prevent admin and coordinator from registering for events
    if request.user.profile.user_type in ['admin', 'coordinator']:
        messages.error(request, 'Your role does not allow event registration.')
        return redirect('event_detail', pk=pk)
    
    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, 'You are already registered for this event.')
    else:
        next_number = EventRegistration.objects.filter(event=event).count() + 1
        chest_number = f"{event.pk:03d}-{next_number:03d}"
        EventRegistration.objects.create(event=event, user=request.user, chest_number=chest_number)
        messages.success(request, f'Successfully registered for the event! Your chest number is {chest_number}.')
    return redirect('event_detail', pk=pk)

@login_required
def my_events(request):
    registrations = EventRegistration.objects.filter(user=request.user).select_related('event')
    return render(request, 'events/my_events.html', {'registrations': registrations})

@login_required
def create_event(request):
    if request.user.profile.user_type != 'coordinator':
        messages.error(request, 'You do not have permission to create events.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def my_organized_events(request):
    if request.user.profile.user_type != 'coordinator':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    events = Event.objects.filter(organizer=request.user).order_by('date')
    return render(request, 'events/my_organized_events.html', {'events': events})
