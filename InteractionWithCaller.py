import AudioToText
import TextToAudio
import API_1

## Call is received


keep_talking = 1
# initial prompt
say = "9 1 1, what's your emergency?"
while keep_talking == 1:
    TextToAudio.translate(say)

    # receive audio input
    input = AudioToText.translate()
    print(input)

    # send to AI Text Processing
    response = API_1.get_completion(input)
    print(response)

    keep_talking = 0

