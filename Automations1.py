"""
Automations for FRIDAY Voice Assistant
Desktop-only imports (pyttsx3, speech_recognition, pyautogui, selenium)
are wrapped in try/except so the web app works without them.
"""

import datetime
import time
from textblob import TextBlob
from PyDictionary import PyDictionary

# --- Optional desktop-only imports ---
try:
    import pyttsx3
    _engine = pyttsx3.init()
    voices = _engine.getProperty('voices')
    if voices:
        _engine.setProperty('voice', voices[0].id)
    _engine.setProperty('rate', 180)
    TTS_AVAILABLE = True
except Exception:
    _engine = None
    TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    from selenium import webdriver
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# --- Core functions ---

def speak(audio):
    print(f"FRIDAY: {audio}")
    if TTS_AVAILABLE and _engine:
        try:
            _engine.say(audio)
            _engine.runAndWait()
        except Exception:
            pass

def take_command():
    if not SR_AVAILABLE:
        return ""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except Exception:
        return ""

reminders = []

def set_reminder(task, time_interval):
    try:
        time_interval = int(time_interval)
    except ValueError:
        print("Invalid time interval. Please provide a valid integer.")
        return
    if time_interval <= 0:
        print("Invalid time interval. Please provide a positive value.")
        return
    current_time = datetime.datetime.now()
    reminder_time = current_time + datetime.timedelta(seconds=time_interval)
    reminders.append({"task": task, "reminder_time": reminder_time})

def check_reminders():
    current_time = datetime.datetime.now()
    for reminder in list(reminders):
        if current_time >= reminder["reminder_time"]:
            speak(f"Reminder: {reminder['task']}")
            reminders.remove(reminder)

def get_word_definition(word):
    dictionary = PyDictionary()
    try:
        definition = dictionary.meaning(word)
        if definition:
            return definition
        else:
            return {"error": "Definition not found for the given word."}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    if sentiment.polarity > 0:
        return "positive"
    elif sentiment.polarity < 0:
        return "negative"
    else:
        return "neutral"

def convert_length(value, from_unit, to_unit):
    conversion_factors = {
        "meters_to_feet": 3.281, "feet_to_meters": 0.305,
        "meters_to_inches": 39.37, "inches_to_meters": 0.0254,
        "feet_to_yards": 0.3333, "yards_to_feet": 3,
        "cm_to_meters": 0.01, "meters_to_cm": 100,
        "meters_to_km": 0.001, "km_to_meters": 1000,
        "mm_to_meters": 0.001, "meters_to_mm": 1000,
        "miles_to_km": 1.60934, "km_to_miles": 0.621371,
    }
    conversion_key = f"{from_unit}to{to_unit}"
    if conversion_key not in conversion_factors:
        print("Invalid conversion units.")
        return None
    return value * conversion_factors[conversion_key]
