import os
import json
import pandas as pd
import openai
from dotenv import load_dotenv, find_dotenv
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
import tempfile
import time
openai.api_key  = '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'

import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



def Check(info):
    if info["name"] == "XXX":
        return "What is your name?"
    elif info["location"] == "XXX":
        return "Where are you?"
    elif info["type"] == "XXX":
        return "What is the emergency?"
    elif info["symptoms"] == "XXX":
        return "What are the symptoms?"
    else:
        return None

def AtoT():
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # use the microphone as source for input. Here, we also specify
    # which device ID to specifically look for incase the microphone
    # is not working, an error will pop up saying "device_id undefined"
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source, timeout=5, phrase_time_limit=10)
        print("Time over, thanks")
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling

        try:
            # using google speech recognition
            print("Text: "+r.recognize_google(audio_text))
            return r.recognize_google(audio_text)
        except:
            print("Sorry, I did not get that")

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
    while mixer.music.get_busy():  # wait for the audio to finish
        time.sleep(0.1)

def translate(text):
    # text = "9 1 1, what's your emergency?"
    audio_file = text_to_speech(text)
    play_audio(audio_file)

def get_emergency_info(call, name_list,  cur_info, model="gpt-3.5-turbo"): 
    prompt = f"""role':'system', 'content':
            Get information from the following text ```{call}``` and ```{cur_info}`` in an emergency caller\
            1. name of the caller: use the list in```{name_list}``` and get the name
               if the actual name getting from the text does not match, then choose the most similar one of the first name
            2. emergency types: FIRE CALLS, POLICE CALLS, EMS CALLS\
            3. the incident location (as short as possible)\
            4. the symptoms (as short as possible)\

            Note:
            if any of the information is not available, put XXX as the value.\
            if all the information has a value
            
            Output:
            save all the information in JSON format, with the key: name, type, location, symptoms\
            """
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

