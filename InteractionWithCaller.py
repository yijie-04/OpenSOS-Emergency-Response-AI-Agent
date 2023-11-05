import AudioToText
import TextToAudio
import API_1
from info import Caller
import CheckMissingData
import pandas as pd

## Call is received

def Check(info):
    if info.caller_name == "XXX":
        return "What is your name?"
    elif info.incident_location == "XXX":
        return "Where are you?"
    elif info.incident_type == "XXX":
        return "What is the emergency?"
    elif info.symptoms == "XXX":
        return "What are the symptoms?"
    else:
        return None

keep_talking = 1
cur_caller = Caller()
# initial prompt
say = "9 1 1, what's your emergency?"


while keep_talking == 1:
    TextToAudio.translate(say)

    # receive audio input
    #input = AudioToText.translate()
    input1 = input("Enter response: ")
    print(input1)

    # send to AI Text Processing
    classification = API_1.get_completion(input1, cur_caller)
    print(classification)
        # actually dont need classification here, it is needed for backend stuff

#
    # Determine if we need more information
    say = Check(classification)
    if say == None:
        keep_talking = 0

filename = 'new_hacks_2023.json'
df = pd.read_json(filename)
name_list = df['first_name']
if classification.caller_name in name_list: 
    index = (list(name_list)).index(classification.caller_name)
    df_information = df.iloc[index]
    print(df_information)
print(classification)
    

