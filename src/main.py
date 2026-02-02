import logging
from fastapi import FastAPI

from api.exception_handlers import register_exception_handlers
from api.routes import router as job_applications_router
from settings import settings

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings.log.setup()
    logger.info("Application started")
    app = FastAPI()
    app.include_router(job_applications_router, prefix="/v1/job-applications")
    register_exception_handlers(app)
    return app


app = create_app()
