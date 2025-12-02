import os
import sys
import time
import logging
from logging.handlers import RotatingFileHandler
import pyaudio
import wave
import keyboard
import pyperclip
import tempfile
import subprocess
import shutil
from typing import Optional, Tuple
from groq import Groq
from dotenv import load_dotenv

# Try to use modern importlib.resources, fallback to pkg_resources
try:
    from importlib.resources import files
    USE_IMPORTLIB = True
except ImportError:
    try:
        import pkg_resources
        USE_IMPORTLIB = False
    except ImportError:
        USE_IMPORTLIB = None

load_dotenv()
load_dotenv(os.path.expanduser("~/.wisper-typer"))


def setup_logging() -> logging.Logger:
    """Setup logging with rotation to ~/.wisper-typer.log"""
    log_path = os.path.expanduser("~/.wisper-typer.log")
    
    logger = logging.getLogger("wisper_typer")
    logger.setLevel(logging.DEBUG)
    
    # Avoid adding multiple handlers if function is called multiple times
    if logger.handlers:
        return logger
    
    # Rotating file handler: 5MB max, keep 3 backups
    file_handler = RotatingFileHandler(
        log_path, 
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler for important messages
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logging()


def get_config() -> Tuple[Optional[str], str]:
    """Load configuration from ~/.wisper-typer file"""
    config_path = os.path.expanduser("~/.wisper-typer")
    
    if not os.path.exists(config_path):
        logger.warning(f"Config file not found at {config_path}")
        print(f"⚠️  Config file not found at {config_path}")
        print("📝 Creating default config file...")
        with open(config_path, "w") as f:
            f.write("# Wisper-Linux Configuration\n")
            f.write("# Get your API key from https://console.groq.com/keys\n")
            f.write("GROQ_API_KEY=\n")
            f.write("# Hotkey to trigger recording (default: ctrl+win)\n")
            f.write("WISPER_HOTKEY=ctrl+win\n")
        logger.info(f"Created default config file at {config_path}")
        print(f"✅ Created {config_path}")
        print("❌ Please edit this file and add your GROQ_API_KEY, then run wisper again.")
        sys.exit(1)

    load_dotenv(config_path)
    api_key = os.getenv("GROQ_API_KEY")
    hotkey = os.getenv("WISPER_HOTKEY", "ctrl+win")
    
    logger.debug(f"Loaded config: hotkey={hotkey}, api_key={'present' if api_key else 'missing'}")
    return api_key, hotkey


def record_audio(hotkey: str, p: pyaudio.PyAudio) -> Optional[str]:
    """Record audio while hotkey is pressed. Returns path to temp WAV file."""
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000

    try:
        stream = p.open(format=format, channels=channels, rate=rate, input=True,
                        frames_per_buffer=chunk)
    except IOError as e:
        logger.error(f"Microphone error: {e}")
        print("❌ Error: Microphone not found or busy.")
        return None

    logger.info(f"Recording started (hotkey: {hotkey})")
    print(f"🎤 Recording... (Release '{hotkey}' to stop)")
    frames = []

    while keyboard.is_pressed(hotkey):
        try:
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)
        except IOError as e:
            logger.warning(f"Audio read error: {e}")
            break

    stream.stop_stream()
    stream.close()
    
    logger.info(f"Recording stopped. Captured {len(frames)} frames")

    if not frames:
        logger.warning("No audio frames captured")
        return None

    # Store sample size BEFORE terminating PyAudio (FIX: Bug #1)
    sample_size = p.get_sample_size(format)

    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            wf = wave.open(temp_wav.name, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(sample_size)  # Use stored value
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            logger.debug(f"Audio saved to temp file: {temp_wav.name}")
            return temp_wav.name
    except Exception as e:
        logger.error(f"Failed to save audio file: {e}", exc_info=True)
        return None


def transcribe(filename: str, client: Groq) -> Optional[str]:
    """Transcribe audio file using Groq API"""
    if not filename:
        return None
    
    try:
        logger.debug(f"Transcribing file: {filename}")
        with open(filename, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(filename, file.read()),
                model="whisper-large-v3-turbo",
                response_format="text"
            ).strip()
        logger.info(f"Transcription successful: '{transcription}'")
        return transcription
    except Exception as e:
        logger.error(f"API Error during transcription: {e}", exc_info=True)
        print(f"❌ API Error: {e}")
        return None


def type_text(text: str) -> None:
    """Type text into active window using clipboard + Ctrl+V"""
    if not text:
        logger.warning("Empty text, nothing to type")
        return

    logger.info(f"Typing text: {text}")
    print(f"📝 Typing: {text}")
    
    # Wayland Clipboard Support (wl-copy)
    clipboard_success = False
    if shutil.which("wl-copy"):
        try:
            subprocess.run(["wl-copy", text], check=True, timeout=1)
            clipboard_success = True
            logger.debug("Clipboard set via wl-copy")
        except Exception as e:
            logger.warning(f"wl-copy failed: {e}")
            print(f"⚠️ wl-copy failed: {e}")
    
    # Fallback to pyperclip
    if not clipboard_success:
        try:
            pyperclip.copy(text)
            clipboard_success = True
            logger.debug("Clipboard set via pyperclip")
        except Exception as e:
            logger.error(f"Clipboard copy failed: {e}")
            print(f"❌ Failed to copy to clipboard: {e}")
            return

    # Add delay for clipboard to be ready (FIX: Performance improvement #3)
    time.sleep(0.05)  # 50ms delay
    
    # Verify clipboard content
    try:
        if shutil.which("wl-paste"):
            result = subprocess.run(["wl-paste"], capture_output=True, text=True, timeout=1)
            clipboard_content = result.stdout
        else:
            clipboard_content = pyperclip.paste()
        
        if clipboard_content != text:
            logger.warning(f"Clipboard verification failed. Expected: '{text}', Got: '{clipboard_content}'")
    except Exception as e:
        logger.warning(f"Clipboard verification error: {e}")

    # Simulate Ctrl+V using keyboard (works on Wayland via uinput)
    try:
        keyboard.send("ctrl+v")
        logger.debug("Sent Ctrl+V keystroke")
    except Exception as e:
        logger.error(f"Failed to send Ctrl+V: {e}")


def install_service() -> None:
    """Install systemd service for auto-start"""
    if os.geteuid() != 0:
        logger.error("Service installation attempted without root privileges")
        print("❌ Error: Must run as root to install service.")
        print("Try: sudo wisper --install-service")
        sys.exit(1)

    logger.info("Installing Wisper Typer service...")
    print("⚙️  Installing Wisper Typer Service...")
    
    # Locate service file within the package
    service_content = None
    
    if USE_IMPORTLIB:
        # Modern approach with importlib.resources
        try:
            service_file = files(__package__) / "wisper_typer.service"
            service_content = service_file.read_bytes()
            logger.debug("Loaded service file via importlib.resources")
        except Exception as e:
            logger.warning(f"Failed to load service file via importlib: {e}")
    elif USE_IMPORTLIB is False:
        # Fallback to pkg_resources
        try:
            service_content = pkg_resources.resource_string(__name__, "wisper_typer.service")
            logger.debug("Loaded service file via pkg_resources")
        except Exception as e:
            logger.warning(f"Failed to load service file via pkg_resources: {e}")
    
    # Final fallback for local dev
    if service_content is None:
        if os.path.exists("wisper_typer.service"):
            with open("wisper_typer.service", "rb") as f:
                service_content = f.read()
            logger.debug("Loaded service file from local directory")
        else:
            logger.error("Could not find wisper_typer.service file")
            print("❌ Error: Could not find wisper_typer.service file.")
            sys.exit(1)

    service_path = "/etc/systemd/system/wisper_typer.service"
    with open(service_path, "wb") as f:
        f.write(service_content)

    logger.info(f"Service file copied to {service_path}")
    print(f"✅ Service file copied to {service_path}")
    
    try:
        subprocess.run(["systemctl", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "enable", "wisper_typer"], check=True)
        subprocess.run(["systemctl", "start", "wisper_typer"], check=True)
        logger.info("Service started and enabled successfully")
        print("✅ Service started and enabled!")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error enabling service: {e}")
        print(f"❌ Error enabling service: {e}")


def start() -> None:
    """Main entry point for wisper application"""
    logger.info("=== Wisper Typer Starting ===")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--install-service":
        install_service()
        return

    api_key, hotkey = get_config()

    if not api_key:
        logger.critical("API Key missing in configuration")
        print("\n❌ CRITICAL ERROR: API Key missing.")
        print("Please export your key:")
        print("  export GROQ_API_KEY='gsk_...'")
        sys.exit(1)

    client = Groq(api_key=api_key)
    logger.info("Groq client initialized")

    print("\n--- 🐧 Wisper Typer (Ultra-Fast) ---")
    print(f"✅ API Key Detected")
    print(f"⌨️  Hotkey: {hotkey}")
    print(f"🚀 Model: whisper-large-v3-turbo")
    print(f"📋 Log file: ~/.wisper-typer.log")
    print(f"👂 Status: Listening... (Press Ctrl+C to quit)")

    if os.geteuid() != 0:
        logger.warning("Running without sudo - hotkeys and typing may fail")
        print("⚠️ WARNING: Not running as sudo. Global hotkeys and typing may fail.")

    # Create PyAudio instance once and reuse (FIX: Performance improvement #1)
    p = pyaudio.PyAudio()
    logger.info("PyAudio instance created")
    
    # Rate limiting variables (FIX: Performance improvement #2)
    last_transcription_time = 0
    min_cooldown = 0.5  # 500ms minimum between transcriptions

    try:
        while True:
            try:
                keyboard.wait(hotkey)
                
                # Small delay to ensure key is still pressed (FIX: Race condition bug #3)
                time.sleep(0.05)
                
                # Rate limiting check
                current_time = time.time()
                time_since_last = current_time - last_transcription_time
                if time_since_last < min_cooldown:
                    remaining = min_cooldown - time_since_last
                    logger.warning(f"Rate limit: waiting {remaining:.2f}s")
                    print(f"⏳ Please wait {remaining:.2f}s before next recording")
                    continue
                
                audio_file = None
                try:
                    # Record, transcribe, and type (FIX: Proper cleanup in finally block)
                    audio_file = record_audio(hotkey, p)
                    if audio_file:
                        text = transcribe(audio_file, client)
                        if text:
                            type_text(text)
                            last_transcription_time = time.time()
                finally:
                    # ALWAYS clean up temp file (FIX: Bug #2)
                    if audio_file and os.path.exists(audio_file):
                        try:
                            os.remove(audio_file)
                            logger.debug(f"Cleaned up temp file: {audio_file}")
                        except Exception as e:
                            logger.warning(f"Failed to delete temp file {audio_file}: {e}")
                            
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                print("\n👋 Exiting.")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
                print(f"⚠️ Error: {e}")
    finally:
        # Clean up PyAudio instance on exit
        p.terminate()
        logger.info("PyAudio instance terminated")
        logger.info("=== Wisper Typer Stopped ===")


if __name__ == "__main__":
    start()
