from apps.applications.models import (
    AIInterviewSession,
    AIQuestion,
)

from apps.ai.services.llm_service import GeminiService
from apps.ai.services.prompt_service import PromptService


class InterviewService:

    def __init__(self):
        self.llm = GeminiService()

    def generate_questions(self, application, triggered_by):
        """
        Creates interview session and generates AI questions.
        """

        session = AIInterviewSession.objects.create(
            candidate=application.candidate.user,
            job=application.job,
            triggered_by=triggered_by,
            ai_model_used="Gemini 2.5 Flash",
        )

        prompt = PromptService.generate_interview_questions(
            application.job
        )

        response = self.llm.generate_json(prompt)

        questions = response.get("questions", [])

        for item in questions:

            AIQuestion.objects.create(
                session=session,
                question_order=item["order"],
                question_text=item["question"],   
            )

        return session