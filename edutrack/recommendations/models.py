from django.db import models
from users.models import CustomUser

class AIRecommendation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recommended_course = models.TextField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.recommended_course}"