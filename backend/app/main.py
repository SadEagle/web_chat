from fastapi import APIRouter, FastAPI, Request, status
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import user, message, chat

# Add backend prefix
app_route = APIRouter(prefix="/api")
app_route.include_router(user.user_route)
app_route.include_router(message.message_route)
app_route.include_router(chat.chat_route)

app = FastAPI(
    title=settings.PROJECT_NAME,
)
app.include_router(app_route)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# WARN: need to be set up at the end of all other exception handlers
@app.exception_handler(Exception)
async def unexpected_exception_handler(request: Request, exc: Exception):
    # TODO: add logger for catch undefined errors instead of print and add proper error message
    print(exc)
    return PlainTextResponse(
        content=f"Unexpected exception appeared. {exc}",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
