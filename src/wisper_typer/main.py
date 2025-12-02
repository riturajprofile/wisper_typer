import os
import sys
import pyaudio
import wave
import keyboard
import pyperclip
import tempfile
import subprocess
import shutil
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
load_dotenv(os.path.expanduser("~/.wisper-typer"))


def get_config():
    api_key = os.getenv("GROQ_API_KEY")
    hotkey = os.getenv("WISPER_HOTKEY", "f4")
    return api_key, hotkey

def record_audio(hotkey):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000

    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=format, channels=channels, rate=rate, input=True,
                        frames_per_buffer=chunk)
    except IOError:
        print("❌ Error: Microphone not found or busy.")
        return None

    print(f"🎤 Recording... (Release '{hotkey}' to stop)")
    frames = []

    while keyboard.is_pressed(hotkey):
        data = stream.read(chunk, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    if not frames:
        return None

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        wf = wave.open(temp_wav.name, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        return temp_wav.name

def transcribe(filename, client):
    if not filename:
        return None
    try:
        with open(filename, "rb") as file:
            return client.audio.transcriptions.create(
                file=(filename, file.read()),
                model="whisper-large-v3-turbo",
                response_format="text"
            ).strip()
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None

def type_text(text):
    if not text:
        return

    print(f"📝 Typing: {text}")
    
    # Wayland Clipboard Support (wl-copy)
    if shutil.which("wl-copy"):
        try:
            subprocess.run(["wl-copy", text], check=True)
        except Exception as e:
            print(f"⚠️ wl-copy failed: {e}")
            pyperclip.copy(text) # Fallback
    else:
        pyperclip.copy(text)

    # Simulate Ctrl+V using keyboard (works on Wayland via uinput)
    keyboard.send("ctrl+v")

def start():
    api_key, hotkey = get_config()

    if not api_key:
        print("\n❌ CRITICAL ERROR: API Key missing.")
        print("Please export your key:")
        print("  export GROQ_API_KEY='gsk_...'")
        sys.exit(1)

    client = Groq(api_key=api_key)

    print("\n--- 🐧 Wisper Typer (Ultra-Fast) ---")
    print(f"✅ API Key Detected")
    print(f"⌨️  Hotkey: {hotkey}")
    print(f"🚀 Model: whisper-large-v3-turbo")
    print(f"👂 Status: Listening... (Press Ctrl+C to quit)")

    if os.geteuid() != 0:
        print("⚠️ WARNING: Not running as sudo. Global hotkeys and typing may fail.")

    while True:
        try:
            keyboard.wait(hotkey)
            audio_file = record_audio(hotkey)
            text = transcribe(audio_file, client)
            type_text(text)
            if audio_file:
                os.remove(audio_file)
        except KeyboardInterrupt:
            print("\n👋 Exiting.")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    start()
