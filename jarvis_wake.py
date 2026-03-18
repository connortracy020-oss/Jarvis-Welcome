#!/usr/bin/env python3
"""
J.A.R.V.I.S Wake System
  1. Clap twice (within 2 seconds)
  2. Say anything with "wake", "daddy", or "home"
  3. JARVIS responds

Usage:
  python3 jarvis_wake.py /path/to/audio.mp3
"""

import sys, os, time, threading, subprocess
import numpy as np
import pyaudio
import speech_recognition as sr

# ── Config ─────────────────────────────────────
AUDIO_FILE     = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/jarvis_welcome.mp3")
CLAP_THRESHOLD = 2500   # raise if false triggers, lower if missing claps
CLAP_WINDOW    = 2.0    # seconds between first and second clap
MIN_CLAP_GAP   = 0.15   # debounce
TRIGGER_WORDS  = ["wake", "daddy", "home"]
SAMPLE_RATE    = 44100
CHUNK          = 1024
# ───────────────────────────────────────────────

if not os.path.isfile(AUDIO_FILE):
    print(f"\n❌  Audio file not found: {AUDIO_FILE}")
    print("    Usage: python3 jarvis_wake.py /path/to/audio.mp3\n")
    sys.exit(1)

print(f"\n🤖  JARVIS online — audio: {os.path.basename(AUDIO_FILE)}")
print("👏  Clap twice, then say the phrase.\n")

_phrase_active = threading.Event()
_cooldown_until = 0.0


def play_audio():
    time.sleep(0.3)
    subprocess.run(["afplay", AUDIO_FILE])


def listen_for_phrase():
    global _cooldown_until
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 200
    recognizer.dynamic_energy_threshold = True
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.3)
            print("🎤  Listening for phrase...")
            audio = recognizer.listen(mic, timeout=6, phrase_time_limit=6)
        text = recognizer.recognize_google(audio).lower()
        print(f'   heard: "{text}"')
        if any(w in text for w in TRIGGER_WORDS):
            print("\n⚡  Welcome home, sir.\n")
            _cooldown_until = time.time() + 12.0
            threading.Thread(target=play_audio, daemon=True).start()
        else:
            print("   ✗ Phrase not matched. Try again.\n")
    except sr.WaitTimeoutError:
        print("   ✗ Timeout. Try again.\n")
    except sr.UnknownValueError:
        print("   ✗ Couldn't understand. Try again.\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    finally:
        _phrase_active.clear()


pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE,
                 input=True, frames_per_buffer=CHUNK)

clap_times = []

try:
    while True:
        try:
            raw = stream.read(CHUNK, exception_on_overflow=False)
        except Exception:
            time.sleep(0.005)
            continue

        now = time.time()
        if now < _cooldown_until or _phrase_active.is_set():
            continue

        audio = np.frombuffer(raw, dtype=np.int16)
        rms = float(np.sqrt(np.mean(audio.astype(np.float64) ** 2)))

        if rms < CLAP_THRESHOLD:
            continue

        if clap_times and now - clap_times[-1] < MIN_CLAP_GAP:
            continue

        clap_times.append(now)
        clap_times = [t for t in clap_times if now - t < CLAP_WINDOW]
        print(f"  👏  clap {len(clap_times)}  (rms {int(rms)})")

        if len(clap_times) >= 2:
            clap_times = []
            _phrase_active.set()
            threading.Thread(target=listen_for_phrase, daemon=True).start()

except KeyboardInterrupt:
    print("\nGoodnight, sir.\n")
finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
