import pvporcupine
import pyaudio
import struct
import os
from dotenv import load_dotenv
from python_backend.voice import listen_command
from python_backend.ai_engine import process_command
from python_backend.logger import log_info, log_error, log_warning

load_dotenv()
ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY", "YOUR_PICOVOICE_ACCESS_KEY")

def start_wake_word():
    """Start wake word detection for 'Hey VEDA'"""
    if not ACCESS_KEY or ACCESS_KEY == "YOUR_PICOVOICE_ACCESS_KEY" or ACCESS_KEY == "your_picovoice_access_key_here":
        log_warning("Wake word detection disabled: Please set PICOVOICE_ACCESS_KEY in .env")
        print("⚠️ Wake word detection disabled: Please set PICOVOICE_ACCESS_KEY in .env")
        return

    porcupine = None
    pa = None
    stream = None
    
    try:
        log_info("Initializing wake word detection...")
        
        # Try to use custom "Hey Veda" wake word if available
        custom_wake_word_path = os.path.join("python_frontend", "sounds", "Hey-Veda_en_windows_v4_0_0.ppn")
        
        if os.path.exists(custom_wake_word_path):
            log_info("Using custom 'Hey VEDA' wake word")
            porcupine = pvporcupine.create(
                access_key=ACCESS_KEY,
                keyword_paths=[custom_wake_word_path]
            )
        else:
            log_info("Using default 'computer' wake word")
            porcupine = pvporcupine.create(
                access_key=ACCESS_KEY,
                keywords=["computer"]  # Using "computer" as wake word (closest to VEDA)
            )

        pa = pyaudio.PyAudio()
        stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("🟢 VEDA AI is always listening for wake word...")
        log_info("Wake word detection active")

        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from(
                "h" * porcupine.frame_length,
                pcm
            )

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("🔥 Wake word detected!")
                log_info("Wake word detected")
                command = listen_command()
                if command:
                    process_command(command)

    except Exception as e:
        log_error(f"Wake word error: {e}")
        print(f"❌ Wake word error: {e}")
    finally:
        if stream is not None:
            try:
                stream.close()
            except:
                pass
        if pa is not None:
            try:
                pa.terminate()
            except:
                pass
        if porcupine is not None:
            try:
                porcupine.delete()
            except:
                pass
        log_info("Wake word detection cleanup completed")
