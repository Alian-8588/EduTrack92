from django.urls import path
from .views import (
    CourseListView,
    StudyGoalCreateView,
    StudyGoalListView,
    StudyGoalUpdateDeleteView,
    learning_hub_view
)

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),         # 获取课程
    path('goals/', StudyGoalListView.as_view(), name='goal-list'),         # 获取目标
    path('goals/create/', StudyGoalCreateView.as_view(), name='goal-create'),  # 添加目标
    path('goals/<int:pk>/', StudyGoalUpdateDeleteView.as_view(), name='goal-update-delete'),  # ✅ 更新&删除
    path('learning-hub/', learning_hub_view, name='learning-hub'),         # 页面渲染
]
