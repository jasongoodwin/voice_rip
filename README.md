# voice_rip (for use with assistant!)
This is only the audio ripping portion of a meeting_assistant solution - pipe to an LLM and you can do some interesting things

## Setup

```
brew install portaudio

pyenv install 3.10.6
pyenv local 3.10.6
python3.10 -m venv .venv-assistant
. .venv-assistant/bin/activate
python --version
pip install -r requirements.txt
```

## Audio Conversion
You'll need a wav, and can process very long wavs, but you'll want to convert your sources into wav! You can use ffmpeg and, as an example, take the recordings from Apple's "Voice Memos" that come stock on the mac.

The audio signals are parsed gracefully handling multiple concurrent speakers etc. So you don't have to worry about having particularly clean input with many speakers. This won't identify unique speakers correctly but generally will gracefully handle a couple speakers talking over each other. In the context of use with an LLM, it's a great start at a useful tool.

To convert from a format to a `wav` file, you can install and use ffmpeg:

```
ffmpeg -i input.mp4 output.wav
```
