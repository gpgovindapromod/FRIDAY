"""
Enhanced Features for FRIDAY Voice Assistant
Clean version with proper error handling
"""

import random
import os
import sqlite3
import hashlib
import requests
import json
from datetime import datetime, timedelta
import platform
import socket

# Optional imports with error handling
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not available. System monitoring features will be limited.")

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False
    print("Warning: qrcode not available. QR code generation will be disabled.")

try:
    import pyshorteners
    SHORTENER_AVAILABLE = True
except ImportError:
    SHORTENER_AVAILABLE = False
    print("Warning: pyshorteners not available. URL shortening will be disabled.")

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("Warning: yfinance not available. Stock features will be disabled.")

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("Warning: pyautogui not available. Screenshot features will be disabled.")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("Warning: textblob not available. Advanced text analysis will be disabled.")

try:
    import geocoder
    GEOCODER_AVAILABLE = True
except ImportError:
    GEOCODER_AVAILABLE = False
    print("Warning: geocoder not available. Advanced location features will be disabled.")


class AdvancedFeatures:
    """Enhanced features for FRIDAY assistant"""
    
    def __init__(self):
        self.db_path = "friday_data.db"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for storing user data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                              name TEXT NOT NULL, 
                              phone TEXT, 
                              email TEXT,
                              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS notes
                             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                              title TEXT NOT NULL, 
                              content TEXT NOT NULL, 
                              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                              task TEXT NOT NULL, 
                              priority INTEGER DEFAULT 1,
                              due_date TEXT, 
                              completed INTEGER DEFAULT 0,
                              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            conn.commit()
            conn.close()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {e}")

    # ==================== ENTERTAINMENT FEATURES ====================
    
    def play_spotify_music(self, song_name):
        """Play music on Spotify web player"""
        try:
            import webbrowser
            spotify_url = f"https://open.spotify.com/search/{song_name.replace(' ', '%20')}"
            webbrowser.open(spotify_url)
            return f"Opening Spotify to search for: {song_name}"
        except Exception as e:
            return f"Error opening Spotify: {str(e)}"

    def get_movie_info(self, movie_name):
        """Get movie information from OMDB API"""
        try:
            # Using a demo API key - replace with your own
            api_key = "trilogy"  # This is a demo key, get your own from omdbapi.com
            url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('Response') == 'True':
                info = f"🎬 Movie: {data['Title']} ({data['Year']})\n"
                info += f"⭐ Rating: {data.get('imdbRating', 'N/A')}/10\n"
                info += f"🎭 Genre: {data.get('Genre', 'N/A')}\n"
                info += f"📖 Plot: {data.get('Plot', 'N/A')}"
                return info
            else:
                return f"Movie '{movie_name}' not found. Please check the spelling."
        except Exception as e:
            return f"Error getting movie info: {str(e)}"

    def generate_qr_code(self, text, filename="qr_code.png"):
        """Generate QR code for text"""
        if not QRCODE_AVAILABLE:
            return "QR code generation not available. Install: pip install qrcode[pil]"
        
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(text)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            return f"✅ QR code generated and saved as {filename}"
        except Exception as e:
            return f"Error generating QR code: {str(e)}"

    # ==================== INTERNET & NETWORK FEATURES ====================
    
    def shorten_url(self, long_url):
        """Shorten URL using TinyURL"""
        if not SHORTENER_AVAILABLE:
            return "URL shortening not available. Install: pip install pyshorteners"
        
        try:
            s = pyshorteners.Shortener()
            short_url = s.tinyurl.short(long_url)
            return f"🔗 Shortened URL: {short_url}"
        except Exception as e:
            return f"Error shortening URL: {str(e)}"

    def get_my_ip(self):
        """Get current IP address and location"""
        try:
            # Get public IP
            ip_response = requests.get('https://api.ipify.org?format=json', timeout=5)
            public_ip = ip_response.json()['ip']
            
            # Get basic location info
            if GEOCODER_AVAILABLE:
                g = geocoder.ip('me')
                info = f"🌐 Your IP: {public_ip}\n"
                info += f"📍 Location: {g.city}, {g.country}\n"
                info += f"🗺️ Coordinates: {g.latlng}"
            else:
                info = f"🌐 Your IP: {public_ip}\n"
                info += "Install geocoder for location info: pip install geocoder"
            
            return info
        except Exception as e:
            return f"Error getting IP info: {str(e)}"

    # ==================== FINANCIAL FEATURES ====================
    
    def get_stock_price(self, symbol):
        """Get current stock price"""
        if not YFINANCE_AVAILABLE:
            return "Stock features not available. Install: pip install yfinance"
        
        try:
            ticker = yf.Ticker(symbol.upper())
            data = ticker.history(period="1d")
            
            if not data.empty:
                current_price = data['Close'].iloc[-1]
                open_price = data['Open'].iloc[-1]
                high_price = data['High'].iloc[-1]
                low_price = data['Low'].iloc[-1]
                
                info = f"📈 {symbol.upper()} Stock Information:\n"
                info += f"Current: ${current_price:.2f}\n"
                info += f"Open: ${open_price:.2f}\n"
                info += f"High: ${high_price:.2f}\n"
                info += f"Low: ${low_price:.2f}"
                return info
            else:
                return f"Stock symbol '{symbol}' not found or no recent data available"
        except Exception as e:
            return f"Error getting stock price: {str(e)}"

    def get_crypto_price(self, crypto):
        """Get cryptocurrency price"""
        try:
            # Convert common names to IDs
            crypto_map = {
                'btc': 'bitcoin',
                'eth': 'ethereum',
                'bitcoin': 'bitcoin',
                'ethereum': 'ethereum',
                'dogecoin': 'dogecoin',
                'doge': 'dogecoin',
                'xrp': 'ripple',
                'ripple': 'ripple'
            }
            
            crypto_id = crypto_map.get(crypto.lower(), crypto.lower())
            
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if crypto_id in data:
                price = data[crypto_id]['usd']
                return f"💰 {crypto_id.capitalize()} price: ${price:,.2f} USD"
            else:
                return f"Cryptocurrency '{crypto}' not found. Try: bitcoin, ethereum, dogecoin, xrp"
        except Exception as e:
            return f"Error getting crypto price: {str(e)}"

    def currency_converter(self, amount, from_currency, to_currency):
        """Convert currency"""
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if to_currency.upper() in data['rates']:
                rate = data['rates'][to_currency.upper()]
                converted = amount * rate
                return f"💱 {amount} {from_currency.upper()} = {converted:.2f} {to_currency.upper()}"
            else:
                return f"Currency '{to_currency}' not supported"
        except Exception as e:
            return f"Error converting currency: {str(e)}"

    # ==================== SYSTEM MONITORING FEATURES ====================
    
    def get_system_info(self):
        """Get detailed system information"""
        try:
            info = f"🖥️ System Information:\n"
            info += f"OS: {platform.system()} {platform.release()}\n"
            info += f"Version: {platform.version()}\n"
            info += f"Machine: {platform.machine()}\n"
            info += f"Processor: {platform.processor()}\n"
            info += f"Computer Name: {platform.node()}\n"
            
            if PSUTIL_AVAILABLE:
                # Memory info
                memory = psutil.virtual_memory()
                info += f"\n💾 Memory:\n"
                info += f"Total: {memory.total // (1024**3)} GB\n"
                info += f"Available: {memory.available // (1024**3)} GB\n"
                info += f"Used: {memory.percent}%\n"
                
                # Disk info
                disk = psutil.disk_usage('/')
                info += f"\n💿 Disk:\n"
                info += f"Total: {disk.total // (1024**3)} GB\n"
                info += f"Free: {disk.free // (1024**3)} GB\n"
                info += f"Used: {disk.percent}%\n"
                
                # CPU info
                info += f"\n⚡ CPU Usage: {psutil.cpu_percent(interval=1)}%"
            else:
                info += "\nInstall psutil for detailed memory/disk/CPU info: pip install psutil"
            
            return info
        except Exception as e:
            return f"Error getting system info: {str(e)}"

    def get_running_processes(self):
        """Get list of running processes"""
        if not PSUTIL_AVAILABLE:
            return "Process monitoring not available. Install: pip install psutil"
        
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)
            
            result = "🔄 Top 10 processes by CPU usage:\n\n"
            for i, proc in enumerate(processes[:10], 1):
                result += f"{i}. {proc['name']} - PID: {proc['pid']} - CPU: {proc.get('cpu_percent', 0)}%\n"
            
            return result
        except Exception as e:
            return f"Error getting processes: {str(e)}"

    # ==================== PRODUCTIVITY FEATURES ====================
    
    def save_note(self, title, content):
        """Save a note to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
            conn.commit()
            conn.close()
            return f"✅ Note '{title}' saved successfully"
        except Exception as e:
            return f"Error saving note: {str(e)}"

    def get_notes(self):
        """Get all saved notes"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT title, content, created_at FROM notes ORDER BY created_at DESC LIMIT 10")
            notes = cursor.fetchall()
            conn.close()
            
            if notes:
                result = "📝 Your saved notes:\n\n"
                for i, (title, content, created_at) in enumerate(notes, 1):
                    result += f"{i}. {title}\n"
                    result += f"   {content[:100]}{'...' if len(content) > 100 else ''}\n"
                    result += f"   Created: {created_at}\n\n"
                return result
            else:
                return "No notes found. Say 'save note [content]' to create one!"
        except Exception as e:
            return f"Error retrieving notes: {str(e)}"

    def add_contact(self, name, phone="", email=""):
        """Add contact to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", 
                         (name, phone, email))
            conn.commit()
            conn.close()
            return f"✅ Contact '{name}' added successfully"
        except Exception as e:
            return f"Error adding contact: {str(e)}"

    def find_contact(self, name):
        """Find contact by name"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name, phone, email FROM contacts WHERE name LIKE ?", (f"%{name}%",))
            contacts = cursor.fetchall()
            conn.close()
            
            if contacts:
                result = f"👤 Found {len(contacts)} contact(s):\n\n"
                for i, (contact_name, phone, email) in enumerate(contacts, 1):
                    result += f"{i}. {contact_name}\n"
                    if phone:
                        result += f"   📱 Phone: {phone}\n"
                    if email:
                        result += f"   📧 Email: {email}\n"
                    result += "\n"
                return result
            else:
                return f"No contact found for '{name}'"
        except Exception as e:
            return f"Error finding contact: {str(e)}"

    def add_task(self, task, priority=1, due_date=""):
        """Add task to to-do list"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task, priority, due_date) VALUES (?, ?, ?)", 
                         (task, priority, due_date))
            conn.commit()
            conn.close()
            return f"✅ Task added: {task}"
        except Exception as e:
            return f"Error adding task: {str(e)}"

    def get_tasks(self):
        """Get all tasks"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT task, priority, due_date FROM tasks WHERE completed = 0 ORDER BY priority DESC, created_at LIMIT 10")
            tasks = cursor.fetchall()
            conn.close()
            
            if tasks:
                result = "✅ Your pending tasks:\n\n"
                for i, (task, priority, due_date) in enumerate(tasks, 1):
                    priority_icon = "🔴" if priority >= 3 else "🟡" if priority == 2 else "🟢"
                    result += f"{i}. {priority_icon} {task}\n"
                    if due_date:
                        result += f"   Due: {due_date}\n"
                    result += "\n"
                return result
            else:
                return "No pending tasks. Say 'add task [task name]' to create one!"
        except Exception as e:
            return f"Error getting tasks: {str(e)}"

    # ==================== SECURITY FEATURES ====================
    
    def generate_password(self, length=12):
        """Generate secure password"""
        try:
            import string
            characters = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(random.choice(characters) for _ in range(length))
            return f"🔐 Generated password ({length} characters):\n{password}\n\n⚠️ Store this securely!"
        except Exception as e:
            return f"Error generating password: {str(e)}"

    def hash_text(self, text):
        """Generate hash of text"""
        try:
            sha256_hash = hashlib.sha256(text.encode()).hexdigest()
            md5_hash = hashlib.md5(text.encode()).hexdigest()
            
            result = "🔒 Text Hashes:\n\n"
            result += f"SHA-256:\n{sha256_hash}\n\n"
            result += f"MD5:\n{md5_hash}"
            return result
        except Exception as e:
            return f"Error hashing text: {str(e)}"

    # ==================== IMAGE & MEDIA FEATURES ====================
    
    def take_screenshot(self, filename="screenshot.png"):
        """Take screenshot"""
        if not PYAUTOGUI_AVAILABLE:
            return "Screenshot feature not available. Install: pip install pyautogui pillow"
        
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            return f"📸 Screenshot saved as {filename}"
        except Exception as e:
            return f"Error taking screenshot: {str(e)}"

    # ==================== FUN & GAMES FEATURES ====================
    
    def roll_dice(self, sides=6, count=1):
        """Roll dice"""
        try:
            results = [random.randint(1, sides) for _ in range(count)]
            result_str = "🎲 Dice Roll Results:\n\n"
            result_str += f"Rolled {count} {sides}-sided dice\n"
            result_str += f"Results: {results}\n"
            result_str += f"Total: {sum(results)}"
            return result_str
        except Exception as e:
            return f"Error rolling dice: {str(e)}"

    def flip_coin(self):
        """Flip a coin"""
        try:
            result = random.choice(["Heads", "Tails"])
            coin_emoji = "🪙" 
            return f"{coin_emoji} Coin flip result: {result}!"
        except Exception as e:
            return f"Error flipping coin: {str(e)}"

    def random_number(self, min_val=1, max_val=100):
        """Generate random number"""
        try:
            number = random.randint(min_val, max_val)
            return f"🎰 Random number between {min_val} and {max_val}: {number}"
        except Exception as e:
            return f"Error generating random number: {str(e)}"

    # ==================== TEXT ANALYSIS FEATURES ====================
    
    def text_sentiment_detailed(self, text):
        """Detailed sentiment analysis"""
        if not TEXTBLOB_AVAILABLE:
            return "Sentiment analysis not available. Install: pip install textblob"
        
        try:
            blob = TextBlob(text)
            sentiment = blob.sentiment
            
            # Determine sentiment category
            if sentiment.polarity > 0.3:
                category = "Very Positive 😊"
            elif sentiment.polarity > 0.1:
                category = "Positive 🙂"
            elif sentiment.polarity > -0.1:
                category = "Neutral 😐"
            elif sentiment.polarity > -0.3:
                category = "Negative ☹️"
            else:
                category = "Very Negative 😢"
            
            result = f"📊 Text Sentiment Analysis:\n\n"
            result += f"Category: {category}\n"
            result += f"Polarity: {sentiment.polarity:.2f} (Range: -1 to 1)\n"
            result += f"Subjectivity: {sentiment.subjectivity:.2f} (0=Objective, 1=Subjective)"
            
            return result
        except Exception as e:
            return f"Error analyzing sentiment: {str(e)}"

    def get_file_info(self, file_path):
        """Get detailed file information"""
        try:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                size = stat.st_size
                modified = datetime.fromtimestamp(stat.st_mtime)
                created = datetime.fromtimestamp(stat.st_ctime)
                
                info = f"📄 File Information:\n\n"
                info += f"Path: {file_path}\n"
                info += f"Size: {size:,} bytes ({size/1024/1024:.2f} MB)\n"
                info += f"Modified: {modified}\n"
                info += f"Created: {created}"
                return info
            else:
                return f"❌ File '{file_path}' does not exist"
        except Exception as e:
            return f"Error getting file info: {str(e)}"


# Create global instance
advanced_features = AdvancedFeatures()

# Export
__all__ = ['advanced_features', 'AdvancedFeatures']