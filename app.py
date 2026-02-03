"""
GDM Chatbot MVP - Main Application
CS 584 Case Study - Spring 2026

A minimal working prototype demonstrating:
- Patient authentication
- Glucose tracking
- AI-powered chat with Kerala-specific diet knowledge
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['DATABASE'] = 'database/gdm_chatbot.db'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import models and chatbot
from lib.models import User, init_db
# from lib.chatbot import ChatbotRAG # TODO: Change from lib.chatbot for fake question-answering --> lib.chatbot_rag_real for real RAG with LLM + FAISS.
from lib.chatbot_rag_real import ChatbotRAG 

# Initialize database on startup
with app.app_context():
    init_db()

# Lazy load chatbot to avoid startup delay
_chatbot_instance = None

def get_chatbot():
    """Get or create chatbot instance"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = ChatbotRAG()
    return _chatbot_instance


# ==================== DATABASE HELPERS ====================

def get_db():
    """Get database connection"""
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    conn = get_db()
    user_data = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user_data:
        return User(user_data['id'], user_data['email'], user_data['name'], 
                   user_data['language_preference'])
    return None


# ==================== AUTHENTICATION ====================

@app.route('/')
def index():
    """Landing page - redirect based on auth status"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        conn = get_db()
        user_data = conn.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data['id'], user_data['email'], user_data['name'],
                       user_data['language_preference'])
            login_user(user)
            
            # Update last login
            conn.execute('UPDATE users SET last_login = ? WHERE id = ?',
                        (datetime.now(), user_data['id']))
            conn.commit()
            
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        phone = request.form.get('phone', '').strip()
        language = request.form.get('language', 'ml')
        
        # Patient-specific data
        due_date = request.form.get('due_date')
        gestational_weeks = int(request.form.get('gestational_weeks', 20))
        kerala_region = request.form.get('kerala_region', 'Ernakulam')
        
        # Validation
        if not all([name, email, password, due_date]):
            flash('Please fill in all required fields.', 'error')
            return render_template('register.html')
        
        conn = get_db()
        
        # Check if email exists
        existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            flash('This email is already registered.', 'error')
            return render_template('register.html')
        
        # Create user account
        password_hash = generate_password_hash(password)
        cursor = conn.execute(
            'INSERT INTO users (email, password_hash, name, phone, language_preference) VALUES (?, ?, ?, ?, ?)',
            (email, password_hash, name, phone, language)
        )
        user_id = cursor.lastrowid
        
        # Create patient profile
        conn.execute(
            '''INSERT INTO patients (user_id, due_date, gestational_age_weeks, kerala_region,
                                    diagnosis_date, target_fasting_glucose, target_postmeal_glucose)
               VALUES (?, ?, ?, ?, ?, 95.0, 120.0)''',
            (user_id, due_date, gestational_weeks, kerala_region, datetime.now().date())
        )
        conn.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))


# ==================== DASHBOARD ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Patient dashboard - main hub"""
    conn = get_db()
    
    # Get patient information
    patient = conn.execute(
        '''SELECT p.*, u.language_preference
           FROM patients p
           JOIN users u ON p.user_id = u.id
           WHERE u.id = ?''',
        (current_user.id,)
    ).fetchone()
    
    # Get recent glucose readings (last 5)
    readings = conn.execute(
        '''SELECT * FROM glucose_readings
           WHERE patient_id = ?
           ORDER BY timestamp DESC
           LIMIT 5''',
        (patient['id'],)
    ).fetchall()
    
    # Calculate today's statistics
    today_stats = conn.execute(
        '''SELECT COUNT(*) as count, AVG(reading_value) as avg
           FROM glucose_readings
           WHERE patient_id = ? AND DATE(timestamp) = DATE('now')''',
        (patient['id'],)
    ).fetchone()
    
    # Calculate 7-day average
    week_avg = conn.execute(
        '''SELECT AVG(reading_value) as avg FROM glucose_readings
           WHERE patient_id = ? AND DATE(timestamp) >= DATE('now', '-7 days')''',
        (patient['id'],)
    ).fetchone()
    
    return render_template('dashboard.html',
                         patient=patient,
                         readings=readings,
                         today_count=today_stats['count'] or 0,
                         today_avg=round(today_stats['avg'] or 0, 1),
                         week_avg=round(week_avg['avg'] or 0, 1))


