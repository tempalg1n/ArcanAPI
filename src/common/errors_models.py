from pydantic import BaseModel, Field


class InternalServerErrorMessage(BaseModel):
    error: str = Field(
        ...,
        description="Message describing the internal server error",
        example=(
            "An internal server error occurred during the process. The developer "
            "received a notification."
        ),
    )


class ArcaneDBErrorMessage(BaseModel):
    error: str = Field(
        ...,
        description="Message describing the DB operations error",
        example="Timeout.",
    )


class ArcaneNotFoundMessage(BaseModel):
    error: str = Field(
        ...,
        description="Message describing the DB operations error",
        example="Arcane not found",
    )


class ForbiddenErrorMessage(BaseModel):
    error: str = Field(
        ...,
        description="Message describing that user have no rights",
        example="You have no access to that operation."
    )
