from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers import (
    auth, users, profiles, topics, patterns,
    knowledge_graph, recommendations, mastery,
    assessments, revision, gaps, activity
)

settings = get_settings()

app = FastAPI(
    title="DSAURA API",
    description="Intelligent DSA Learning and Knowledge Assessment Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

cors_origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins else ["*"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(profiles.router, prefix="/api/v1/profiles", tags=["Profiles"])
app.include_router(topics.router, prefix="/api/v1/topics", tags=["Topics"])
app.include_router(patterns.router, prefix="/api/v1/patterns", tags=["Patterns"])
app.include_router(knowledge_graph.router, prefix="/api/v1/knowledge-graph", tags=["Knowledge Graph"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"])
app.include_router(mastery.router, prefix="/api/v1/mastery", tags=["Mastery"])
app.include_router(assessments.router, prefix="/api/v1/assessments", tags=["Assessments"])
app.include_router(revision.router, prefix="/api/v1/revision", tags=["Revision"])
app.include_router(gaps.router, prefix="/api/v1/gaps", tags=["Gaps & Reality Check"])
app.include_router(activity.router, prefix="/api/v1/activity", tags=["Activity & Dashboard"])


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "dsaura-api", "version": "1.0.0"}


@app.on_event("startup")
def init_db():
    try:
        from app.database import engine, Base, SessionLocal
        from app.models.user import User
        from app.utils.security import hash_password
        from app.knowledge_base.seed_data import seed_database
        from app.routers.mastery import ensure_user_problem_history
        import uuid

        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            seed_database(db)
            test_user = db.query(User).filter(User.email == "test@dsaura.dev").first()
            if not test_user:
                test_user = User(
                    id=uuid.uuid4(),
                    name="Test Architect",
                    email="test@dsaura.dev",
                    password_hash=hash_password("Password123!"),
                )
                db.add(test_user)
                db.commit()
                db.refresh(test_user)
            ensure_user_problem_history(test_user.id, db)
        finally:
            db.close()
    except Exception as e:
        print(f"Startup DB init info: {e}")
