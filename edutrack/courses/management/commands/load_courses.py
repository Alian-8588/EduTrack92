from django.core.management.base import BaseCommand
from courses.models import Course

class Command(BaseCommand):
    help = 'Batch import representative courses (English)'

    def handle(self, *args, **kwargs):
        courses_by_category = {
            'Programming & Development': [
                'Python Basics', 'Django Web Development', 'JavaScript Intro', 'React Frontend Framework',
                'Data Structures & Algorithms'
            ],
            'Data Science & AI': [
                'Machine Learning Basics', 'Deep Learning Practice', 'Data Analysis & Visualization', 'Python for Data Science'
            ],
            'Finance & Business': [
                'Financial Markets Intro', 'Financial Statement Analysis', 'Business Intelligence (BI)', 'Advanced Excel Skills'
            ],
            'Design & Creativity': [
                'Photoshop Basics', 'UI/UX Design Intro', 'Figma Practice', 'Digital Drawing Techniques'
            ],
            'Product & Operations': [
                'Product Management Basics', 'User Growth Strategy', 'Data-Driven Decisions', 'Project Management Practice'
            ]
        }

        created_count = 0

        for category, titles in courses_by_category.items():
            for title in titles:
                if not Course.objects.filter(title=title, category=category).exists():
                    Course.objects.create(
                        title=title,
                        category=category,
                        description=f"{title} course: Suitable for all levels to help you master key skills.",
                        instructor="System Import"
                    )
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully imported {created_count} courses."))
