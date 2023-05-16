from starlette import status

from src.common.errors_models import InternalServerErrorMessage, ArcaneDBErrorMessage

routes_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": InternalServerErrorMessage,
        "description": "Internal Server Error",
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ArcaneDBErrorMessage,
        "description": "Database operation error",
    },
}