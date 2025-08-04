import speech_recognition as sr
import pyttsx3
import datetime
import requests
import webbrowser
import smtplib
import json
import schedule
import time
import google.generativeai as genai

# Text-to-Speech engine setup
engine = pyttsx3.init()
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Listen from microphone
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=20)
            query = r.recognize_google(audio)
            print(f"User: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            speak("No speech detected.")
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Speech service is down.")
            return ""


# Send email (basic)
def send_email(sender, to_address, subject, message):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, "itlfmkniqovoebuu")
            msg = f"Subject: {subject}\n\n{message}"
            server.sendmail(sender, to_address, msg)
        speak("Email has been sent.")
    except Exception as e:
        speak(f"Failed to send email. Error: {e}")

# Weather API using OpenWeatherMap
def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            speak("City not found.")
        else:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp}°C with {desc}.")
    except:
        speak("Weather service is currently unreachable.")

# Reminder setup (temporary memory)
reminders = []
def set_reminder(reminder, remind_time):
    reminders.append((reminder, remind_time))
    speak(f"Reminder set for {remind_time} to: {reminder}")

# Check reminders
def check_reminders():
    now = datetime.datetime.now().strftime("%H:%M")
    for r in reminders[:]:
        if r[1] == now:
            speak(f"Reminder: {r[0]}")
            reminders.remove(r)

# Smart home device simulation
def control_device(device, state):
    speak(f"{device} turned {'on' if state else 'off'}.")



def answer_question_offline(query):
    try:

        genai.configure(api_key="50c93d60-c569-49c5-b864-5211feb2e3f7")  # Replace with your actual key

        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(query)

        answer = response.text.strip()
        speak(answer)
        print(f"💡 Gemini Answer:\n{answer}")

    except Exception as e:
        speak("Sorry, Gemini couldn't process the request.")
        print(f"Error: {e}")


def tell_date():
    today = datetime.date.today()
    speak(f"Today's date is {today.strftime('%B %d, %Y')}")

def tell_day():
    today = datetime.date.today()
    speak(f"Today is {today.strftime('%A')}")

# Main processing
def process_query(query):
    if "email" in query:
        speak("Please type your Gmail address.")
        sender = input("Sender Email: ")

        speak("Who is the recipient?")
        to = input("Recipient Email: ")

        speak("Please type the subject of your email.")
        subject = input("Subject: ")

        speak("Now type your message.")
        message = input("Message: ")

        send_email(sender, to, subject, message)


    elif "weather" in query:
        speak("Please type your OpenWeatherMap API key.")
        api_key = input("Enter your weather API key: ")

        speak("Which city?")
        city = take_command()

        get_weather(city, api_key)


    elif "remind me" in query:
        speak("What should I remind you about?")
        task = take_command()
        speak("At what time? Please say in HH:MM format.")
        time_str = take_command()
        set_reminder(task, time_str)

    elif "turn on light" in query:
        control_device("light", True)
    elif "turn off light" in query:
        control_device("light", False)






    elif "open youtube" in query:
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")

    elif "time" in query:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    elif "date" in query:
        tell_date()

    elif "day" in query:
        tell_day()

    elif "exit" in query:
        speak("Goodbye!")
        exit()

    elif query.endswith("?") or query.startswith(
            ("how", "why", "when", "where", "which", "explain", "define", "what", "who", "tell me about")):
        answer_question_offline(query)
    else:
        speak("Let me try to find something useful for you.")
        answer_question_offline(query)



# Scheduler loop for checking reminders
def run_assistant():
    speak("Voice assistant is now active.")
    while True:
        schedule.run_pending()
        query = take_command()
        if query:
            process_query(query)
        check_reminders()

# Start the assistant
if __name__ == "__main__":
    run_assistant()
