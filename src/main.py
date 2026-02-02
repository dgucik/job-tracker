import logging
from fastapi import FastAPI

from api.routes import router as job_applications_router
from settings import settings

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings.log.setup()
    logger.info("Application started")
    app = FastAPI()
    app.include_router(job_applications_router, prefix="/v1/job-applications")
    return app


app = create_app()
