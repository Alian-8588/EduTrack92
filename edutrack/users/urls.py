from .views import RegisterView  # ✅ 确保 RegisterView 在 views.py 里存在
from django.urls import path
from .views import dashboard_view
from django.contrib.auth import views as auth_views
from .views import custom_logout
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('password/change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),
    path('logout/', custom_logout, name='logout'),
    path(
        'users/password/change/',
        auth_views.PasswordChangeView.as_view(template_name='password_change.html', success_url='/accounts/login/'),
        name='password_change'
    ),
]