import pyttsx3
import pyaudio
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib

# Initialize pyttsx3 (change 'sapi5' to 'nsss' for macOS)
engine = pyttsx3.init('nsss')  # 'sapi5' for Windows

def speak(audio ):
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Greet the user based on time."""
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")     
    else:
        speak("Good Evening!")  
    speak("I am your AI Assistant. How may I help you?")              

def takeCommand():
    """Take voice input from the user and return as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 100
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        print("Say that again, please...")
        return "None"
    
    return query.lower()

def sendEmail(to, content): 
    """Send an email using SMTP."""
    try:
        sender_email = os.getenv("EMAIL_USER")  # Use environment variable
        sender_password = os.getenv("EMAIL_PASS")  # Use environment variable
        if not sender_email or not sender_password:
            raise ValueError("Missing email credentials in environment variables.")

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to, content)
        server.close()
        speak("Email has been sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I am unable to send the email at this moment.")

if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com") 

        elif 'open google' in query:
            webbrowser.open("https://google.com") 

        elif 'open stackoverflow' in query:
            webbrowser.open("https://stackoverflow.com")

        elif 'play music' in query:
            music_dir = '/Users/hariomkasaundhan/Music/'  # Update path
            songs = os.listdir(music_dir)
            if songs:
                os.system(f"open {os.path.join(music_dir, songs[0])}")  # Open music on macOS
            else:
                speak("No music files found.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            code_path = "/Applications/Visual Studio Code.app"  # Update for macOS
            os.system(f"open {code_path}")

        elif 'email to shivam' in query:
            speak("What should I say?")
            content = takeCommand()
            sendEmail("shivam@example.com", content)  # Replace with actual email

        elif 'exit' in query or 'stop' in query:
            speak("Goodbye! Have a great day.")
            break
