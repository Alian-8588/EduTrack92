from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from .models import Course, StudyGoal

class CourseTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user1', password='pass1234')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title='Python 101',
            description='Intro to Python',
            instructor='Jane Doe',
            category='编程与开发'
        )

    def test_list_courses(self):
        response = self.client.get('/api/courses/courses/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Python 101', str(response.data))

    def test_create_study_goal_and_update_progress(self):
        # 创建学习目标
        response = self.client.post('/api/courses/goals/create/', {
            'course': self.course.id,
            'progress': 0.0
        }, format='json')
        self.assertEqual(response.status_code, 201)
        goal_id = response.data['id']

        # 更新进度
        patch_response = self.client.patch(f'/api/courses/goals/{goal_id}/', {
            'progress': 50.0
        }, format='json')
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.data['progress'], 50.0)