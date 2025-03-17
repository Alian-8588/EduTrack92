"""
URL configuration for edutrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include  # ✅ 添加 include
from users.views import RegisterView  # ✅ 添加这行，确保导入
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.urls import path
from django.views.generic import TemplateView
from django.urls import path
from users.views import home_view, dashboard_view, faq_view, user_center_view
from courses.views import learning_hub_view
from community.views import community_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('users.urls')),  # ✅ 确保包含 users.urls
    path('register/', RegisterView.as_view(), name='register'),
    path('api/courses/', include('courses.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # ✅ 获取 access 和 refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # ✅ 刷新 access token
    path('api/recommendations/', include('recommendations.urls')),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # <-- 添加这个
    path('', include('users.urls')),
    path('dashboard', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('learning/', learning_hub_view, name='learning_hub'),
    path('community/', community_view, name='community'),
    path('user/', user_center_view, name='user_center'),
    path('users/', include('users.urls')),
    path('faq/', faq_view, name='faq'),
    path('accounts/', include('allauth.urls')),
    path('api/community/', include('community.urls')),
    path('api/analytics/', include('analytics.urls')),
]
