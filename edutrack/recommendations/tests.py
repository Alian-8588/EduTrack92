from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from courses.models import Course, StudyGoal
from unittest.mock import patch
from datetime import date

class RecommendationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user2', password='pass1234')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Django Basics', description='Django intro', instructor='John')

        # ✅ 创建学习目标，确保推荐接口有数据
        StudyGoal.objects.create(user=self.user, course=self.course, target_date=date.today(), progress=0.0)

    @patch('openai.ChatCompletion.create')
    def test_ai_recommendation(self, mock_openai):
        # ✅ 模拟 OpenAI 返回结果（根据你接口使用 GPT-3.5 的写法）
        mock_openai.return_value = {
            'choices': [{'message': {'content': 'Recommended: Advanced Django'}}]
        }
        response = self.client.get('/api/recommendations/recommend/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('recommended_course', response.data)