# ==================== GLUCOSE TRACKING ====================

@app.route('/log-glucose', methods=['GET', 'POST'])
@login_required
def log_glucose():
    """Log a new glucose reading"""
    if request.method == 'POST':
        conn = get_db()
        
        # Get patient targets
        patient = conn.execute(
            'SELECT id, target_fasting_glucose, target_postmeal_glucose FROM patients WHERE user_id = ?',
            (current_user.id,)
        ).fetchone()
        
        # Get form data
        reading_value = float(request.form.get('reading_value'))
        reading_type = request.form.get('reading_type')
        meal_context = request.form.get('meal_context', '').strip()
        notes = request.form.get('notes', '').strip()
        
        # Determine if reading is flagged
        flagged_low = reading_value < 70.0
        
        if reading_type == 'fasting':
            flagged_high = reading_value > patient['target_fasting_glucose']
        else:
            flagged_high = reading_value > patient['target_postmeal_glucose']
        
        # Save to database
        conn.execute(
            '''INSERT INTO glucose_readings (patient_id, reading_value, reading_type,
                                            meal_context, notes, flagged_high, flagged_low)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (patient['id'], reading_value, reading_type, meal_context, notes,
             flagged_high, flagged_low)
        )
        conn.commit()
        
        # Flash appropriate message
        if flagged_high:
            flash('Reading logged. Note: This reading is above your target range.', 'warning')
        elif flagged_low:
            flash('Reading logged. Warning: Low reading detected. Contact your provider if you feel unwell.', 'warning')
        else:
            flash('Glucose reading logged successfully!', 'success')
        
        return redirect(url_for('dashboard'))
    
    return render_template('log_glucose.html')


@app.route('/glucose-history')
@login_required
def glucose_history():
    """View complete glucose reading history"""
    conn = get_db()
    
    patient = conn.execute(
        'SELECT id FROM patients WHERE user_id = ?', (current_user.id,)
    ).fetchone()
    
    # Get all readings (limit to recent 50 for performance)
    readings = conn.execute(
        '''SELECT * FROM glucose_readings
           WHERE patient_id = ?
           ORDER BY timestamp DESC
           LIMIT 50''',
        (patient['id'],)
    ).fetchall()
    
    return render_template('glucose_history.html', readings=readings)


# ==================== CHAT INTERFACE ====================

@app.route('/chat')
@login_required
def chat():
    """Chat interface with AI assistant"""
    conn = get_db()
    
    patient = conn.execute(
        'SELECT id FROM patients WHERE user_id = ?', (current_user.id,)
    ).fetchone()
    
    # Get conversation history
    messages = conn.execute(
        '''SELECT message_text, is_from_bot, timestamp
           FROM chat_messages
           WHERE patient_id = ?
           ORDER BY timestamp ASC''',
        (patient['id'],)
    ).fetchall()
    
    return render_template('chat.html', messages=messages)


@app.route('/chat/send', methods=['POST'])
@login_required
def send_message():
    """Process chat message and generate AI response"""
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    conn = get_db()
    patient = conn.execute(
        'SELECT id, kerala_region FROM patients WHERE user_id = ?', (current_user.id,)
    ).fetchone()
    
    # Save user message
    conn.execute(
        '''INSERT INTO chat_messages (patient_id, message_text, is_from_bot, language)
           VALUES (?, ?, 0, ?)''',
        (patient['id'], user_message, current_user.language_preference)
    )
    
    # Generate AI response
    chatbot = get_chatbot()
    bot_response = chatbot.get_response(
        user_message,
        language=current_user.language_preference,
        region=patient['kerala_region']
    )
    
    # Save bot response
    conn.execute(
        '''INSERT INTO chat_messages (patient_id, message_text, is_from_bot, language)
           VALUES (?, ?, 1, ?)''',
        (patient['id'], bot_response, current_user.language_preference)
    )
    conn.commit()
    
    return jsonify({
        'user_message': user_message,
        'bot_response': bot_response,
        'timestamp': datetime.now().strftime('%I:%M %p')
    })


if __name__ == '__main__':
    # Run app (debug mode for development)
    app.run(debug=True, host='0.0.0.0', port=5001) # Try 5000, 5001 or 8000 if one is in use