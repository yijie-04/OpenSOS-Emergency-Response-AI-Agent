import AudioToText
import TextToAudio

## Call is received

# initial prompt
TextToAudio.translate("9 1 1, what's your emergency?")

# receive audio input
input = AudioToText.translate()
print(input)
