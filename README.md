# Voice-Activated AI Personal Assistant

A Python-based voice assistant that leverages speech recognition, text-to-speech, OpenWeatherMap for weather, Google Gemini for AI Q&A, reminders, smart home simulation, and more. Powered by `speech_recognition`, `pyttsx3`, Google Gemini API, and more.

---

## ✨ Features

- **Conversational Voice Assistant** — Interact with natural speech, not just commands.
- **Text-to-Speech** — Female voice for responses (via `pyttsx3`).
- **Speech Recognition** — Accurate voice input using your microphone.
- **Google Gemini Integration** — Ask any question and get intelligent, AI-powered answers.
- **Weather Updates** — Get real-time weather for any city (OpenWeatherMap).
- **Reminders** — Set and receive reminders at specified times.
- **Email Sending** — Send basic emails via Gmail (requires app password).
- **Smart Home Simulation** — Simulate turning lights on and off.
- **Web Actions** — Open websites like YouTube via voice command.
- **Date, Day, and Time** — Ask for the current date, day of week, or time.
- **Extensible Command Handling** — All questions are answered via Gemini AI, or fallback if unknown.

---

## 🖥️ Demo

![Voice Assistant Demo](https://user-images.githubusercontent.com/0000000/demo.gif)

---

## 🚀 Getting Started

### 1. **Clone This Repository**

```bash
git clone https://github.com/yourusername/voice-ai-assistant.git
cd voice-ai-assistant
```

### 2. **Install Requirements**

```bash
pip install -r requirements.txt
```

#### Requirements:

- `speech_recognition`
- `pyttsx3`
- `requests`
- `schedule`
- `google-generativeai`
- `pyaudio` (for microphone input)
- `datetime`
- `smtplib`
- `webbrowser`

> **Note:** On some systems, you may need to install `pyaudio` separately.  
> For Windows: `pip install pipwin && pipwin install pyaudio`  
> For Mac: `brew install portaudio` then `pip install pyaudio`

### 3. **API Keys Setup**

- **OpenWeatherMap:** [Get a free API key](https://openweathermap.org/api)
- **Google Gemini:** [Get Gemini API key](https://aistudio.google.com/app/apikey)
- **Gmail App Password:** [Learn how to generate one](https://support.google.com/mail/answer/185833?hl=en)

Open the script and **replace** these placeholders at the top:

```python
WEATHER_API_KEY = "your_openweathermap_api_key"
GEMINI_API_KEY = "your_gemini_api_key"
# In send_email(): Replace "YOUR_GMAIL_APP_PASSWORD_HERE" with your Gmail app password
```

---

## 🎤 Usage

Simply run:

```bash
python your_script_name.py
```

- The assistant will greet you and start listening.
- **Example commands:**
    - "What's the weather in Paris?"
    - "Remind me to call John at 14:30"
    - "Send an email"
    - "Turn on light"
    - "Open YouTube"
    - "What's the time?"
    - "Who invented Python?"
    - "Goodbye" (to exit)

---

## ⚡ Hotkeys & Tips

- **Say "goodbye" or "exit"** to stop the assistant.
- For email: you’ll be prompted to **type** addresses and messages for security.
- Reminders are stored **in-memory** (reset on restart).
- All unknown or complex queries are answered via Gemini AI.

---

## 🛡️ Security Notes

- Your API keys and Gmail app password are required for full functionality.
- Never share your credentials publicly.
- For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833?hl=en), not your main password.

---

## 🛠️ Customization

- Add your own commands in the `process_query()` function.
- Change the assistant's voice by modifying the `pyttsx3` settings.
- Integrate with real smart home APIs for actual device control.

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to submit issues or pull requests.



---

> **Made with ❤️ for modern AI-powered productivity**
