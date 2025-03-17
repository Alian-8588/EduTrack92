from django.urls import path
from .views import AIRecommendationView

urlpatterns = [
    path('recommend/', AIRecommendationView.as_view(), name='recommend'),
]