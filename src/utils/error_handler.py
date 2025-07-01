from typing import Annotated, Mapping, Union
from uuid import UUID
import uuid
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import (
    BaseModel,
    Field,
    PlainSerializer,
    PlainValidator,
    ValidationError,
    WithJsonSchema,
)

StrUUID = Annotated[
    UUID,
    PlainSerializer(str, return_type=str),
    PlainValidator(
        lambda x: UUID(x, version=4) if isinstance(x, str) else x,
        json_schema_input_type=Union[str, UUID],
    ),
    WithJsonSchema(
        {
            "type": "string",
            "format": "uuid",
            "description": "UUID v4",
        },
        mode="serialization",
    ),
]


class Response(JSONResponse):
    def __init__(
        self,
        model: BaseModel,
        status_code: int,
        headers: Union[Mapping[str, str], None] = None,
    ):
        super().__init__(
            content=model.model_dump(),
            status_code=status_code,
            headers=headers
        )


class ResponseModel(BaseModel):
    operationId: StrUUID = Field(
        default_factory=uuid.uuid4,
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    detail: str = Field(
        description="Estado de la solicitud", examples=["Solicitud exitosa"]
    )


async def error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        return Response(ResponseModel(detail=str(e)), 500)

    return response


def validation_error_handler(_: Request, e: ValidationError):
    response_details = {error.get("loc")[-1]: error.get("msg")
                        for error in e.errors()}
    return Response(ResponseModel(detail=str(response_details)), 400)


def http_exception_handler(_: Request, e: HTTPException):
    return Response(ResponseModel(detail=str(e.detail)), e.status_code)
