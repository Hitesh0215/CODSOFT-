from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import os
import math

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or os.urandom(24)
CORS(app)

def try_math_response(user_input):
    """Safely evaluate math expressions from user input"""
    allowed = {
        "sqrt": math.sqrt, "pow": math.pow, "abs": abs, "round": round,
        "floor": math.floor, "ceil": math.ceil, "log": math.log,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "pi": math.pi, "e": math.e
    }
    try:
        result = eval(user_input, {"__builtins__": None}, allowed)
        return f"🧮 The result is: {result}"
    except:
        return None

def get_response(user_input, user_name="You"):
    """Generate chatbot responses based on user input"""
    user_input = user_input.lower().strip()
    
    # Try math evaluation first
    math_reply = try_math_response(user_input)
    if math_reply:
        return math_reply
    
    # Greeting responses
    if any(word in user_input for word in ["hello", "hi", "hey", "greetings"]):
        return "Hey hey! Great to hear from you 😄"
    
    # How are you responses
    elif any(phrase in user_input for phrase in ["how are you", "how's it going", "what's up"]):
        return "I'm doing fantastic! Thanks for asking. How are you doing?"
    
    # Identity responses
    elif any(phrase in user_input for phrase in ["your name", "who are you", "what are you"]):
        return "I'm HitBot, your helpful AI buddy coded by Hitesh! 🤖"
    
    # Time responses
    elif any(word in user_input for word in ["time", "clock", "what time"]):
        now = datetime.now().strftime("%I:%M %p")
        return f"It's currently {now}. ⏰"
    
    # Joke responses
    elif "joke" in user_input:
        jokes = [
            "Why do Java developers wear glasses? Because they can't C#! 😂",
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡"
        ]
        import random
        return random.choice(jokes)
    
    # Emotional support
    elif any(word in user_input for word in ["sad", "tired", "bored", "stressed", "upset"]):
        return "Sounds like you need a boost. Want a joke, a fact, or a motivational quote? 🌈"
    
    # Goodbye responses
    elif any(word in user_input for word in ["bye", "exit", "quit", "goodbye", "see you"]):
        return f"Catch you later, {user_name}! You've got this. 👋"
    
    # Help responses
    elif "help" in user_input:
        return "I can chat about greetings, tell jokes, give you the time, or just have a friendly conversation! What would you like to talk about?"
    
    # Default response
    else:
        return "Hmm... That one flew over my antenna. Mind rephrasing it? 🤔"

@app.route('/')
def home():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat API requests"""
    try:
        data = request.get_json()
        if not data or 'user_input' not in data:
            return jsonify({'error': 'No user input provided'}), 400
        
        user_input = data.get('user_input', '').strip()
        if not user_input:
            return jsonify({'error': 'Empty user input'}), 400
        
        response = get_response(user_input)
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("🚀 Starting HiteBot Flask App...")
    print("📍 Running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)