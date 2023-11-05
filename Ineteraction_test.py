import AudioToText
import TextToAudio
import API_1
from info import Caller
import CheckMissingData
from Interface import App
import globals

## Call is received
keep_talking = 1
cur_caller = Caller()

# set up interface
# import tkinter
# import tkinter.messagebox
# import customtkinter
# customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
# customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
start_app = 1
# app = App()
# app.mainloop()

# initial prompt
say = "9 1 1, what's your emergency?"

while keep_talking == 1:
    TextToAudio.translate(say)
    globals.transcript("911:" + say + "\n")

    # receive audio input
    input = AudioToText.translate()
    globals.transcript("911:" + input + "\n")

    # send to AI Text Processing
    API_1.get_completion(input, cur_caller)
        # actually dont need classification here, it is needed for backend stuff
    if start_app == 1:
        app = App()
        app.mainloop()
    # Determine if we need more information
    say = CheckMissingData.check(cur_caller)
    if say == None:
        keep_talking = 0

    

