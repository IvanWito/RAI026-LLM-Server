from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models import HealthResponse, ProcessRequest, ProcessResponse
from app.services import build_user_prompt, get_provider, load_system_prompt, parse_instruction

app = FastAPI(title=settings.app_name, version="0.1.0")

cors_origins = [origin.strip() for origin in settings.cors_allow_origins.split(",") if origin.strip()]
if not cors_origins:
    cors_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _verify_api_key(x_api_key: str | None) -> None:
    expected = settings.server_api_key
    if expected and x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

@app.get("/")
async def root():
    return {"message": "Welcome, LLM Server is running!"}

@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(provider=settings.llm_provider, model=settings.llm_model)


@app.post("/v1/raw")
async def raw_output(request: ProcessRequest, x_api_key: str | None = Header(default=None)) -> dict:
    """Debug endpoint: returns the raw LLM text without parsing."""
    _verify_api_key(x_api_key)
    provider = get_provider(request.provider or settings.llm_provider)
    system_prompt = load_system_prompt()
    user_prompt = build_user_prompt(
        transcript=request.transcript,
        context=request.context,
        history=[msg.model_dump() for msg in request.history],
    )
    raw = await provider.generate(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=request.model or settings.llm_model,
    )
    return {"raw": raw}


@app.post("/v1/process", response_model=ProcessResponse)
async def process(request: ProcessRequest, x_api_key: str | None = Header(default=None)) -> ProcessResponse:
    _verify_api_key(x_api_key)
    provider_name = request.provider or settings.llm_provider
    model_name = request.model or settings.llm_model

    try:
        provider = get_provider(provider_name)
        system_prompt = load_system_prompt()
        user_prompt = build_user_prompt(
            transcript=request.transcript,
            context=request.context,
            history=[msg.model_dump() for msg in request.history],
        )

        raw_output = await provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model_name,
        )
        instruction = parse_instruction(raw_output)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"LLM processing failed: {type(exc).__name__}: {exc}") from exc

    return ProcessResponse(
        transcript=request.transcript,
        provider=provider_name,
        model=model_name,
        instruction=instruction,
        raw_model_output=raw_output,
    )
