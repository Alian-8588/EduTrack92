from rest_framework import serializers
from .models import StudyGroup

class StudyGroupSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    course_title = serializers.CharField(source='course.title', read_only=True)
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'course_title', 'description', 'is_member']

    def get_name(self, obj):
        return str(obj)  # 返回 __str__ 方法的内容

    def get_is_member(self, obj):
        user = self.context.get('request').user
        return user in obj.members.all()