def get_sug(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

class App(customtkinter.CTk):
    def __init__(self, input_keyInput, input_database, input_transcript):
        super().__init__()

        # configure window
        self.title("OpenSOS.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="OpenSOS", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.open_input_dialog_event_hospital)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.open_input_dialog_event_ambulance)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.open_input_dialog_event_family)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create bottom text entry
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Comments")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create database
        self.database = customtkinter.CTkFrame(self)  # fg_color="transparent"
        self.database.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.database.grid_columnconfigure(0, weight=1)
        self.database.grid_rowconfigure(4, weight=1)
        self.database_label = customtkinter.CTkLabel(self.database, text="Database", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.database_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))
        self.database_text = customtkinter.CTkTextbox(self.database, width=150)
        self.database_text.grid(row=1, column=0,rowspan=5, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.database_text.insert("0.0", input_database + "\n\n")

        # create transcript
        self.transcript = customtkinter.CTkFrame(self)  # fg_color="transparent"
        self.transcript.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.transcript.grid_columnconfigure(0, weight=1)
        self.transcript.grid_rowconfigure(4, weight=1)
        self.transcript_label = customtkinter.CTkLabel(self.transcript, text="Transcript", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.transcript_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))
        self.transcript_text = customtkinter.CTkTextbox(self.transcript, width=150)
        self.transcript_text.grid(row=1, column=0,rowspan=5, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.transcript_text.insert("0.0",  input_transcript + "\n\n" )


        # create Key Info
        self.keyInfo = customtkinter.CTkFrame(self)  # fg_color="transparent"
        self.keyInfo.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.keyInfo.grid_columnconfigure(0, weight=1)
        self.keyInfo.grid_rowconfigure(4, weight=1)
        self.keyInfo_label = customtkinter.CTkLabel(self.keyInfo, text="Key Info", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.keyInfo_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))
        self.keyInfo_text = customtkinter.CTkTextbox(self.keyInfo, width=150)
        self.keyInfo_text.grid(row=1, column=0,rowspan=5, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.keyInfo_text.insert("0.0", input_keyInfo + "\n\n")


        # create Emergency Response sending
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Send Emergency Response")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(1, 4):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"Fire DEP {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)
        for j in range(4, 7):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"EMT DEP {j}")
            switch.grid(row=j, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)
        for k in range(7, 11):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"Police DEP {k}")
            switch.grid(row=k, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)


        # set default values
        # self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        # self.scrollable_frame_switches[0].select()
        # self.scrollable_frame_switches[4].select()
        # self.appearance_mode_optionemenu.set("Dark")
        # self.scaling_optionemenu.set("100%")
        

    def open_input_dialog_event_hospital(self):
        dialog = customtkinter.CTkInputDialog(text="To hospital:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())
    def open_input_dialog_event_family(self):
        dialog = customtkinter.CTkInputDialog(text="To family:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())
    def open_input_dialog_event_ambulance(self):
        dialog = customtkinter.CTkInputDialog(text="To ambulance:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

################################################################################################################

if __name__ == "__main__":
    
    filename = 'new_hacks_2023.json'
    keep_talking = 1
    say = "9 1 1, what's your emergency?"
    df = pd.read_json(filename)
    name_list = df['first_name']
    cur_info = ''

    while keep_talking == 1:
        translate(say)

        # receive audio input
        #input = AtoT()
        #print(input)

        input = """
            My name is Amy. My friend fell down the stairs. Her ankle is swollen and 
            her nose is bleeding. We are in 100 College St.\
        """
        transc = transc + say + "\n" + input + "\n"

        # send to AI Text Processing 
        response = get_emergency_info(input, cur_info, name_list)
        cur_info = response
        response_js = json.loads(response)
        print(response_js)
        print(type(response_js))

        say = Check(response_js)
        if say == None:
            keep_talking = 0

    index = (list(name_list)).index(response_js.get('name'))
    df_information = df.iloc[index]
    print(df_information)

    # hospital information
    prompt_hos = f"""role':'system', 'content':
                Get information from the following dataframe ```{df_information}``` and ```{response_js}``` base on an emergency caller\
                provide two specific suggestions each less than 20 words for the hospital to prepare\
                
                Output:
                in JSON style\
                """
    hos_sug = get_sug(prompt_hos)
    print(hos_sug)

    #ambulence information
    prompt_amb = f"""role':'system', 'content':
                Get information from the following dataframe ```{df_information}``` and ```{response_js}``` base on an emergency caller\
                provide two specific suggestions each less than 20 words for the coming ambulence to prepare\
                template of specific suggestions could be certain equipment and action\
                
                Output:
                in JSON style\
                """
    amb_sug = get_sug(prompt_amb)
    print(amb_sug)

    #for family
    prompt_fam = f"""role':'system', 'content':
                Get information from the following dataframe ```{df_information}```, ```{df}``` and base on an emergency caller\
                and write a message to the family group with the same family_id\
                briefly explain the current situation based on ```{response_js}``` in kind and concise language\
                and inform them to come to hospital\
                
                Output:
                in JSON style\
                """
    fam_sug = get_sug(prompt_fam)
    print(fam_sug)

    data, response_js, df = final_data()
    hos_sug, amb_sug, fam_sug = final_suggestions(data, response_js, df)
    input_keyInfo = "Lets just test it"
    sex_char = 'F' if data['sex'] == 1 else 'M'
    input_database = f"First name: {data['first_name']}\nLast name: {data['last_name']} \n\n Age: {data['age']}\Sex:{sex_char}\n Blood type: {data['blood_type']}\n \
                                    Allergies: {data['allergies']} \tPast_disease: {data['past_desease']} \n\Family id: {data['family_id']}\n Address: {data['address']}"
    input_transcript = "911: 9-1-1, what is your emergency? \nCaller: My house burned down\n 911: What is your name?"
    app = App(input_keyInfo, input_database, input_transcript)
    app.mainloop()

