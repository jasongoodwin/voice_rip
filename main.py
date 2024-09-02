from meeting_assistant.audio.speech_processor import SpeechProcessor

if __name__ == "__main__":
    processor = SpeechProcessor()
    result = processor.process("output.wav")
    for segment in result:
        print(f"{segment['speaker']}: {segment['text']}")
