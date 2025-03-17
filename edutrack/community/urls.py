from django.urls import path
from .views import (
    community_view,
    StudyGroupListView,
    JoinGroupView,
    LeaveGroupView,
)

urlpatterns = [
    path('groups/', StudyGroupListView.as_view(), name='group-list'),  # 获取小组列表
    path('groups/<int:pk>/join/', JoinGroupView.as_view(), name='group-join'),
    path('groups/<int:pk>/leave/', LeaveGroupView.as_view(), name='group-leave'),
]
