from app.database import Base, SessionLocal, engine
from app.db_models import JobRole, Competency


Base.metadata.create_all(bind=engine)


DEMO_JOB_ROLES = [
    {
        "job_role_code": "DEMO-ELECTRICAL-001",
        "title": "Electrical Technician",
        "sector": "Electronics & Hardware",
        "nsqf_level": "DEMO",
        "qualification_title": "DEMO RECORD - VERIFY OFFICIAL SOURCE",
        "description": (
            "Demonstration job role for testing VoxMinds matching."
        ),
        "source": "DEMO_DATA_NOT_OFFICIAL",
        "competencies": [
            "Basic electrical safety",
            "Electrical wiring",
            "Use of electrical tools",
            "Basic fault identification",
        ],
    },
    {
        "job_role_code": "DEMO-SOLAR-001",
        "title": "Solar Technician",
        "sector": "Green Jobs",
        "nsqf_level": "DEMO",
        "qualification_title": "DEMO RECORD - VERIFY OFFICIAL SOURCE",
        "description": (
            "Demonstration job role for testing solar-related matching."
        ),
        "source": "DEMO_DATA_NOT_OFFICIAL",
        "competencies": [
            "Solar system basics",
            "Basic electrical safety",
            "Solar installation",
            "Basic maintenance",
        ],
    },
    {
        "job_role_code": "DEMO-TAILOR-001",
        "title": "Tailoring Professional",
        "sector": "Apparel",
        "nsqf_level": "DEMO",
        "qualification_title": "DEMO RECORD - VERIFY OFFICIAL SOURCE",
        "description": (
            "Demonstration job role for testing tailoring matching."
        ),
        "source": "DEMO_DATA_NOT_OFFICIAL",
        "competencies": [
            "Fabric handling",
            "Sewing machine operation",
            "Garment measurement",
            "Basic garment finishing",
        ],
    },
]


def seed_database():
    db = SessionLocal()

    try:
        for role_data in DEMO_JOB_ROLES:

            existing = (
                db.query(JobRole)
                .filter(
                    JobRole.job_role_code
                    == role_data["job_role_code"]
                )
                .first()
            )

            if existing:
                continue

            role = JobRole(
                job_role_code=role_data["job_role_code"],
                title=role_data["title"],
                sector=role_data["sector"],
                nsqf_level=role_data["nsqf_level"],
                qualification_title=(
                    role_data["qualification_title"]
                ),
                description=role_data["description"],
                source=role_data["source"],
            )

            db.add(role)

            db.flush()

            for competency_name in role_data["competencies"]:
                competency = Competency(
                    job_role_id=role.id,
                    name=competency_name,
                    description=(
                        f"Demo competency: {competency_name}"
                    ),
                )

                db.add(competency)

        db.commit()

        print("NSQF demo knowledge base seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()