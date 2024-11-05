from fastapi import APIRouter
from starlette import status


apiRouter = APIRouter(tags=["Health check"])


@apiRouter.get(
    "/health_check/ping",
    status_code=status.HTTP_200_OK,
)
async def health_check():
    return {"status": "ok"}
