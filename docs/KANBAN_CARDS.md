# GitHub Project - Kanban Card Templates (for future reference)
## GDM Care MVP

> **Purpose:** Template cards to organize MVP development work  

---

## Card Categories (Labels)

For your specific project, you may create something like these labels in your GitHub repo:

- The 'ui', 'api', 'database' cards are quite standard -- you may include more categories specific to your project if it helps you organize features within that category. Additionally, the category colors are just suggestions.

| Label | Color | When to Use |
|-------|-------|-------------|
| `ui` | (blue) | Frontend templates, styling, user interface |
| `api` | (green) | Backend routes, endpoints, data processing |
| `database` | (orange) | Schema design, queries, data models |
| `chat` | (purple) | Chatbot logic, RAG, LLM integration |
| `docs` | (gray) | Documentation, README, guides |

---

## Card Template Format

Each card should have:
1. **Title** - Clear, action-oriented (starts with verb)
2. **Size** - S/M/L estimate
3. **Description** - What needs to be done
4. **Acceptance Criteria** - How we know it's done
5. **Labels** - Category tags

---

## Template 1: UI Cards

### [M] Create Patient Dashboard Template

**Labels:** `ui`

**Description:**
Build the main dashboard page that patients see after login. Should display glucose statistics, recent readings, and action buttons for logging glucose and accessing chat.

