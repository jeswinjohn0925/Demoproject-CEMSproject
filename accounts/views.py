from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from events.models import Event, EventRegistration

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.profile.user_type == 'user':
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or access denied')
    return render(request, 'accounts/user_login.html')

def coordinator_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.profile.user_type == 'coordinator':
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or access denied')
    return render(request, 'accounts/coordinator_login.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.profile.user_type == 'admin':
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or access denied')
    return render(request, 'accounts/admin_login.html')

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/user_register.html', {'form': form})

def coordinator_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.user_type = 'coordinator'
            user.profile.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/coordinator_register.html', {'form': form})

@never_cache
def logout_view(request):
    logout(request)
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    response = redirect('home')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
@never_cache
def dashboard(request):
    user_type = request.user.profile.user_type
    if user_type == 'admin':
        return redirect('admin_dashboard')
    elif user_type == 'coordinator':
        return redirect('coordinator_dashboard')
    else:
        return redirect('user_dashboard')

@login_required
@never_cache
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')

@login_required
@never_cache
def coordinator_dashboard(request):
    return render(request, 'accounts/coordinator_dashboard.html')

@login_required
@never_cache
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')

@login_required
@never_cache
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
@never_cache
def manage_users(request):
    if request.user.profile.user_type != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard')
    
    users = User.objects.all().select_related('profile')
    user_count = users.count()
    user_types = users.values('profile__user_type').annotate(count=Count('id'))
    
    context = {
        'users': users,
        'user_count': user_count,
        'user_types': user_types,
    }
    return render(request, 'accounts/manage_users.html', context)

@login_required
@never_cache
def system_reports(request):
    if request.user.profile.user_type != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard')
    
    # User Statistics
    total_users = User.objects.count()
    users_by_type = User.objects.filter(profile__isnull=False).values('profile__user_type').annotate(count=Count('id'))
    
    # Event Statistics
    total_events = Event.objects.count()
    total_registrations = EventRegistration.objects.count()
    
    # Average participants per event
    events_with_reg = Event.objects.annotate(reg_count=Count('eventregistration')).filter(reg_count__gt=0)
    avg_participants = events_with_reg.aggregate(avg=Count('eventregistration') / Count('id'))['avg'] or 0
    
    context = {
        'total_users': total_users,
        'users_by_type': users_by_type,
        'total_events': total_events,
        'total_registrations': total_registrations,
        'avg_participants': round(avg_participants, 2),
    }
    return render(request, 'accounts/system_reports.html', context)
