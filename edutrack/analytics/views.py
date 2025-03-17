# analytics/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from courses.models import Course, StudyGoal
from community.models import StudyGroup
from django.db.models import Count
import math
import random

# ✅ 页面渲染（用于 /api/analytics/）
def analytics_view(request):
    return render(request, 'analytics.html')  # 确保 templates/analytics.html 存在

# ✅ 数据接口（用于 /api/analytics/data/）
class AnalyticsDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1. 获取当前用户的学习目标和进度
        goals = StudyGoal.objects.filter(user=user)
        progress_data = [
            {
                "course": goal.course.title,
                "progress": round(goal.progress, 1)  # 保留1位小数
            }
            for goal in goals
        ]

        # 2. 模拟学习总时长（例如 progress 的总和）
        total_hours = math.ceil(sum(goal.progress for goal in goals))

        # 3. 模拟推荐课程数量（可替换为实际推荐逻辑）
        recommended = random.randint(1, 5)

        # ✅ 返回符合 JS 预期格式
        return Response({
            "total_hours": total_hours,
            "recommended": recommended,
            "courses": progress_data
        })
