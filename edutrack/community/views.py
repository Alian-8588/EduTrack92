from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StudyGroup
from .serializers import StudyGroupSerializer  # 引入序列化器

# ✅ 页面渲染
def community_view(request):
    return render(request, 'community.html')


# ✅ 小组列表（使用 serializer 返回完整数据）
class StudyGroupListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        groups = StudyGroup.objects.all()
        serializer = StudyGroupSerializer(groups, many=True, context={'request': request})
        return Response(serializer.data)


# ✅ 加入小组
class JoinGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            group = StudyGroup.objects.get(pk=pk)
            group.members.add(request.user)
            return Response({"detail": "已加入小组"})
        except StudyGroup.DoesNotExist:
            return Response({"detail": "小组不存在"}, status=status.HTTP_404_NOT_FOUND)


# ✅ 退出小组
class LeaveGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            group = StudyGroup.objects.get(pk=pk)
            group.members.remove(request.user)
            return Response({"detail": "已退出小组"})
        except StudyGroup.DoesNotExist:
            return Response({"detail": "小组不存在"}, status=status.HTTP_404_NOT_FOUND)
