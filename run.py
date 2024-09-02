# run.py
import sys
import os

# Add the parent directory of 'meeting_assistant' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meeting_assistant.audio.speech_processor import SpeechProcessor

if __name__ == "__main__":
    processor = SpeechProcessor()
    result = processor.process("output.wav")
    for segment in result:
        print(f"{segment['speaker']}: {segment['text']}")
