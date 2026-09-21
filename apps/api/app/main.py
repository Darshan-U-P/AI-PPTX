import logging
import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import ai, exports, presentations
from app.core.database import Base, engine
from app.services.presentation_service import NotFoundError

logging.basicConfig(format="%(message)s", level=logging.INFO)
logger = logging.getLogger("brahma.api")

app = FastAPI(title="Brahma Slides API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(presentations.router, prefix="/api/v1")
app.include_router(exports.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def log_request(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    logger.info("request method=%s path=%s status=%s duration_ms=%d", request.method, request.url.path, response.status_code, (time.perf_counter() - started) * 1000)
    return response


@app.exception_handler(NotFoundError)
async def missing_resource(_, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"error": {"code": "RESOURCE_NOT_FOUND", "message": str(exc)}})


@app.exception_handler(RequestValidationError)
async def invalid_request(_, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"error": {"code": "VALIDATION_ERROR", "message": "Invalid Presentation IR payload", "details": exc.errors()}})


@app.get("/health")
def health():
    return {"status": "ok"}
