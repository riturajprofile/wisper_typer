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
    config_path = os.path.expanduser("~/.wisper-typer")
    
    if not os.path.exists(config_path):
        print(f"⚠️  Config file not found at {config_path}")
        print("📝 Creating default config file...")
        with open(config_path, "w") as f:
            f.write("# Wisper-Linux Configuration\n")
            f.write("# Get your API key from https://console.groq.com/keys\n")
            f.write("GROQ_API_KEY=\n")
            f.write("# Hotkey to trigger recording (default: ctrl+win)\n")
            f.write("WISPER_HOTKEY=ctrl+win\n")
        print(f"✅ Created {config_path}")
        print("❌ Please edit this file and add your GROQ_API_KEY, then run wisper again.")
        sys.exit(1)

    load_dotenv(config_path)
    api_key = os.getenv("GROQ_API_KEY")
    hotkey = os.getenv("WISPER_HOTKEY", "ctrl+win")
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

def install_service():
    if os.geteuid() != 0:
        print("❌ Error: Must run as root to install service.")
        print("Try: sudo wisper --install-service")
        sys.exit(1)

    print("⚙️  Installing Wisper Typer Service...")
    
    # Locate service file within the package
    import pkg_resources
    try:
        service_content = pkg_resources.resource_string(__name__, "wisper_typer.service")
    except Exception:
        # Fallback for local dev
        if os.path.exists("wisper_typer.service"):
            with open("wisper_typer.service", "rb") as f:
                service_content = f.read()
        else:
            print("❌ Error: Could not find wisper_typer.service file.")
            sys.exit(1)

    service_path = "/etc/systemd/system/wisper_typer.service"
    with open(service_path, "wb") as f:
        f.write(service_content)

    print(f"✅ Service file copied to {service_path}")
    
    try:
        subprocess.run(["systemctl", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "enable", "wisper_typer"], check=True)
        subprocess.run(["systemctl", "start", "wisper_typer"], check=True)
        print("✅ Service started and enabled!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error enabling service: {e}")

def start():
    if len(sys.argv) > 1 and sys.argv[1] == "--install-service":
        install_service()
        return

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
