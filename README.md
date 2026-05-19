# Ankiflash

Ankiflash is a small Python tool for turning an Italian vocabulary CSV into an Anki `.apkg` deck with audio. It is built around Persian learners: translations in `input/words.csv` can be written in Farsi, while the audio is generated in Italian.

## What It Does

* Reads vocabulary from `input/words.csv`.
* Cleans `input/words.csv` before creating cards by removing duplicate words and rows whose first column is only a number.
* Generates Italian MP3 audio with `gTTS`.
* Reuses existing audio files from `output/audio_files/` so it does not regenerate audio unnecessarily.
* Creates a ready-to-import Anki `.apkg` file inside `output/`.
* Adds a clean, mobile-friendly card style for Anki and AnkiDroid.

## CSV Format

The input file must be:

```text
input/words.csv
```

Each row needs at least 3 columns:

```csv
Word,Translation,Example
appartamento,آپارتمان,Vivo در یک آپارتمان.
```

Column meaning:

* `Word`: Italian word or phrase. This is also used for duplicate detection and audio generation.
* `Translation`: Persian translation.
* `Example`: Example sentence shown on the back of the card.

If the example sentence contains commas, the script keeps the extra CSV columns as part of the example sentence.

The `Word` column must not be only a number. Rows like this are removed before card generation:

```csv
1,translation,example
```

## Setup

This project uses Python 3.12 or newer.

Install dependencies with `uv`:

```bash
uv sync
```

Or with `pip`:

```bash
pip install genanki gtts
```

## Usage

Run the generator:

```bash
python main.py
```

The script asks for an output name:

```text
Enter the desired name for your Anki package (e.g., Lesson1):
```

Examples:

```text
Lesson1
```

creates:

```text
output/Lesson1.apkg
```

If you press Enter without typing a name, the default file is:

```text
output/Italian_With_Audio.apkg
```

## Output

Generated files are stored in `output/`:

```text
output/
  Italian_With_Audio.apkg
  audio_files/
    appartamento.mp3
    terrazzo.mp3
    ...
```

Import the `.apkg` file into Anki or AnkiDroid.

At the end of the run, the script prints a report like this:

```text
Report
Total word rows: ...
Duplicate rows removed: ...
Cards created: ...
Cards with audio: ...
Cards without audio: ...
Existing audio files reused: ...
New audio files generated: ...
Audio generation failures: ...
```

## Input Cleanup

Before generating audio or cards, Ankiflash cleans the first CSV column.

It removes rows where the word is only a number, including Persian digits such as:

```text
1
۱
```

It also removes duplicate words.

Duplicate matching ignores:

* Leading and trailing spaces.
* Letter case.

For example, these are treated as the same word:

```text
ciao
 Ciao
```

Only the first row is kept. Later duplicate rows are removed from `input/words.csv`.

## Project Structure

```text
.
├── main.py
├── input/
│   └── words.csv
├── output/
│   ├── Italian_With_Audio.apkg
│   └── audio_files/
├── pyproject.toml
└── README.md
```

## Notes

* `gTTS` needs internet access when creating new audio files.
* Existing MP3 files are reused, so rerunning the script is faster after the first generation.
* If audio generation fails for some rows, the `.apkg` file is still created. Those cards are included without audio, and the failed words are printed in the terminal.
* The generated Anki deck name is currently `Italian::Polito`.
* The script writes cleaned CSV data back to `input/words.csv` when duplicate or numeric-only word rows are found.

Buon apprendimento! یادگیری خوبی داشته باشید.
