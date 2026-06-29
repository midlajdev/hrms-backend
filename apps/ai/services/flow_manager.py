class FlowManager:

    @staticmethod
    def get_next_question(session):

        answered = (
            session.questions
            .filter(answers__isnull=False)
            .count()
        )

        return session.questions.filter(
            question_order=answered + 1
        ).first()