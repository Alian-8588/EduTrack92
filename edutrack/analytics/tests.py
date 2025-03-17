from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AnalyticsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='anuser', password='pass123')

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_analytics_data_api(self):
        response = self.client.get('/api/analytics/data/')
        self.assertEqual(response.status_code, 200)

        # 🔹 新接口字段断言
        self.assertIn('total_hours', response.data)
        self.assertIn('recommended', response.data)
        self.assertIn('courses', response.data)  # courses 为列表