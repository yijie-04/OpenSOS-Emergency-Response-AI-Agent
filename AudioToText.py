# when called, it will start listening and stop listening when there is a pause of 5 seconds
# the output will be a string of text that translated the audio message

# things to fix
# if nothing is spoken before timeout, there is error
import speech_recognition as sr

def translate():
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
