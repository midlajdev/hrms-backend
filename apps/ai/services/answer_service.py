from apps.applications.models import AIAnswer
from apps.ai.services.llm_service import GeminiService
from apps.ai.services.prompt_service import PromptService


class AnswerService:

    def __init__(self):
        self.llm = GeminiService()

    def evaluate_answer(self, question, answer_text):

        prompt = PromptService.evaluate_answer(
            question.question_text,
            answer_text
        )

        result = self.llm.generate_json(prompt)

        ai_answer = AIAnswer.objects.create(
            question=question,
            answer_text=answer_text,
            confidence_score=result.get("score", 0),
            transcript_json=result
        )

        return ai_answer