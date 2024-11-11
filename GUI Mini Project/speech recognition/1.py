import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pywhatkit

# Initialize the speech engine
engine = pyttsx3.init()

# Set voice rate (speed) and volume
engine.setProperty('rate', 150)  # Adjust speech speed
engine.setProperty('volume', 1.0)  # Maximum volume

# Function for the assistant to speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to take voice commands from the user
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # Wait for the user to finish speaking
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Could not understand your command. Please say that again...")
        return None
    return query.lower()

# Greet the user
def greet():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. How can I assist you today?")

# Main function that listens and processes commands
def jarvis():
    greet()
    while True:
        query = take_command()

        if query is None:
            continue

        # Basic commands that Jarvis can handle
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif 'play' in query:
            song = query.replace('play', '')
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'open code' in query:
            speak("Opening Visual Studio Code")
            codePath = "C:\\Users\\YourName\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'exit' in query:
            speak("Goodbye!")
            break

        else:
            speak("I don't understand the command. Please try again.")

if __name__ == "__main__":
    jarvis()
