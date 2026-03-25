from pydantic import BaseModel, computed_field, EmailStr
from datetime import datetime, date
from typing import List

from .config import settings


class Words(BaseModel):
    id: int
    book: int
    letter: str
    words: str
    model_config = {"from_attributes": True}


class Flashcard(BaseModel):
    id: int
    description: str
    example: str
    vi: str
    unit_id: int
    word: str
    pronunciation: str
    image: str
    sound: str

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def image_url(self) -> str:
        return f"{settings.base_url}/media/images/{self.image}"

    @computed_field
    @property
    def audio_url(self) -> str:
        return f"{settings.base_url}/media/audio/{self.sound}"


class Story(BaseModel):
    id: int
    unit_id: int
    title: str
    type: str
    content: str
    image: str
    sound: str

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def image_url(self) -> str:
        return f"{settings.base_url}/media/images/{self.image}"

    @computed_field
    @property
    def audio_url(self) -> str:
        return f"{settings.base_url}/media/audio/{self.sound}"


class Exercise(BaseModel):
    id: int
    unit_id: int
    title: str
    type: str
    content: str


class AnswerKey(BaseModel):
    id: int
    unit_id: int
    title: str
    content: str


class Unit(BaseModel):
    id: int
    title: str
    image: str
    words: List[Flashcard]
    readings: List[Story | Exercise | AnswerKey]
    # reading_comperhension: Exercise
    # reading_answer_key: AnswerKey
    exercises: List[Exercise]
    # answer_key: AnswerKey

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def image_url(self) -> str:
        return f"{settings.base_url}/media/images/{self.image}"


class User(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    current_streak: int
    longest_streak: int
    last_active_date: date
    created_at: datetime
    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class UserAnswer(BaseModel):
    unit_id: int
    answer: str


class UserAnswerRespone(UserAnswer):
    id: int
    created_at: datetime
    user_id: int
