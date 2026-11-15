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


@app.middleware("http")
async def fix_vercel_path(request, call_next):
    raw_target = request.headers.get("x-matched-path") or request.headers.get("x-forwarded-uri")
    if raw_target:
        clean_path = raw_target.split("?")[0]
        if request.scope.get("path") in ["/api/index.py", "/api", "/api/", "/index.py", "/"]:
            request.scope["path"] = clean_path
    return await call_next(request)


# Include all routers under both /api/v1 and /v1 for Vercel path compatibility
ROUTERS = [
    (auth.router, "/auth", ["Authentication"]),
    (users.router, "/users", ["Users"]),
    (profiles.router, "/profiles", ["Profiles"]),
    (topics.router, "/topics", ["Topics"]),
    (patterns.router, "/patterns", ["Patterns"]),
    (knowledge_graph.router, "/knowledge-graph", ["Knowledge Graph"]),
    (recommendations.router, "/recommendations", ["Recommendations"]),
    (mastery.router, "/mastery", ["Mastery"]),
    (assessments.router, "/assessments", ["Assessments"]),
    (revision.router, "/revision", ["Revision"]),
    (gaps.router, "/gaps", ["Gaps & Reality Check"]),
    (activity.router, "/activity", ["Activity & Dashboard"]),
]

for router_obj, path_prefix, tags in ROUTERS:
    app.include_router(router_obj, prefix=f"/api/v1{path_prefix}", tags=tags)
    app.include_router(router_obj, prefix=f"/v1{path_prefix}", tags=tags, include_in_schema=False)


@app.get("/api/health")
@app.get("/health")
@app.get("/api")
@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "dsaura-api",
        "version": "1.0.0",
        "message": "DSAURA Intelligence Engine is running"
    }


def init_db():
    try:
        from app.database import engine, Base, SessionLocal
        from app.models.user import User
        from app.utils.security import hash_password
        from app.knowledge_base.seed_data import seed_database
        from app.routers.mastery import ensure_user_problem_history
        import uuid

        DEFAULT_TEST_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            seed_database(db)
            test_user = db.query(User).filter(User.email == "test@dsaura.dev").first()
            if not test_user:
                test_user = User(
                    id=DEFAULT_TEST_USER_ID,
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


@app.on_event("startup")
def on_startup():
    init_db()


# Initialize database on module load so it works even in serverless environments where lifespan events are skipped
try:
    init_db()
except Exception:
    pass
