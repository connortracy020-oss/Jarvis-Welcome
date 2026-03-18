[README (1).md](https://github.com/user-attachments/files/26075612/README.1.md)
# Jarvis-Welcome

A Python-based voice-activated wake system for Mac. Clap twice, say the phrase, and your computer responds with JARVIS.

---

## How It Works

1. Clap twice within 2 seconds
2. Say "Wake up daddy's home" or anything containing **"wake"**, **"daddy"**, or **"home"**
3. JARVIS responds with the audio clip, exactly like the scene in Iron Man 2 (2010).

---

## Requirements

- macOS (uses `afplay` for audio)
- Python 3
- A microphone
- Your own JARVIS audio clip (.mp3)

---

## Installation

**1. Install Homebrew** (if you don't have it):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**2. Install portaudio:**
```bash
brew install portaudio
```

**3. Install Python dependencies:**
```bash
pip3 install pyaudio numpy SpeechRecognition
```

---

## Usage

```bash
python3 jarvis_wake.py /path/to/your/audio.mp3
```

**Example:**
```bash
python3 jarvis_wake.py ~/jarvis_welcome.mp3
```

---

## Configuration

At the top of `jarvis_wake.py` you can tweak these values:

| Variable | Default | Description |
|---|---|---|
| `CLAP_THRESHOLD` | `2500` | RMS amplitude to register a clap. Raise if too sensitive, lower if missing claps. |
| `CLAP_WINDOW` | `2.0` | Max seconds allowed between two claps |
| `MIN_CLAP_GAP` | `0.15` | Debounce gap to avoid double-counting one clap |
| `TRIGGER_WORDS` | `["wake", "daddy", "home"]` | Any of these words in your phrase will trigger the response |

---

## Notes

- The audio file is not included. Bring your own .mp3.
- Requires microphone permissions on macOS. You will be prompted on first run.
- Uses Google Speech Recognition, so an internet connection is required for phrase detection.

---

## License

MIT
