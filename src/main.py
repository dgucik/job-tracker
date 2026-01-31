from fastapi import FastAPI
from api.routes import router as job_applications_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(job_applications_router, prefix="/v1/job-applications")
    return app


app = create_app()
