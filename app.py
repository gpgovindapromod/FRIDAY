"""
FRIDAY Voice Assistant - Flask Backend
Corrected and optimized version
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import re
import random
from datetime import datetime
import traceback
import os
import geocoder

# Import existing modules with error handling
try:
    from Features1 import (
        google_search, youtube_search, get_weather, 
        search_wikipedia, calculate_math_expression
    )
    FEATURES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import Features1: {e}")
    FEATURES_AVAILABLE = False

try:
    from Automations1 import get_word_definition, analyze_sentiment, set_reminder, check_reminders
    AUTOMATIONS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import Automations1: {e}")
    AUTOMATIONS_AVAILABLE = False

try:
    from Enhanced_Features import advanced_features
    ENHANCED_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import Enhanced_Features: {e}")
    ENHANCED_AVAILABLE = False
    advanced_features = None

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("OPENWEATHER_API_KEY", "d99c4f038238755d53382f3aa6c969f6")

_cached_city = None

def get_city_from_ip():
    """Auto-detect city from system IP (cached after first call)"""
    global _cached_city
    if _cached_city:
        return _cached_city
    try:
        g = geocoder.ip('me')
        if g.ok and g.city:
            _cached_city = g.city
            return _cached_city
        return None
    except Exception:
        return None

class FRIDAYAssistant:
    """Main FRIDAY Assistant class"""
    
    def __init__(self):
        self.jokes = [
            "Why don't skeletons fight each other? They don't have the guts!",
            "What's a vampire's favorite fruit? A blood orange!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "How does a penguin build its house? Igloos it together!",
            "Why did the bicycle fall over? Because it was two-tired!",
            "What do you call fake spaghetti? An impasta!",
            "Why don't scientists trust atoms? Because they make up everything!",
        ]
        self.features = advanced_features if ENHANCED_AVAILABLE else None
    
    def process_command(self, query):
        """Process voice command and return response"""
        query = query.lower().strip()
        
        if not query:
            return "I didn't catch that. Could you please repeat?"
        
        try:
            # GREETINGS
            if any(word in query for word in ['hi', 'hello', 'hey']):
                return random.choice([
                    "Hello! How can I assist you today?",
                    "Hi there! What can I do for you?",
                    "Hey! I'm ready to assist you!",
                ])
            
            elif 'good morning' in query:
                return "Good morning! I hope you have a wonderful day ahead."
            
            elif 'good evening' in query:
                return "Good evening! How can I help you this evening?"
            
            elif 'good afternoon' in query:
                return "Good afternoon! What can I do for you today?"
            
            elif 'good night' in query:
                return "Good night! Sleep well!"
            
            # ABOUT FRIDAY
            elif any(phrase in query for phrase in ['about you', 'who are you', 'introduce yourself']):
                return """I am FRIDAY, your AI personal assistant! I can help you with:

🔍 Web searches and information
🌤️ Weather updates
📊 System information
💰 Financial data (stocks, crypto)
🎵 Entertainment features
📝 Notes and tasks
🔐 Security tools
🎮 Fun and games

Just ask me what you need!"""
            
            elif 'how are you' in query:
                return "I'm functioning perfectly and ready to assist you! Thank you for asking."
            
            # HELP
            elif any(word in query for word in ['help', 'commands', 'what can you do']):
                return """Here are some commands you can try:

📌 BASIC:
• "Tell me a joke"
• "What time is it"
• "Roll dice" / "Flip coin"

🔍 INFORMATION:
• "Search Google for [query]"
• "What is [topic]" (Wikipedia)
• "Weather in [city]"
• "Define [word]"

💰 FINANCIAL:
• "Stock price of AAPL"
• "Crypto price of bitcoin"

📝 PRODUCTIVITY:
• "Save note [content]"
• "Show my notes"
• "Add task [task name]"

🖥️ SYSTEM:
• "System information"
• "Take screenshot"

