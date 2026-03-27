import os
import json
from app.database import SessionLocal, engine, Base
from app.models import Unit, Word, Exercise, Reading, Index


DATA_DIR = "books"


def get_exercise_type(title):
    if not title:
        return "exercise"
    return "answer" if "answer" in title.lower() else "exercise"


def import_unit(session, unit_data, file):
    filename = int(file[:-5])

    # Create unit
    if unit_data.get("en") == "Index":
        word_list = []
        for w in unit_data.get("exercise", []):
            word_list.append(
                Index(
                    book=filename,
                    letter=w.get("en"),
                    words=w.get("story"),
                )
            )
        session.bulk_save_objects(word_list)
        pass
    else:
        unit = unit_data.get("en")
        unit_num = (filename - 1) * 30
        print(unit_num)
        title = f"Unit {int(unit[5:])+unit_num}"
        unit = Unit(title=title, image=unit_data.get("image"))
        session.add(unit)
        session.flush()

        # Words,
        words = []
        for w in unit_data.get("wordlist", []):
            words.append(
                Word(
                    unit_id=unit.id,
                    word=w.get("en"),
                    description=w.get("desc"),
                    example=w.get("exam"),
                    pronunciation=w.get("pron"),
                    image=w.get("image"),
                    sound=w.get("sound"),
                    vi=w.get("vi"),
                )
            )
        session.bulk_save_objects(words)

        # Exercises
        exercises = []
        for ex in unit_data.get("exercise", []):
            exercises.append(
                Exercise(
                    unit_id=unit.id,
                    title=ex.get("en"),
                    content=ex.get("story"),
                    type=get_exercise_type(ex.get("en")),
                )
            )
        session.bulk_save_objects(exercises)

        # Readings
        readings = []
        for r in unit_data.get("reading", []):
            readings.append(
                Reading(
                    unit_id=unit.id,
                    title=r.get("en"),
                    content=r.get("story"),
                    type=r.get("type", "answer"),
                    image=r.get("image"),
                    sound=r.get("sound"),
                )
            )
        session.bulk_save_objects(readings)


def import_all_books():
    session = SessionLocal()

    try:
        for filename in os.listdir(DATA_DIR):
            if not filename.endswith(".json"):
                continue

            filepath = os.path.join(DATA_DIR, filename)

            print(f"📘 Importing {filename}...")

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)["flashcard"]

            for unit_data in data:
                import_unit(session, unit_data, filename)

        session.commit()
        print("✅ All books imported successfully!")

    except Exception as e:
        session.rollback()
        print("❌ Error:", e)

    finally:
        session.close()


if __name__ == "__main__":
    # Create tables first
    # Base.metadata.create_all(engine)

    # Import data
    import_all_books()
