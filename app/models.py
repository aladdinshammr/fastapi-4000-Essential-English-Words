from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    image = Column(String, nullable=False)

    words = relationship("Word", back_populates="unit", cascade="all, delete")
    exercises = relationship("Exercise", back_populates="unit", cascade="all, delete")
    readings = relationship("Reading", back_populates="unit", cascade="all, delete")
    reading_answers = relationship(
        "ReadingAnswer", back_populates="unit", cascade="all, delete"
    )
    exercise_answers = relationship(
        "ExerciseAnswer", back_populates="unit", cascade="all, delete"
    )


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey("units.id", ondelete="CASCADE"), index=True)

    word = Column(String, index=True)
    description = Column(Text)
    example = Column(Text)
    pronunciation = Column(String)
    image = Column(String)
    sound = Column(String)
    vi = Column(String)

    unit = relationship("Unit", back_populates="words")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey("units.id", ondelete="CASCADE"), index=True)

    title = Column(String)
    content = Column(Text)
    type = Column(String, index=True)

    unit = relationship("Unit", back_populates="exercises")


class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey("units.id", ondelete="CASCADE"), index=True)

    title = Column(String)
    content = Column(Text)
    type = Column(String)
    image = Column(String)
    sound = Column(String)

    unit = relationship("Unit", back_populates="readings")


class Index(Base):
    __tablename__ = "indexes"
    id = Column(Integer, primary_key=True)
    book = Column(Integer, nullable=False)
    letter = Column(String, nullable=False)
    words = Column(String, nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    reading_answers = relationship(
        "ReadingAnswer", back_populates="user", cascade="all, delete"
    )
    exercise_answers = relationship(
        "ExerciseAnswer", back_populates="user", cascade="all, delete"
    )


class ReadingAnswer(Base):
    __tablename__ = "reading_answers"
    id = Column(Integer, primary_key=True, nullable=False)
    unit_id = Column(
        Integer, ForeignKey("units.id", ondelete="CASCADE"), index=True, nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    answer = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    unit = relationship("Unit", back_populates="reading_answers")
    user = relationship("User", back_populates="reading_answers")


class ExerciseAnswer(Base):
    __tablename__ = "exercise_answers"
    id = Column(Integer, primary_key=True, nullable=False)
    unit_id = Column(
        Integer, ForeignKey("units.id", ondelete="CASCADE"), index=True, nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    answer = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    unit = relationship("Unit", back_populates="exercise_answers")
    user = relationship("User", back_populates="exercise_answers")

    __table_args__ = (UniqueConstraint("unit_id", "user_id", name="uq_unit_user"),)
