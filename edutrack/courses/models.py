from datetime import date

from django.db import models
from users.models import CustomUser

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, default='编程与开发')
    instructor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"

class StudyGoal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    target_date = models.DateField(null=True, blank=True)
    progress = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.course.title} - {self.progress}%"


class LearningProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)  # 进度 (0~100%)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.progress}%"

class StudyGoal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    target_date = models.DateField()
    progress = models.FloatField(default=0.0)

    def days_remaining(self):
        return (self.target_date - date.today()).days

    def __str__(self):
        return f"{self.course.title} - {self.progress}%"
