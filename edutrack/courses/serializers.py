
from .models import Course, LearningProgress
from rest_framework import serializers
from .models import Course, StudyGoal

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class LearningProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningProgress
        fields = '__all__'

# 学习目标序列化器
class StudyGoalSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    target_date = serializers.DateField(required=False)

    class Meta:
        model = StudyGoal
        fields = ['id', 'course', 'course_title', 'target_date', 'progress', 'days_remaining']
        read_only_fields = ['id', 'course_title', 'days_remaining']