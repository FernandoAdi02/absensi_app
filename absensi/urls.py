from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('attendance/', views.do_attendance, name='attendance'),
    path('profile/', views.profile, name='profile'),
    path('profile/detail/', views.profile_detail, name='profile_detail'),
    path('profile/password/', views.change_password, name='change_password'),
    path('notifications/', views.notifications, name='notifications'),
    path('history/', views.history, name='history'),
    path('leave/', views.leave_request, name='leave_request'),
    path('register/', views.register, name='register'),
    path('login/', csrf_exempt(auth_views.LoginView.as_view(template_name='registration/login.html')), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
