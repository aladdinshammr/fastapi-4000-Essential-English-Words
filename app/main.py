from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


from .routers import index, flashcards, story, exercise, unit, user, answer


app = FastAPI(
    title="4000 Essential English Words",
    description="The 4000 Essential English Words series is a six-book vocabulary collection designed for English language learners. It systematically introduces the 4,000 most frequent and useful words in English. Each book contains 600 words divided into 30 units, with 20 words per unit. The series emphasizes learning through context—every word is presented with a clear definition, example sentences, and a short story that incorporates the target vocabulary. Exercises reinforce meaning, spelling, and usage. The structured, step‑by‑step approach helps learners build a strong foundation for reading, writing, and communication.",
    version="1.0.0",
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(unit.router)
app.include_router(story.router)
app.include_router(flashcards.router)
app.include_router(exercise.router)
app.include_router(answer.router)
app.include_router(index.router)
app.include_router(user.router)


# @app.get("/")
# def root():
#     return "Up"
