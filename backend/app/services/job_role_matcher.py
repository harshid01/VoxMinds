from app.services.competency_mapper import (
    map_skills_to_competencies
)


def normalize_name(value: str) -> str:
    return value.strip().lower()


def match_job_roles(
    skills: list,
    job_roles: list,
    top_k: int = 5
):
    """
    Match beneficiary skills against job-role competencies.

    This is a prototype suitability matcher.
    It is NOT an employment probability.
    """

    if not skills:
        return []

    skill_mappings = map_skills_to_competencies(skills)

    beneficiary_competencies = set()

    for mapping in skill_mappings:
        for competency in mapping["competencies"]:
            beneficiary_competencies.add(
                normalize_name(competency)
            )

    results = []

    for role in job_roles:
        role_competencies = {
            normalize_name(competency.name)
            for competency in role.competencies
        }

        if not role_competencies:
            continue

        matched_competencies = (
            beneficiary_competencies
            & role_competencies
        )

        if not matched_competencies:
            continue

        score = (
            len(matched_competencies)
            / len(role_competencies)
        ) * 100

        results.append({
            "job_role_id": role.id,
            "job_role_code": role.job_role_code,
            "title": role.title,
            "sector": role.sector,
            "nsqf_level": role.nsqf_level,
            "qualification_title": role.qualification_title,
            "score": round(score, 2),
            "matched_competencies": sorted(
                matched_competencies
            ),
            "total_role_competencies": len(
                role_competencies
            ),
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]