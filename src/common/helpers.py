from functools import wraps
from typing import Callable

from fastapi import HTTPException, Request
from pydantic import ValidationError
from starlette import status

from src.cards.response_models import ArcaneSchema
from src.common.errors_models import InternalServerErrorMessage, ArcaneDBErrorMessage
from src.common.logs import logger

routes_responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": InternalServerErrorMessage,
        "description": "Internal Server Error",
    },
    status.HTTP_504_GATEWAY_TIMEOUT: {
        "model": ArcaneDBErrorMessage,
        "description": "Database operation error",
    },
}


def arcanapi_internal_error(url: str, error: Exception) -> HTTPException:
    """
    Returns an Internal Server Error. Also log it and eventually send
    a Discord notification via a webhook if configured.
    """

    # Log the critical error
    logger.critical(
        "Internal server error for URL {} : {}",
        url,
        str(error),
    )

    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=(
            "An internal server error occurred during the process. The developer "
            "received a notification."
        ),
    )


def validation_error_handler(response_model: type):
    """Decorator used for checking if the value processed by parsers are valid and
    matches the pydantic model. It prevents FastAPI to immediatly return an error,
    and allows to expose a custom error to the user and send a Discord
    notification to the developer.
    """

    def validation_error_handler_inner(func: Callable):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            try:
                result: ArcaneSchema = await func(request, *args, **kwargs)
                print(type(result))
                response = (
                    [response_model(**res) for res in result]
                    if isinstance(result, list)
                    else response_model(result.dict())
                )
            except ValidationError as error:
                raise arcanapi_internal_error(request.url.path, error) from error
            else:
                return response

        return wrapper

    return validation_error_handler_inner
