"""
Basic Features for FRIDAY Voice Assistant
Reconstructed to support core logic
"""

import datetime
import webbrowser
import requests
import wikipedia

# pyttsx3 is a desktop/Windows-only library — skip gracefully in web/server mode
try:
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    TTS_AVAILABLE = True
except Exception:
    engine = None
    TTS_AVAILABLE = False

def speak(audio):
    """Speak the given audio text (falls back to print in server mode)."""
    print(f"FRIDAY: {audio}")
    if TTS_AVAILABLE and engine:
        try:
            engine.say(audio)
            engine.runAndWait()
        except Exception:
            pass

def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching Google for: {query}"

def youtube_search(query):
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    return f"Searching YouTube for: {query}"

def open_website(website_name):
    url = f"https://www.{website_name}.com"
    webbrowser.open(url)
    return f"Opening {website_name}"

def get_current_time():
    time_str = datetime.datetime.now().strftime("%I:%M %p")
    result = f"Sir, the time is {time_str}"
    speak(result)
    return result

def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}&units=metric"
    try:
        response = requests.get(complete_url)
        data = response.json()
        if data.get("cod") != "404" and data.get("cod") == 200:
            main = data["main"]
            temperature = main["temp"]
            humidity = main["humidity"]
            weather_desc = data["weather"][0]["description"]
            return f"The temperature in {city} is {temperature} degrees Celsius with {weather_desc}. Humidity is at {humidity}%."
        else:
            return f"Sorry, I could not find the city {city}."
    except Exception as e:
        return f"Could not retrieve weather data at this time. Error: {str(e)}"

def Get_news(api_key, country_code="us"):
    base_url = "https://newsapi.org/v2/top-headlines?"
    complete_url = f"{base_url}country={country_code}&apiKey={api_key}"
    try:
        response = requests.get(complete_url)
        news_data = response.json()
        if news_data.get("status") == "ok":
            articles = news_data.get("articles", [])
            return [{"title": article["title"]} for article in articles[:5]]
        else:
            return "Sorry, I couldn't fetch the news right now."
    except Exception as e:
        return f"Error fetching news: {str(e)}"

def get_location(location_query):
    url = f"https://www.google.com/maps/place/{location_query}"
    webbrowser.open(url)
    return f"Here is the location of {location_query} on Google Maps."

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return f"According to Wikipedia: {result}"
    except wikipedia.exceptions.DisambiguationError:
        return "There are multiple results for that query. Can you be more specific?"
    except wikipedia.exceptions.PageError:
        return "I could not find any matching page on Wikipedia."
    except Exception as e:
        return f"An error occurred while searching Wikipedia: {str(e)}"

def email_task():
    return "Email task initiated. (Functionality is currently in placeholder mode)"

def calculate_math_expression(expression):
    try:
        expression = expression.replace('x', '*').replace('X', '*')
        allowed_chars = "0123456789+-*/.() "
        if not all(c in allowed_chars for c in expression):
            return "Invalid math expression."
        result = eval(expression)
        return str(result)
    except Exception:
        return "Sorry, I could not calculate that."
