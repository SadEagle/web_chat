from fastapi import FastAPI

from app.core.config import settings
from app.routes import login, message

app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.include_router(login.login_route)
app.include_router(message.message_route)

# TODO: Add CORS
