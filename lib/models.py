"""
Database models and initialization
"""

import sqlite3
import os
from flask_login import UserMixin


class User(UserMixin):
    """User model for Flask-Login"""
    def __init__(self, id, email, name, language_preference='ml'):
        self.id = id
        self.email = email
        self.name = name
        self.language_preference = language_preference


def init_db():
    """Initialize database with schema"""
    os.makedirs('database', exist_ok=True)
    
    conn = sqlite3.connect('database/gdm_chatbot.db')
    
    conn.executescript('''
        -- Users table (authentication)
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            phone TEXT,
            language_preference TEXT DEFAULT 'ml' CHECK(language_preference IN ('en', 'ml')),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_login DATETIME
        );

        -- Patients table (GDM-specific data)
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            due_date DATE NOT NULL,
            diagnosis_date DATE NOT NULL,
            gestational_age_weeks INTEGER NOT NULL,
            kerala_region TEXT,
            target_fasting_glucose REAL DEFAULT 95.0,
            target_postmeal_glucose REAL DEFAULT 120.0,
            
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        -- Glucose readings table (tracking)
        CREATE TABLE IF NOT EXISTS glucose_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            reading_value REAL NOT NULL,
            timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            reading_type TEXT NOT NULL CHECK(reading_type IN (
                'fasting', 'post_breakfast', 'post_lunch', 'post_dinner', 'bedtime'
            )),
            meal_context TEXT,
            notes TEXT,
            flagged_high BOOLEAN DEFAULT 0,
            flagged_low BOOLEAN DEFAULT 0,
            
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );

        -- Chat messages table (conversation history)
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            message_text TEXT NOT NULL,
            is_from_bot BOOLEAN NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            language TEXT NOT NULL CHECK(language IN ('en', 'ml')),
            
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );

        -- Indexes for performance
        CREATE INDEX IF NOT EXISTS idx_glucose_patient_timestamp 
            ON glucose_readings(patient_id, timestamp DESC);
        
        CREATE INDEX IF NOT EXISTS idx_chat_patient_timestamp 
            ON chat_messages(patient_id, timestamp ASC);
    ''')
    
    conn.commit()
    conn.close()
    
    print("✓ Database initialized successfully")