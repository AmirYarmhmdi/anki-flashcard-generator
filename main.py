import csv
import os

import genanki
from gtts import gTTS

# 1. Setup IDs and Media list
MODEL_ID = 1569382020
DECK_ID = 2025101010
media_files = []

# 2. Define Card Styling (CSS)
style = """
.card { font-family: Arial; text-align: center; color: #2c3e50; background-color: white; }
.word { font-size: 32px; color: #2980b9; font-weight: bold; }
.pron { font-size: 18px; color: #e67e22; margin-bottom: 10px; }
.trans { font-size: 26px; color: #27ae60; margin: 15px 0; }
.ex { font-size: 18px; color: #7f8c8d; font-style: italic; }
audio { margin-top: 10px; }
"""

# 3. Define the Model with Audio field
# We added {{Audio}} to the back template (afmt)
my_model = genanki.Model(
    MODEL_ID,
    "Italian Audio Model",
    fields=[
        {"name": "Word"},
        {"name": "Pronunciation"},
        {"name": "Translation"},
        {"name": "Example"},
        {"name": "Audio"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": '<div class="word">{{Word}}</div><div class="pron">[{{Pronunciation}}]</div>',
            "afmt": '{{FrontSide}}<hr id="answer"><div class="trans">{{Translation}}</div><div class="ex">{{Example}}</div><br>{{Audio}}',
        },
    ],
    css=style,
)

my_deck = genanki.Deck(DECK_ID, "Italian::Polito")

# 4. Read CSV and Generate Audio
try:
    if not os.path.exists("audio_files"):
        os.makedirs("audio_files")

    with open("words.csv", mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 4:
                continue

            word, pron, trans, example = row

            # Generate Text-to-Speech file
            audio_filename = f"audio_files/{word}.mp3"
            if not os.path.exists(audio_filename):
                tts = gTTS(text=word, lang="it")
                tts.save(audio_filename)

            media_files.append(audio_filename)

            # Create Anki Note
            # Note: Audio field uses [sound:filename.mp3] format
            note = genanki.Note(
                model=my_model,
                fields=[word, pron, trans, example, f"[sound:{word}.mp3]"],
            )
            my_deck.add_note(note)

    # 5. Package the Deck and Media files
    package = genanki.Package(my_deck)
    package.media_files = media_files
    package.write_to_file("Italian_With_Audio.apkg")

    print("Success! 'Italian_With_Audio.apkg' has been created with voice files.")

except Exception as e:
    print(f"An error occurred: {e}")
