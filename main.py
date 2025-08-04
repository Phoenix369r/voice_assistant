import speech_recognition as sr
import pyttsx3
import datetime
import requests
import webbrowser
import smtplib
import schedule
import time
import google.generativeai as genai

# --- CHANGE: Add your API keys here ---
# Replace with your actual API keys
WEATHER_API_KEY = "bcf33f6d3d5c4adb65e4667de5783b7c"
GEMINI_API_KEY = "AIzaSyDgZcA82NurAFVzUJMBOyl9U94q-vwpERE"

# --- Text-to-Speech engine setup ---
engine = pyttsx3.init()
# --- CHANGE: Set voice to female ---
voices = engine.getProperty('voices')
# On most systems, voices[0] is male and voices[1] is female.
engine.setProperty('voice', voices[1].id)


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
            # You can uncomment the line below if you want the assistant to say something
            # speak("No speech detected.")
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
        # Note: Using an app password is required for Gmail SMTP.
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            # IMPORTANT: Replace with your Gmail address and App Password
            server.login(sender, "YOUR_GMAIL_APP_PASSWORD_HERE")
            msg = f"Subject: {subject}\n\n{message}"
            server.sendmail(sender, to_address, msg)
        speak("Email has been sent.")
    except Exception as e:
        speak(f"Failed to send email. Error: {e}")


# Weather API using OpenWeatherMap
def get_weather(city):
    # This function now uses the global WEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            speak("City not found or weather service is unavailable.")
        else:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp}°C with {desc}.")
    except requests.exceptions.RequestException:
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


# --- Gemini API Function (Modified) ---
def answer_with_gemini(query):
    """Gets an answer from the Gemini API using the hardcoded key."""
    try:
        # Configure the API key at the start of the function
        genai.configure(api_key=GEMINI_API_KEY)

        # Corrected model name
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(query)
        # Clean up the response text from markdown
        cleaned_text = response.text.replace('*', '').replace('#', '')
        speak(cleaned_text)
    except Exception as e:
        speak("Sorry, I encountered an error while trying to get an answer.")
        print(f"Gemini API Error: {e}")


def tell_date():
    today = datetime.date.today()
    speak(f"Today is {today.strftime('%B %d, %Y')}")


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
        # --- CHANGE: No longer asks for API key ---
        speak("Which city?")
        city = take_command()
        if city:
            get_weather(city)

    elif "remind me" in query:
        speak("What should I remind you about?")
        task = take_command()
        speak("At what time? Please say in HH:MM format.")
        time_str = take_command()
        if task and time_str:
            set_reminder(task, time_str)

    elif "turn on light" in query:
        control_device("light", True)
    elif "turn off light" in query:
        control_device("light", False)

    elif "open youtube" in query:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "time" in query:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "date" in query:
        tell_date()

    elif "day" in query:
        tell_day()

    elif "exit" in query or "goodbye" in query:
        speak("Goodbye!")
        exit()

    # --- All question-like queries go to Gemini ---
    elif query.endswith("?") or query.startswith(
            ("how", "why", "when", "where", "which", "explain", "define", "what", "who", "tell me about")):
        answer_with_gemini(query)
    else:
        # Fallback for any other unrecognized command
        speak("I'm not sure how to handle that, but I'll ask Gemini for you.")
        answer_with_gemini(query)


# Main loop to run the assistant
def run_assistant():
    speak("Voice assistant is now active.")
    while True:
        schedule.run_pending()
        query = take_command()
        if query:
            process_query(query)
        check_reminders()
        time.sleep(1)


# Start the assistant
if __name__ == "__main__":
    run_assistant()