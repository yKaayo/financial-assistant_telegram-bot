from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.database.models.task import TASK_STATUSES


class TaskCreateSchema(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=3, max_length=500)
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in TASK_STATUSES:
            raise ValueError("Status inválido")
        return value


class TaskUpdateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=3, max_length=120)
    description: str | None = Field(default=None, min_length=3, max_length=500)
    status: str | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str | None) -> str | None:
        if value is not None and value not in TASK_STATUSES:
            raise ValueError("Status inválido")
        return value


def validate_create_payload(payload: dict) -> TaskCreateSchema:
    return TaskCreateSchema.model_validate(payload)


def validate_update_payload(payload: dict) -> TaskUpdateSchema:
    model = TaskUpdateSchema.model_validate(payload)
    if model.model_dump(exclude_none=True) == {}:
        raise ValueError("Nenhum campo foi informado para atualização")
    return model
