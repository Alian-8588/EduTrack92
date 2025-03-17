from django.db import models
from users.models import CustomUser
from courses.models import Course

class StudyGroup(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name='study_groups')
    description = models.TextField(default='欢迎加入学习小组！')

    def __str__(self):
        return f"{self.course.title} 小组"

    def member_count(self):
        return self.members.count()
