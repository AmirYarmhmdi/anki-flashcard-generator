# Anki Card Generator (Italian/Persian)

This project is a Python-based automation tool to create Anki flashcards. 
I am **Persian**, which is why the phonetic pronunciations and translations in the `words.csv` file are written in **Farsi**. 

## 🌍 Note to international users
> You can easily adapt this project to your own native language by simply updating the translations and phonetic columns in the `words.csv` file. The core logic remains the same!

## ✨ Features
* **Native Audio:** Automatically generates Italian audio for each word using `gTTS` (Google Text-to-Speech).
* **Persian Phonetics:** Includes phonetic guides in Farsi to help with difficult Italian sounds.
* **Automatic Packaging:** Creates a single `.apkg` file that includes all media and styles.
* **Mobile Optimized:** Clean CSS design for a great experience on **AnkiDroid**.

## 🛠️ Requirements

Install the necessary Python libraries:

```bash
pip install genanki gtts

```

## 🚀 How to Use

1. **Prepare the CSV:** Ensure your `words.csv` file follows this structure (4 columns):
* `Word`
* `Phonetic`
* `Translation`
* `Example Sentence`


2. **Run the Generator:**
```bash
python main.py

```


3. **Import to Anki:**
* Transfer `Italian_With_Audio.apkg` to your mobile or PC.
* Open Anki and click **Import**.



## 📂 Project Structure

* `main.py`: The automation script.
* `words.csv`: The vocabulary database.
* `README.md`: Project documentation.
* `audio_files/`: Automatically generated MP3s.

---

*Buon apprendimento! (یادگیری خوبی داشته باشید!)*
