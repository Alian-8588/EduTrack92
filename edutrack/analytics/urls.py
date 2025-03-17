# analytics/urls.py
from django.urls import path
from .views import analytics_view, AnalyticsDataView

urlpatterns = [
    path('', analytics_view, name='analytics'),  # 页面展示
    path('data/', AnalyticsDataView.as_view(), name='analytics-data'),  # 数据接口
]
