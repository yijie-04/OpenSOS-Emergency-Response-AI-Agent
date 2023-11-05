import AudioToText
import TextToAudio
import API_1
from info import Caller
import CheckMissingData

## Call is received


keep_talking = 1
cur_caller = Caller()
# initial prompt
say = "9 1 1, what's your emergency?"
while keep_talking == 1:
    TextToAudio.translate(say)

    # receive audio input
    input = AudioToText.translate()
    print(input)

    # send to AI Text Processing
    classification = API_1.get_completion(input, cur_caller)
    print(classification)
        # actually dont need classification here, it is needed for backend stuff

    # Determine if we need more information
    say = CheckMissingData.check(cur_caller)
    if say == None:
        keep_talking = 0

    

