import csv
from pathlib import Path

import genanki
from gtts import gTTS

# 1. Setup paths, IDs, and media list
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
WORDS_CSV = INPUT_DIR / "words.csv"
AUDIO_DIR = OUTPUT_DIR / "audio_files"

MODEL_ID = 1569382020
DECK_ID = 2025101010


def load_clean_rows(csv_path):
    unique_rows = []
    seen_words = set()
    total_word_count = 0
    duplicate_count = 0
    numeric_word_count = 0
    header_count = 0

    with csv_path.open(mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                continue

            word = row[0].strip()
            if not word:
                continue

            if word.casefold() == "word":
                header_count += 1
                continue

            if word.isdecimal():
                numeric_word_count += 1
                continue

            total_word_count += 1
            word_key = word.casefold()
            if word_key in seen_words:
                duplicate_count += 1
                continue

            seen_words.add(word_key)
            row[0] = word
            unique_rows.append(row)

    if duplicate_count or numeric_word_count or header_count:
        with csv_path.open(mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(unique_rows)

    stats = {
        "total_word_count": total_word_count,
        "duplicate_count": duplicate_count,
        "numeric_word_count": numeric_word_count,
        "header_count": header_count,
    }

    return unique_rows, stats

# 2. Define Card Styling (CSS)
style = """
.card { font-family: Arial; text-align: center; color: #2c3e50; background-color: white; }
.word { font-size: 32px; color: #2980b9; font-weight: bold; }
.trans { font-size: 26px; color: #27ae60; margin: 15px 0; }
.ex { font-size: 18px; color: #7f8c8d; font-style: italic; }
audio { margin-top: 10px; }
"""

# 3. Define the Model
my_model = genanki.Model(
    MODEL_ID,
    "Italian Audio Model",
    fields=[
        {"name": "Word"},
        {"name": "Translation"},
        {"name": "Example"},
        {"name": "Audio"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": '<div class="word">{{Word}}</div>',
            "afmt": '{{FrontSide}}<hr id="answer"><div class="trans">{{Translation}}</div><div class="ex">{{Example}}</div><br>{{Audio}}',
        },
    ],
    css=style,
)

def main():
    my_deck = genanki.Deck(DECK_ID, "Italian::Polito")
    media_files = []
    audio_errors = []
    generated_audio_count = 0
    existing_audio_count = 0
    cards_with_audio_count = 0

    # 4. Read CSV and Generate Audio
    try:
        OUTPUT_DIR.mkdir(exist_ok=True)
        AUDIO_DIR.mkdir(exist_ok=True)

        rows, cleanup_stats = load_clean_rows(WORDS_CSV)
        if cleanup_stats["header_count"]:
            print(
                f"Removed {cleanup_stats['header_count']} header row(s) from {WORDS_CSV}."
            )
        if cleanup_stats["duplicate_count"]:
            print(
                f"Removed {cleanup_stats['duplicate_count']} duplicate row(s) from {WORDS_CSV}."
            )
        if cleanup_stats["numeric_word_count"]:
            print(
                f"Removed {cleanup_stats['numeric_word_count']} row(s) with numeric-only words from {WORDS_CSV}."
            )

        for row in rows:
            word, trans = row[:2]
            example = ",".join(row[2:])

            audio_filename = AUDIO_DIR / f"{word}.mp3"
            if audio_filename.exists():
                existing_audio_count += 1
            else:
                try:
                    tts = gTTS(text=word, lang="it")
                    tts.save(str(audio_filename))
                    generated_audio_count += 1
                except Exception as e:
                    audio_errors.append((word, e))

            audio_field = ""
            if audio_filename.exists():
                media_files.append(str(audio_filename))
                audio_field = f"[sound:{audio_filename.name}]"
                cards_with_audio_count += 1

            note = genanki.Note(
                model=my_model,
                fields=[word, trans, example, audio_field],
            )
            my_deck.add_note(note)

        if audio_errors:
            print(
                f"Could not generate audio for {len(audio_errors)} row(s). "
                "The package will still be created without those audio files."
            )
            for word, error in audio_errors[:10]:
                print(f"- {word}: {error}")
            if len(audio_errors) > 10:
                print(f"... and {len(audio_errors) - 10} more.")

        # 5. Dynamic Packaging
        print("-" * 30)
        output_filename = input(
            "Enter the desired name for your Anki package (e.g., Lesson1): "
        ).strip()
        if not output_filename:
            output_filename = "Italian_With_Audio"

        output_path = OUTPUT_DIR / Path(output_filename).name

        # Ensure the filename ends with .apkg
        if output_path.suffix.lower() != ".apkg":
            output_path = output_path.with_suffix(".apkg")

        package = genanki.Package(my_deck)
        package.media_files = media_files
        package.write_to_file(str(output_path))

        print(f"\n🚀 Success! '{output_path}' has been created with voice files.")
        print("-" * 30)
        print("Report")
        print(f"Total word rows: {cleanup_stats['total_word_count']}")
        print(f"Duplicate rows removed: {cleanup_stats['duplicate_count']}")
        print(f"Cards created: {len(rows)}")
        print(f"Cards with audio: {cards_with_audio_count}")
        print(f"Cards without audio: {len(rows) - cards_with_audio_count}")
        print(f"Existing audio files reused: {existing_audio_count}")
        print(f"New audio files generated: {generated_audio_count}")
        print(f"Audio generation failures: {len(audio_errors)}")
        print("-" * 30)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
