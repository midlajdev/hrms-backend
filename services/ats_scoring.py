WEIGHTS = {
    "skills": 50,
    "experience": 30,
    "education": 20
}

def parse_skills(skills):
    if not skills:
        return []
    return [s.strip().lower() for s in skills.split(",")]

def parse_education_field(education_text):
    if not education_text:
        return []
    return [edu.strip().lower() for edu in education_text.split(',')]

def calculate_skill_score(job_skills, candidate_skills):
    job_skills = parse_skills(job_skills)
    candidate_skills = parse_skills(candidate_skills)

    matched = set(job_skills) & set(candidate_skills)
    print("Matched", len(matched))
    print("Job Skills", len(job_skills))
    return len(matched) / len(job_skills) if job_skills else 0


def calculate_experience_score(required_exp, candidate_exp):
    if not required_exp:
        return 1
    candidate_exp = candidate_exp or 0
    score = candidate_exp / required_exp
    return min(score, 1)


def calculate_education_score(job_edu, candidate_edu):
    required_list = parse_education_field(job_edu)
    if not job_edu:
        return 1
    if not candidate_edu:
        return 0
    candidate_edu = candidate_edu.lower()
    for edu in job_edu:
        if edu in candidate_edu:
            return 1
    return 0

def calculate_total_score(job, candidate):
    skill_score = calculate_skill_score(job.skills, candidate.skills)
    exp_score = calculate_experience_score(job.experience,candidate.total_experience)
    edu_score = calculate_education_score(job.qualification, candidate.highest_education)

    total = (
        skill_score * WEIGHTS["skills"] +
        exp_score * WEIGHTS["experience"] +
        edu_score * WEIGHTS["education"]
    )

    return round(total, 2)