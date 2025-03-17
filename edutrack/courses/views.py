from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Course, StudyGoal
from .serializers import CourseSerializer, StudyGoalSerializer
from datetime import date

# ✅ Learning Hub 页面渲染
def learning_hub_view(request):
    return render(request, 'learning_hub.html')

# ✅ 课程列表（下拉）
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

# ✅ 添加学习目标
class StudyGoalCreateView(generics.CreateAPIView):
    serializer_class = StudyGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # 默认目标日期设为今天（如果前端没传）
        if not serializer.validated_data.get('target_date'):
            serializer.save(user=self.request.user, target_date=date.today())
        else:
            serializer.save(user=self.request.user)

# ✅ 获取用户学习目标
class StudyGoalListView(generics.ListAPIView):
    serializer_class = StudyGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudyGoal.objects.filter(user=self.request.user)

# ✅ 更新 + 删除 学习目标（同一个视图）
class StudyGoalUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudyGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudyGoal.objects.filter(user=self.request.user)
