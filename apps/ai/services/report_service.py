from django.db.models import Avg

from apps.applications.models import (
    JobApplication,
    AIInterviewSession,
    AIAnswer,
)

from apps.ai.services.llm_service import GeminiService
from apps.ai.services.prompt_service import PromptService


class ReportService:

    def __init__(self):
        self.llm = GeminiService()

    def generate_report(self, session):

        ai_score = 0
        evaluation_notes = ""

        if session:

            answers = AIAnswer.objects.filter(
                question__session=session
            )

            ai_score = (
                answers.aggregate(
                    Avg("confidence_score")
                )["confidence_score__avg"] or 0
            )

            notes = []

            for answer in answers:

                reason = answer.transcript_json.get(
                    "reason",
                    ""
                )

                if reason:
                    notes.append(reason)

            evaluation_notes = "\n".join(notes)

        prompt = PromptService.generate_candidate_summary(
            session.job,
            round(ai_score, 2),
            evaluation_notes
        )

        summary = self.llm.generate_json(prompt)

        return {

            "candidate": session.candidate.email,

            "job": session.job.title,

            "ai_score": round(ai_score, 2),

            "strengths": summary.get("strengths"),

            "risks": summary.get("risks"),

            "recommendation": summary.get("recommendation"),
        }