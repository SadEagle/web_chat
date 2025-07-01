from fastapi import FastAPI, Request, status
from fastapi.responses import PlainTextResponse

from app.core.config import settings
from app.routes import login, message

app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.include_router(login.login_route)
app.include_router(message.message_route)

# TODO: Add CORS


# WARN: need to be set up at the end of all other exception handlers
@app.exception_handler(Exception)
async def unexpected_exception_handler(request: Request, exc: Exception):
    # TODO: add logger for catch undefined errors instead of print
    print(exc)
    return PlainTextResponse(
        content=f"Unexpected exception appeared. {exc}",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
