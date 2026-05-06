from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    
    # User specific
    path('user/login/', views.user_login, name='user_login'),
    path('user/register/', views.user_register, name='user_register'),
    
    # Coordinator specific
    path('coordinator/login/', views.coordinator_login, name='coordinator_login'),
    path('coordinator/register/', views.coordinator_register, name='coordinator_register'),
    
    # Admin specific
    path('admin_login/', views.admin_login, name='admin_login'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('coordinator-dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('system-reports/', views.system_reports, name='system_reports'),
]