**Tasks:**
- [ ] Design layout with stats cards (today's readings, averages)
- [ ] Add action cards for "Log Glucose" and "Ask Questions"
- [ ] Display recent 5 glucose readings in table format
- [ ] Style with professional medical aesthetic
- [ ] Make responsive for mobile screens

**Acceptance Criteria:**
- Dashboard loads at `/dashboard` route after login
- Shows correct patient name and gestational info
- Displays real-time glucose stats from database
- All links navigate to correct pages
- Looks professional on both desktop and mobile

**Files to Modify:**
- `templates/dashboard.html`
- `static/css/style.css`
- `app.py` (dashboard route)

---

### [S] Style Chat Interface

**Labels:** `ui`

**Description:**
Create a clean, WhatsApp-style chat interface with message bubbles, input field, and send button.

**Tasks:**
- [ ] Design message bubble components (user vs bot)
- [ ] Add timestamp to messages
- [ ] Create chat input form with send button
- [ ] Implement auto-scroll to latest message
- [ ] Add loading indicator while bot is "typing"

**Acceptance Criteria:**
- User messages appear on right (blue background)
- Bot messages appear on left (gray background)
- Chat scrolls to bottom automatically
- Send button disabled while waiting for response
- Mobile-friendly touch interactions

**Files to Modify:**
- `templates/chat.html`
- `static/css/style.css`
- `static/js/main.js` (scroll logic)

---

### [S] Create Glucose Logging Form

**Labels:** `ui`

**Description:**
Build a simple form for patients to log glucose readings with validation and helpful hints.

**Tasks:**
- [ ] Create form with reading value, type, meal context fields
- [ ] Add input validation (number range 40-400 mg/dL)
- [ ] Display target ranges info box
- [ ] Show success message after logging
- [ ] Handle errors gracefully

**Acceptance Criteria:**
- Form validates input before submission
- Dropdown shows all reading types (fasting, post-meal, etc.)
- Optional fields clearly marked
- Success flash message appears after save
- Returns to dashboard after logging

**Files to Modify:**
- `templates/log_glucose.html`
- `static/css/style.css`
- `app.py` (log_glucose route)

---

## Template 2: API Cards

### [M] Implement Chat Message API

**Labels:** `api`, `chat`

**Description:**
Create POST endpoint that receives user messages, gets chatbot response, saves both to database, and returns bot reply as JSON.

**Tasks:**
- [ ] Create `/chat/send` POST route
- [ ] Accept JSON payload with message text
- [ ] Call chatbot.get_response() function
- [ ] Save user message to chat_messages table
- [ ] Save bot response to chat_messages table
- [ ] Return JSON with bot response and timestamp

**Acceptance Criteria:**
- Endpoint returns 200 with valid JSON on success
- Returns 400 with error message on empty input
- Messages saved to database with correct patient_id
- Bot response generated using Kerala diet knowledge
- Language preference respected (English/Malayalam)

**Files to Modify:**
- `app.py` (send_message route)
- `lib/chatbot.py` (get_response method)

---

### [M] Build Glucose Logging Endpoint

**Labels:** `api`, `database`

**Description:**
Create POST endpoint that saves glucose readings to database with automatic high/low flagging based on ADA targets.

**Tasks:**
- [ ] Create `/log-glucose` POST route
- [ ] Extract form data (value, type, meal context, notes)
- [ ] Compare reading to patient's target ranges
- [ ] Set flagged_high and flagged_low booleans
- [ ] Insert into glucose_readings table
- [ ] Flash appropriate success/warning message
- [ ] Redirect to dashboard

**Acceptance Criteria:**
- Reading saved with correct patient_id
- Fasting readings flagged if > 95 mg/dL
- Post-meal readings flagged if > 120 mg/dL
- Low readings flagged if < 70 mg/dL
- Appropriate flash message shown based on flags
- Timestamp automatically recorded

**Files to Modify:**
- `app.py` (log_glucose route)
- `lib/models.py` (if adding helper functions)

---

### [S] Create Glucose History API

**Labels:** `api`, `database`

**Description:**
Build GET endpoint that retrieves and displays all glucose readings for the logged-in patient.

**Tasks:**
- [ ] Create `/glucose-history` route
- [ ] Query glucose_readings for current patient
- [ ] Order by timestamp DESC (most recent first)
- [ ] Limit to 50 readings for performance
- [ ] Pass data to template
- [ ] Render readings table

**Acceptance Criteria:**
- Shows all readings for logged-in patient only
- Most recent readings appear first
- Displays value, type, meal context, timestamp
- Color-codes rows (high/low/normal)
- Loads quickly even with many readings

**Files to Modify:**
- `app.py` (glucose_history route)
- `templates/glucose_history.html`

---

## Template 3: Database Cards

### [M] Design MVP Database Schema

**Labels:** `database`

**Description:**
Create minimal SQLite schema to support authentication, glucose tracking, and chat history.

**Tasks:**
- [ ] Design users table (email, password_hash, name, language)
- [ ] Design patients table (due_date, gestational_weeks, targets)
- [ ] Design glucose_readings table (value, type, timestamp, flags)
- [ ] Design chat_messages table (text, is_from_bot, timestamp)
- [ ] Add foreign key constraints
- [ ] Create indexes on common queries

**Acceptance Criteria:**
- All tables created in init_db() function
- Foreign keys properly reference users/patients
- Indexes on patient_id + timestamp columns
- CHECK constraints prevent invalid data
- Database initializes on first app run

**Files to Modify:**
- `lib/models.py` (init_db function)

---

### [S] Add Sample Data for Testing

**Labels:** `database`

**Description:**
Create script to populate database with realistic test data for development.

**Tasks:**
- [ ] Create 2 test user accounts
- [ ] Add patient profiles with different gestational weeks
- [ ] Insert 20+ glucose readings (mix of high/normal/low)
- [ ] Add 10+ chat messages (conversation history)
- [ ] Make data realistic (Kerala names, foods, times)

**Acceptance Criteria:**
- Script can be run multiple times safely
- Test accounts have different language preferences
- Glucose readings span multiple days
- Chat history shows both user and bot messages
- Can log in with test accounts

**Files to Create:**
- `database/seed_data.py` (new file)

---

## Template 4: Chat/RAG Cards

### [L] Implement Kerala Diet Knowledge Base

**Labels:** `chat`

**Description:**
Build chatbot with Kerala-specific food knowledge using simple keyword matching (MVP version before real LLM).

**Tasks:**
- [ ] Create knowledge dictionary with Kerala foods
- [ ] Add entries for: rice, dosa, idli, puttu, appam, fish, coconut
- [ ] Include carb counts and diet guidance for each
- [ ] Support both English and Malayalam responses
- [ ] Handle greetings and general questions
- [ ] Return helpful fallback for unknown questions

**Acceptance Criteria:**
- Bot responds to "Can I eat dosa?" with carb info
- Bot responds to "rice" questions with Kerala Red Rice guidance
- Malayalam responses when user preference is 'ml'
- Handles typos and variations (e.g., "dosa", "dhosa", "dose")
- Default response suggests asking about specific foods

**Files to Modify:**
- `lib/chatbot.py` (ChatbotRAG class)

---

### [M] Add Chat Message Persistence

**Labels:** `chat`, `database`

**Description:**
Ensure all chat messages are saved to database and displayed in conversation history.

**Tasks:**
- [ ] Save user message before calling chatbot
- [ ] Save bot response after generation
- [ ] Load conversation history on /chat page load
- [ ] Display messages in chronological order
- [ ] Show timestamps in readable format

**Acceptance Criteria:**
- All messages persist across page refreshes
- Conversation history loads when revisiting /chat
- Messages associated with correct patient_id
- Timestamps display as "10:05 AM" format
- Only logged-in user's messages visible to them

**Files to Modify:**
- `app.py` (chat and send_message routes)
- `templates/chat.html`

---

## Template 5: Documentation Cards

### [S] Write Setup Instructions

**Labels:** `docs`

**Description:**
Create clear README with setup steps for both Mac and Windows users.

**Tasks:**
- [ ] Document prerequisites (Python 3.10+)
- [ ] Write Mac setup instructions (bash commands)
- [ ] Write Windows setup instructions (cmd commands)
- [ ] Add troubleshooting section
- [ ] Include screenshots or GIFs if helpful

**Acceptance Criteria:**
- Someone new to Python can follow and succeed
- Both platforms (Mac/Windows) covered
- Common errors addressed in troubleshooting
- Links to external resources where helpful

**Files to Modify:**
- `README.md`

---

### [S] Document API Endpoints

**Labels:** `docs`

**Description:**
Create reference documentation for all API endpoints in the app.

**Tasks:**
- [ ] List all routes (authentication, dashboard, glucose, chat)
- [ ] Document request/response formats
- [ ] Show example payloads
- [ ] Note authentication requirements
- [ ] Add error response examples

**Acceptance Criteria:**
- All routes documented
- JSON request/response examples included
- HTTP status codes explained
- Authentication requirements clear

**Files to Create:**
- `docs/API.md` (new file)

---

## How to Use These Templates

### During Lecture (Class Activity)

1. **Instructor opens GitHub Project board**
2. **Class votes on MVP features** (from previous activity)
3. **For each MVP feature, create 2-3 cards using templates above**
4. **Assign sizes together** (S/M/L)
5. **Add to "To Do" column**

### Example Workflow

**Feature:** "Patient can log glucose readings"

**Cards needed:**
1. [S] Create Glucose Logging Form (UI)
2. [M] Build Glucose Logging Endpoint (API)
3. [S] Display readings on dashboard (UI)

**Feature:** "Patient can ask diet questions"

**Cards needed:**
1. [L] Implement Kerala Diet Knowledge Base (Chat)
2. [S] Style Chat Interface (UI)
3. [M] Implement Chat Message API (API)
4. [M] Add Chat Message Persistence (Database)

---

## Estimation Guide

| Size | Time | Complexity | Example |
|------|------|------------|---------|
| **S** | 1-2 hours | Simple, clear requirements | Style a form, add a table |
| **M** | 3-5 hours | Moderate, some unknowns | Create API endpoint, build feature |
| **L** | 6-8 hours | Complex, requires research | Implement RAG, design schema |

**Rule:** If a card is bigger than L, break it into multiple smaller cards!

---
