# GDM Chatbot MVP

> **CS 584 Case Study - Spring 2026**  
> A minimal working prototype for GDM (Gestational Diabetes Mellitus) management in Kerala, India.

---

## What's In This MVP?

This prototype demonstrates:
1. **Patient Authentication** - Register and login
2. **Glucose Tracking** - Log readings, view history
3. **AI Chat** - Ask Kerala diet questions with RAG knowledge

**NOT in MVP:** Provider dashboards, notifications, complex visualizations, mobile apps

---

## Quick Start (Mac & Windows)

### Prerequisites
- Python 3.10 or higher
- pip (comes with Python)

### Setup (5 minutes)

**Mac:**
```bash
# Clone or download this repo
cd gdm-chatbot-mvp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

**Windows:**
```bash
# Clone or download this repo
cd gdm-chatbot-mvp

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

### Access the App
Open your browser and go to:
```
http://localhost:5000
```

---

## MVP Features Implemented

### 1. User Authentication
- Register new patients
- Login/logout
- Password hashing (secure)
- Session management

**Files:**
- `app.py` 
- Routes: `/register`, `/login`, `/logout`
- `templates/login.html`, `templates/register.html`

### 2. Patient Dashboard
- View today's glucose statistics
- See 7-day average
- Quick access to log glucose and chat

**Files:**
- `app.py` - Route: `/dashboard`
- `templates/dashboard.html`

### 3. Glucose Tracking
- Log readings (fasting, post-meal, bedtime)
- Automatic high/low flagging per ADA guidelines
- View complete history

**Files:**
- `app.py` 
- Routes: `/log-glucose`, `/glucose-history`
- `templates/log_glucose.html`, `templates/glucose_history.html`

### 4. AI Chat with Kerala Diet Knowledge
- Ask questions about Kerala foods (rice, dosa, idli, etc.)
- Get carb counts and diet guidance
- Malayalam language support
- Real-time responses

**Files:**
- `app.py` 
- Routes: `/chat`, `/chat/send`
- `lib/chatbot.py` - RAG logic (simplified for MVP)
- `templates/chat.html`

---

## Project Structure

```
gdm-chatbot-mvp/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
│
├── lib/
│   ├── models.py          # Database models & initialization
│   └── chatbot.py         # RAG chatbot (MVP version)
│
├── database/
│   └── gdm_chatbot.db     # SQLite database (created on first run)
│
├── templates/             # HTML pages
│   ├── base.html         # Base template
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── chat.html
│   ├── log_glucose.html
│   └── glucose_history.html
│
├── static/
│   ├── css/
│   │   └── style.css     # Professional styling
│   └── js/
│       └── main.js       # Minimal JavaScript
│
└── docs/                 # Documentation
    └── KANBAN_CARDS.md
```

---

## Database Schema

### Tables Created
1. **users** - Authentication (email, password_hash, name, language_preference)
2. **patients** - GDM data (due_date, gestational_weeks, targets)
3. **glucose_readings** - Tracking (value, type, timestamp, flags)
4. **chat_messages** - Conversation history

### View Database (Optional)
```bash
# Mac/Linux
sqlite3 database/gdm_chatbot.db

# Windows
# Download SQLite browser or use Python
python
>>> import sqlite3
>>> conn = sqlite3.connect('database/gdm_chatbot.db')
>>> conn.execute('SELECT * FROM users').fetchall()
```

---

## How the Chat Works (RAG Simplified)

**In Production:** Would use Llama 3.2 1B + FAISS vector search

**In MVP:** Uses rule-based matching with Kerala food knowledge

```python
# lib/chatbot.py
knowledge_base = {
    'dosa': 'One dosa has 20-25g carbs. Pair with sambar...',
    'rice': 'Kerala Red Rice is better than white rice...',
    'fish': 'Fish curry is excellent! High protein...'
}
```



## Testing the MVP

### 1. Create Account
- Go to `/register`
- Fill in: Name, Email, Password, Due Date, Weeks Pregnant
- Click "Create Account"

### 2. Log Glucose
- Dashboard → "Log Glucose"
- Enter reading value (e.g., 95)
- Select type (Fasting, Post-Breakfast, etc.)
- Optional: Add meal context
- Click "Save Reading"

### 3. Ask Chat Questions
- Dashboard → "Ask Questions"
- Try: "Can I eat dosa?"
- Try: "How much rice can I have?"
- Try: "Is fish curry okay?"

### 4. View History
- Dashboard → "View History"
- See all readings with color-coded status

---

## Troubleshooting

**Port 5000 already in use:**

```bash
# Mac
lsof -ti:5000 | xargs kill

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Database locked:**

```bash
# Stop the app (Ctrl+C)
rm database/gdm_chatbot.db
python app.py
# Database will be recreated
```

**Module not found:**

```bash
# Make sure you're in the virtual environment
# Look for (venv) in your terminal prompt

# Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

# Then reinstall
pip install -r requirements.txt
```

---

## Contributing

This is a class project. To add features:

1. Create a new branch

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes

3. Test locally

4. Create Pull Request

5. Update GitHub Project board

---

**Built with:**

- Flask
- SQLite (Database)
- Vanilla JavaScript (No frameworks - keeping it simple for now)

---

## License

Educational use only. Not for clinical deployment without proper regulatory approval.