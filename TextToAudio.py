# call through TextToAudio.translate(text)
# the code will play the audio version of the text

from gtts import gTTS
from pygame import mixer
import tempfile

def text_to_speech(text):
    # Convert text to speech
    tts = gTTS(text=text, lang='en')

    # Save the audio file
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts.save("{}.mp3".format(fp.name))
        return fp.name

def play_audio(file):
    # Initialize the mixer
    mixer.init()

    # Load the audio file
    mixer.music.load(file + ".mp3")

    # Play the audio file
    mixer.music.play()

def translate(text):
    # text = "9 1 1, what's your emergency?"
    audio_file = text_to_speech(text)
    play_audio(audio_file)