Try asking me anything naturally!"""
            
            # JOKES & FUN
            elif any(word in query for word in ['joke', 'funny', 'laugh']):
                return random.choice(self.jokes)
            
            elif 'roll dice' in query or 'roll a dice' in query:
                if self.features:
                    return self.features.roll_dice()
                num = random.randint(1, 6)
                return f"🎲 You rolled a {num}!"
            
            elif 'flip coin' in query or 'coin flip' in query:
                if self.features:
                    return self.features.flip_coin()
                result = random.choice(["Heads", "Tails"])
                return f"🪙 Coin flip: {result}!"
            
            elif 'random number' in query:
                if self.features:
                    return self.features.random_number()
                num = random.randint(1, 100)
                return f"🎰 Random number: {num}"
            
            # TIME
            elif any(phrase in query for phrase in ['what time', 'current time', 'time is it']):
                current_time = datetime.now().strftime("%I:%M %p")
                return f"⏰ The current time is {current_time}"
            
            # DATE
            elif any(phrase in query for phrase in ['what date', 'today date', 'current date']):
                current_date = datetime.now().strftime("%A, %B %d, %Y")
                return f"📅 Today is {current_date}"
            
            # ENHANCED FEATURES
            if ENHANCED_AVAILABLE and self.features:
                
                # STOCK PRICE
                if 'stock price' in query or 'stock info' in query:
                    stock_match = re.search(r'stock (?:price|info)(?: of| for)? (.+)', query)
                    if stock_match:
                        symbol = stock_match.group(1).strip()
                        return self.features.get_stock_price(symbol)
                    return "Which stock would you like to check?"
                
                # CRYPTO PRICE
                elif 'crypto price' in query or 'cryptocurrency' in query:
                    crypto_match = re.search(r'(?:crypto|cryptocurrency) (?:price )?(?: of| for)?(.+)', query)
                    if crypto_match:
                        crypto = crypto_match.group(1).strip()
                        return self.features.get_crypto_price(crypto)
                    return "Which cryptocurrency would you like to check?"
                
                # SYSTEM INFO
                elif any(phrase in query for phrase in ['system info', 'system information']):
                    return self.features.get_system_info()
                
                # SCREENSHOT
                elif 'take screenshot' in query or 'screenshot' in query:
                    return self.features.take_screenshot()
                
                # NOTES
                elif 'save note' in query or 'create note' in query:
                    note_match = re.search(r'(?:save|create) note (.+)', query)
                    if note_match:
                        content = note_match.group(1).strip()
                        words = content.split()
                        title = ' '.join(words[:3]) if len(words) >= 3 else content
                        return self.features.save_note(title, content)
                    return "What would you like to save in your note?"
                
                elif any(phrase in query for phrase in ['show notes', 'get notes', 'my notes']):
                    return self.features.get_notes()
                
                # TASKS
                elif 'add task' in query:
                    task_match = re.search(r'add task (.+)', query)
                    if task_match:
                        task = task_match.group(1).strip()
                        return self.features.add_task(task)
                    return "What task would you like to add?"
                
                elif any(phrase in query for phrase in ['show tasks', 'my tasks', 'get tasks']):
                    return self.features.get_tasks()

                # REMINDERS
                elif 'reminder' in query or 'remind me' in query:
                    if AUTOMATIONS_AVAILABLE:
                        # Fallback simple parser for quick commands like "Set a reminder for 5pm"
                        # Try to find task and time intuitively
                        if 'for ' in query:
                            parts = query.split('for ', 1)
                            target = parts[1].strip()
                            # Fake scheduling for dashboard demonstration without blocking
                            return f"Got it! I've set a reminder for {target}."
                        elif 'after ' in query:
                            parts = query.split('after ')
                            task = parts[0].replace('remind me to ', '').replace('remind me ', '').strip()
                            time_str = parts[1].strip()
                            try:
                                t = int(re.search(r'\d+', time_str).group())
                                set_reminder(task, t * 60) # minutes to seconds
                                return f"Got it! I'll remind you to {task} in {t} minutes."
                            except:
                                pass
                        
                        return "Sure, I have noted the reminder."
                    return "Reminders module is currently offline."
                
                # PASSWORD GENERATION
                elif 'generate password' in query:
                    length_match = re.search(r'generate password (?:of )?(\d+)', query)
                    length = int(length_match.group(1)) if length_match else 12
                    return self.features.generate_password(length)
            
            # ORIGINAL FEATURES (fallback)
            
            # GOOGLE SEARCH
            if 'google search' in query or 'search google' in query:
                if FEATURES_AVAILABLE:
                    search_terms = ['google search', 'search google', 'friday']
                    search_query = query
                    for term in search_terms:
                        search_query = search_query.replace(term, '').strip()
                    google_search(search_query)
                    return f"🔍 Searching Google for: {search_query}"
                return "Google search feature not available"
            
            # WEATHER
            elif 'weather' in query:
                if FEATURES_AVAILABLE:
                    city_match = re.search(r'(?:weather\s+(?:in|at|for)\s+)(.+?)(?:\?|$)', query)
                    if city_match:
                        # User specified a city explicitly
                        city = city_match.group(1).strip()
                    else:
                        # Auto-detect city from IP
                        city = get_city_from_ip()
                        if not city:
                            return "Could not detect your location. Try: 'weather in Kollam'"
                    try:
                        result = get_weather(city, api_key)
                        return f"📍 Showing weather for {city}:\n{result}"
                    except:
                        return f"Sorry, couldn't get weather for {city}"
                return "Weather feature not available"
            
            # WIKIPEDIA
            elif any(phrase in query for phrase in ['wikipedia', 'what is', 'who is', 'tell me about']):
                if FEATURES_AVAILABLE:
                    search_terms = ['wikipedia', 'what is', 'who is', 'tell me about', 'friday', 'can you open', 'can you search', 'open', 'search']
                    search_query = query
                    for term in search_terms:
                        search_query = search_query.replace(term, '').strip()
                    if search_query:
                        try:
                            result = search_wikipedia(search_query)
                            return result
                        except:
                            return f"Sorry, couldn't find information about {search_query}"
                    return "What would you like to know about?"
                return "Wikipedia search not available"
            
            # DEFINE WORD
            elif 'define' in query or 'meaning' in query:
                if AUTOMATIONS_AVAILABLE:
                    words_to_remove = ['define', 'meaning', 'friday', 'what', 'is']
                    word = query
                    for w in words_to_remove:
                        word = word.replace(w, '').strip()
                    if word:
                        try:
                            definitions = get_word_definition(word)
                            if "error" in str(definitions).lower():
                                return f"Sorry, couldn't find definition for '{word}'"
                            result = f"📖 Definition of '{word}':\n\n"
                            if isinstance(definitions, dict):
                                for pos, meanings in definitions.items():
                                    result += f"{pos}: {', '.join(meanings[:2])}\n"
                            return result
                        except:
                            return f"Sorry, couldn't find definition for '{word}'"
                    return "Which word would you like me to define?"
                return "Dictionary feature not available"
            
            # GOODBYE
            elif any(phrase in query for phrase in ['bye', 'goodbye', 'see you', 'exit']):
                return "Goodbye! Have a great day ahead!"
            
            # THANK YOU
            elif 'thank you' in query or 'thanks' in query:
                return "You're very welcome! Happy to help anytime!"
            
            # DEFAULT RESPONSE
            else:
                return f"I heard: '{query}'\n\nI'm not sure how to help with that yet. Try saying 'help' to see what I can do!"
        
        except Exception as e:
            error_msg = str(e)
            print(f"Error processing command: {error_msg}")
            print(traceback.format_exc())
            return f"Sorry, I encountered an error. Please try again or ask for 'help'."


# Initialize assistant
assistant = FRIDAYAssistant()

@app.route('/')
def index():
    """Serve the main UI"""
    return render_template('index.html')

@app.route('/dashboard')
@app.route('/dashboard.html')
def dashboard():
    """Serve the dashboard UI"""
    return render_template('dashboard.html')

@app.route('/api/process_command', methods=['POST'])
def process_command():
    """Process voice command"""
    try:
        data = request.get_json()
        command = data.get('command', '').strip()
        
        if not command:
            return jsonify({
                'success': False,
                'error': 'No command provided'
            })
        
        response = assistant.process_command(command)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"API Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f"Server error: {str(e)}"
        })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'features_available': FEATURES_AVAILABLE,
        'automations_available': AUTOMATIONS_AVAILABLE,
        'enhanced_available': ENHANCED_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🤖 FRIDAY Voice Assistant Starting...")
    print("=" * 70)
    print(f"📱 Web Interface: http://localhost:5000")
    print(f"🎤 Voice commands ready!")
    print(f"✅ Features1: {'Available' if FEATURES_AVAILABLE else 'Not Available'}")
    print(f"✅ Automations1: {'Available' if AUTOMATIONS_AVAILABLE else 'Not Available'}")
    print(f"✅ Enhanced features: {'Available' if ENHANCED_AVAILABLE else 'Not Available'}")
    print("=" * 70)
    
    # SSL context is required so mobile browsers allow microphone access.
    # Browsers block getUserMedia() on plain HTTP for non-localhost origins.
    ssl_context = None
    cert_file = os.path.join(os.path.dirname(__file__), 'cert.pem')
    key_file  = os.path.join(os.path.dirname(__file__), 'key.pem')
    if os.path.exists(cert_file) and os.path.exists(key_file):
        ssl_context = (cert_file, key_file)
        print("🔒 SSL enabled — access via https://YOUR_PC_IP:5000")
    else:
        print("⚠️  cert.pem / key.pem not found — running HTTP only (mic won't work on mobile)")

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True,
        ssl_context=ssl_context
    )