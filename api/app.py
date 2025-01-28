from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from api.logger import setup_logger
from api.routes import router
from api.config import get_settings

settings = get_settings()
logger = setup_logger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title="BlackBox AI API",
        description="A reverse engineered BlackBox AI API",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )

    # 配置中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 移除 GZip 中间件
    # app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # 添加可信主机中间件
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["*"]  # 在生产环境中应该限制允许的主机
    )

    # 添加路由
    app.include_router(router, prefix="/api/v1")
    app.include_router(router, prefix="/v1")  # 兼容性路由

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"An error occurred: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "message": "An internal server error occurred.",
                "detail": str(exc) if settings.DEBUG else None
            },
        )

    return app

app = create_app()
