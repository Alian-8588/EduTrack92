from django.core.management.base import BaseCommand
from courses.models import Course
from community.models import StudyGroup

class Command(BaseCommand):
    help = 'Create study groups for each course'

    def handle(self, *args, **kwargs):
        for course in Course.objects.all():
            group, created = StudyGroup.objects.get_or_create(course=course)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Founding Group: {group}'))
            else:
                self.stdout.write(f'Already existing: {group}')
