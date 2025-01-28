import json
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import StreamingResponse
from api.auth import verify_app_secret
from api.config import get_settings
from api.models import ChatRequest
from api.utils import process_non_streaming_response, process_streaming_response
from api.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()

ALLOWED_MODELS = get_settings().ALLOWED_MODELS

@router.options("/chat/completions")
async def chat_completions_options():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )

@router.get("/models")
async def list_models():
    return {"object": "list", "data": ALLOWED_MODELS, "success": True}

@router.post("/chat/completions")
async def chat_completions(
    request: ChatRequest, app_secret: str = Depends(verify_app_secret)
):
    logger.info("Entering chat_completions route")
    logger.info(f"Received request: {request}")
    logger.info(f"App secret: {app_secret}")
    logger.info(f"Received chat completion request for model: {request.model}")

    if request.model not in [model["id"] for model in ALLOWED_MODELS]:
        raise HTTPException(
            status_code=400,
            detail=f"Model {request.model} is not allowed. Allowed models are: {', '.join(model['id'] for model in ALLOWED_MODELS)}",
        )

    if request.stream:
        logger.info("Streaming response")
        return StreamingResponse(
            process_streaming_response(request), 
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Transfer-Encoding": "chunked"
            }
        )
    else:
        logger.info("Non-streaming response")
        return await process_non_streaming_response(request)


@router.route('/')  
@router.route('/healthz')  
@router.route('/ready')  
@router.route('/alive')  
@router.route('/status') 
@router.get("/health")
def health_check(request: Request):  
    return Response(content=json.dumps({"status": "ok"}), media_type="application/json")  
