class PromptService:

    @staticmethod
    def generate_interview_questions(job):

        return f"""
You are a senior technical interviewer.

Generate exactly 8 interview questions for the following job.

Job Title:
{job.title}

Job Description:
{job.description}

Required Skills:
{job.skills}

Qualification:
{job.qualification}

Experience:
{job.experience} years

Question Categories:

1. Introduction (1 question)
2. Experience (2 questions)
3. Technical Skills (3 questions)
4. Availability (1 question)
5. Salary Expectation (1 question)

Instructions:

- Start with easy questions.
- Gradually increase the difficulty.
- Include technical questions.
- Include scenario-based questions.
- Ask experience questions based on the required experience.
- Ask one availability question.
- Ask one salary expectation question.
- Do NOT include answers.

Return ONLY valid JSON.

Format:

{{
    "questions":[
        {{
            "order":1,
            "question":"Question text"
        }}
    ]
}}
"""
    
    @staticmethod
    def evaluate_answer(question, answer):
        return f"""
You are a senior technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Rules:
- Score between 0 and 10.
- Return ONLY valid JSON.
- Do not use markdown.

Format:

{{
    "score": 8,
    "reason": "Short explanation"
}}
"""
    


    @staticmethod
    def generate_candidate_summary(
        job,
        ai_score,
        evaluation_notes,
    ):

        return f"""
You are an experienced HR recruiter.

Generate a short evaluation report.

Job Title:
{job.title}

Required Skills:
{job.skills}

Average AI Interview Score:
{ai_score}

AI Evaluation Notes:
{evaluation_notes}

Generate ONLY JSON.

{{
    "strengths":"...",
    "risks":"...",
    "recommendation":"..."
}}
"""