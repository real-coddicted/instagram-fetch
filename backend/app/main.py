from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import ALLOWED_ORIGIN
from app.graph_client import GraphAPIError
from app.models.schemas import PostMetrics, ProfileMetrics
from app.services.metrics_service import MetricsService

app = FastAPI(title="Instagram Metrics Fetcher - Tier 1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def get_metrics_service() -> MetricsService:
    return MetricsService()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Ensure no tokens or stack traces are leaked
    return JSONResponse(
        status_code=500, content={"error": "An internal server error occurred."}
    )


@app.exception_handler(GraphAPIError)
async def graph_api_exception_handler(
    request: Request, exc: GraphAPIError
) -> JSONResponse:
    if exc.status_code == 429:
        headers = {"Retry-After": "60"}
        return JSONResponse(
            status_code=429, content={"error": exc.message}, headers=headers
        )
    return JSONResponse(status_code=exc.status_code, content={"error": exc.message})


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/profile/{username}", response_model=ProfileMetrics)
def get_profile(
    username: str, service: MetricsService = Depends(get_metrics_service)  # noqa: B008
) -> ProfileMetrics:
    data = service.get_profile(username)
    return ProfileMetrics(**data)


@app.get("/post", response_model=PostMetrics)
def get_post(
    username: str, url: str, service: MetricsService = Depends(get_metrics_service)  # noqa: B008
) -> PostMetrics:
    data = service.get_post(username, url)
    return PostMetrics(**data)
