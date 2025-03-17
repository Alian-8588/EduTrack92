from django.test import TestCase
from courses.models import Course
from community.models import StudyGroup

class StudyGroupTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title='React', category='Frontend', description='React Basics', instructor='System')

    def test_study_group_creation(self):
        group = StudyGroup.objects.create(course=self.course)
        self.assertEqual(group.course.title, 'React')