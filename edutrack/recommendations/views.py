import openai
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from courses.models import StudyGoal
from .models import AIRecommendation

class AIRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        goals = StudyGoal.objects.filter(user=request.user)
        if not goals.exists():
            return Response({"detail": "No study record, no course recommendation. "}, status=400)

        progress_info = "\n".join(
            f"- {goal.course.title}：{goal.progress}% Done"
            for goal in goals
        )
        prompt = (
            f"The user's learning record is as follows:\n{progress_info}\n"
            f"Please recommend the next course that is suitable for the user based on their interest and learning progress, and explain the reason for the recommendation."
        )

        # ✅ 使用新版 OpenAI 客户端
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

        try:
            chat_response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # 或 "gpt-4"
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            recommended_course = chat_response.choices[0].message.content.strip()

            recommendation = AIRecommendation.objects.create(
                user=request.user,
                recommended_course=recommended_course,
                reason=recommended_course
            )

            return Response({
                "recommended_course": recommendation.recommended_course,
                "reason": recommendation.reason
            })

        except Exception as e:
            return Response({"detail": f"AI recommendation failure: {str(e)}"}, status=500)
