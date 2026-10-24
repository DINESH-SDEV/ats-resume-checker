
from app.database import Base, engine, SessionLocal
from app.models import User, ResumeAnalysis

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    user = User(
        name="Test User",
        email="testuser2@example.com"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    analysis = ResumeAnalysis(
        resume_text="Python SQL",
        job_text="Python SQL Java",
        score=75.0,
        matched_keywords="python, sql",
        missing_keywords="java",
        user_id=user.id
    )
    db.add(analysis)
    db.commit()

    saved_user = db.query(User).filter_by(
        email="testuser@example.com"
    ).first()

    saved_analysis = db.query(ResumeAnalysis).filter_by(
        user_id=user.id
    ).first()

    print("User saved:", saved_user.name)
    print("Resume score:", saved_analysis.score)
    print("Database CRUD test successful!")

finally:
    db.close()
