"""
Chatbot with RAG (Retrieval-Augmented Generation)
Uses lightweight local LLM (Llama 3.2 1B) + FAISS for Kerala diet knowledge
"""

import os
import json
from typing import List, Dict


class ChatbotRAG:
    """
    Simple RAG chatbot for GDM diet questions
    
    In production, this would use:
    - llama-cpp-python for local LLM
    - FAISS for vector search
    - sentence-transformers for embeddings
    
    For MVP: Using rule-based responses with Kerala diet knowledge
    """
    
    def __init__(self):
        """Initialize chatbot and load knowledge base"""
        self.knowledge_base = self._load_knowledge()
        print("✓ Chatbot initialized with Kerala diet knowledge")
    
    def _load_knowledge(self) -> Dict:
        """Load Kerala-specific diet knowledge"""
        # In production: Load from rag/knowledge_base/
        # For MVP: Hardcoded Kerala food knowledge
        return {
            'rice': {
                'en': 'White rice has a high glycemic index. Try Kerala Red Rice (Matta Rice) instead - 1 cup cooked has about 45g carbs. Eat with protein like fish curry to slow glucose spike.',
                'ml': 'വെള്ള അരിക്ക് ഉയർന്ന ഗ്ലൈസെമിക് സൂചികയുണ്ട്. പകരം കേരള ചുവന്ന അരി (മട്ട അരി) ഉപയോഗിക്കുക - 1 കപ്പ് വേവിച്ചതിൽ ഏകദേശം 45g കാർബോഹൈഡ്രേറ്റ് ഉണ്ട്. മത്സ്യ കറിയുടെ കൂടെ കഴിക്കുക.'
            },
            'dosa': {
                'en': 'One medium dosa (about 50g) has 20-25g carbs. Made from fermented rice and lentils, it\'s a good choice. Pair with sambar (protein) and avoid potato masala filling. Best for breakfast.',
                'ml': 'ഒരു ഇടത്തരം ദോശയിൽ (ഏകദേശം 50g) 20-25g കാർബോഹൈഡ്രേറ്റ് ഉണ്ട്. പുളിപ്പിച്ച അരിയും പയറും കൊണ്ട് ഉണ്ടാക്കുന്നത് നല്ലതാണ്. സാമ്പാറിന്റെ കൂടെ കഴിക്കുക.'
            },
            'idli': {
                'en': '2 medium idlis have about 20g carbs. Fermentation makes them easier to digest. Good for breakfast. Eat with sambar or fish curry, not coconut chutney (high fat).',
                'ml': '2 ഇടത്തരം ഇഡ്ഡലിയിൽ ഏകദേശം 20g കാർബോഹൈഡ്രേറ്റ് ഉണ്ട്. പുളിപ്പിക്കൽ ദഹനം എളുപ്പമാക്കുന്നു. സാമ്പാറിന്റെ കൂടെ നല്ലത്.'
            },
            'puttu': {
                'en': 'One small puttu (100g) has 25-30g carbs. Steam-cooked, so healthier than fried. Pair with kadala curry (protein) not banana. Check glucose 2 hours after.',
                'ml': 'ഒരു ചെറിയ പുട്ടിൽ (100g) 25-30g കാർബോഹൈഡ്രേറ്റ് ഉണ്ട്. ആവിയിൽ വേവിച്ചത്, ആരോഗ്യകരമാണ്. കടല കറിയുടെ കൂടെ കഴിക്കുക.'
            },
            'appam': {
                'en': '2 plain appams have about 30g carbs. Soft center, crispy edges. Better than rice at night. Eat with vegetable stew or egg curry, not sweetened coconut milk.',
                'ml': '2 വെള്ള അപ്പങ്ങളിൽ ഏകദേശം 30g കാർബോഹൈഡ്രേറ്റ് ഉണ്ട്. രാത്രി അരിയേക്കാൾ നല്ലത്. വെജിറ്റബിൾ സ്റ്റൂവിന്റെ കൂടെ കഴിക്കുക.'
            },
            'parotta': {
                'en': 'Avoid parotta - it\'s made with refined flour (maida) and has high fat from layering. One parotta has 40g+ carbs. Choose dosa or chapati instead.',
                'ml': 'പരോട്ട ഒഴിവാക്കുക - മൈദയും കൊഴുപ്പും കൂടുതലാണ്. ഒരു പരോട്ടയിൽ 40g+ കാർബോഹൈഡ്രേറ്റ്. പകരം ദോശ അല്ലെങ്കിൽ ചപ്പാത്തി കഴിക്കുക.'
            },
            'fish': {
                'en': 'Fish curry is excellent! High protein, low carb. Kerala fish (sardines, mackerel, pomfret) are rich in omega-3. Eat with small portion of rice. No limits on fish amount.',
                'ml': 'മത്സ്യ കറി മികച്ചതാണ്! ഉയർന്ന പ്രോട്ടീൻ, കുറഞ്ഞ കാർബോഹൈഡ്രേറ്റ്. കേരള മത്സ്യം (മത്തി, ആയില, വെള്ളത്താണി) ഒമേഗ-3 സമ്പന്നമാണ്.'
            },
            'coconut': {
                'en': 'Fresh coconut is fine in moderation. Has healthy fats. Coconut oil for cooking is good. Avoid sweetened coconut milk. Grated coconut on dishes is okay - about 1/4 cup daily.',
                'ml': 'പുതിയ തേങ്ങ മിതമായി കഴിക്കാം. ആരോഗ്യകരമായ കൊഴുപ്പുണ്ട്. തേങ്ങാ എണ്ണ പാചകത്തിന് നല്ലത്. പഞ്ചസാര ചേർത്ത തേങ്ങാപ്പാൽ ഒഴിവാക്കുക.'
            },
            'fruits': {
                'en': 'Best fruits: Guava, papaya (small), apple (with skin). Limit: Banana, mango, grapes (high sugar). One small fruit = 15g carbs. Eat with meals, not alone.',
                'ml': 'നല്ല പഴങ്ങൾ: പേരയ്ക്ക, പപ്പായ (ചെറുത്), ആപ്പിൾ (തൊലിയോടെ). പരിമിതപ്പെടുത്തുക: വാഴപ്പഴം, മാമ്പഴം, മുന്തിരിങ്ങ.'
            },
            'vegetables': {
                'en': 'All vegetables are good! Kerala favorites: Drumstick, bitter gourd (pavakka), snake gourd (padavalanga), okra (vendakka). No limits. Eat plenty with every meal.',
                'ml': 'എല്ലാ പച്ചക്കറികളും നല്ലതാണ്! കേരള പ്രിയപ്പെട്ടവ: മുരിങ്ങക്കായ, പാവയ്ക്ക, പടവലങ്ങ, വെണ്ടയ്ക്ക. പരിമിതിയില്ല.'
            },
            'general': {
                'en': 'For GDM diet: (1) Eat small frequent meals, (2) Always pair carbs with protein, (3) Choose whole grains, (4) Check glucose 2 hours after meals. Target: Fasting <95, Post-meal <120 mg/dL.',
                'ml': 'GDM ഭക്ഷണക്രമം: (1) ചെറിയ ഭക്ഷണം പതിവായി കഴിക്കുക, (2) കാർബോഹൈഡ്രേറ്റ് പ്രോട്ടീനോടൊപ്പം, (3) ധാന്യങ്ങൾ തിരഞ്ഞെടുക്കുക, (4) ഭക്ഷണത്തിന് 2 മണിക്കൂർ ശേഷം ഗ്ലൂക്കോസ് പരിശോധിക്കുക.'
            }
        }
    
    def get_response(self, user_message: str, language: str = 'en', region: str = 'Kerala') -> str:
        """
        Generate response to user question
        
        Args:
            user_message: User's question
            language: 'en' or 'ml'
            region: User's region (for context)
            
        Returns:
            Bot response string
        """
        # Normalize message
        msg_lower = user_message.lower()
        
        # Check for greetings
        if any(word in msg_lower for word in ['hello', 'hi', 'hey', 'namaste', 'നമസ്കാരം']):
            if language == 'ml':
                return 'നമസ്കാരം! ഗർഭകാല പ്രമേഹത്തെ കുറിച്ച് എന്നെ ചോദിക്കൂ. ഭക്ഷണം, ഗ്ലൂക്കോസ് ട്രാക്കിംഗ്, അല്ലെങ്കിൽ കേരള വിഭവങ്ങളെ കുറിച്ച് സഹായിക്കാം.'
            return 'Hello! I\'m here to help with your GDM questions. Ask me about Kerala foods, glucose tracking, or diet tips!'
        
        # Check knowledge base for food-related questions
        for food, info in self.knowledge_base.items():
            if food in msg_lower or (food == 'general' and 'help' in msg_lower):
                return info.get(language, info['en'])
        
        # Check for glucose reading questions
        if 'glucose' in msg_lower or 'sugar' in msg_lower or 'reading' in msg_lower:
            if language == 'ml':
                return 'നിങ്ങളുടെ ഗ്ലൂക്കോസ് റീഡിംഗ് രേഖപ്പെടുത്താൻ "Log Glucose" ബട്ടൺ ഉപയോഗിക്കുക. ലക്ഷ്യം: ഉപവാസം <95, ഭക്ഷണത്തിന് ശേഷം <120 mg/dL. എന്തെങ്കിലും ഭക്ഷണത്തെ കുറിച്ച് ചോദിക്കൂ!'
            return 'Use the "Log Glucose" button to record your readings. Target: Fasting <95, Post-meal <120 mg/dL. Ask me about any Kerala foods!'
        
        # Check for meal planning
        if 'meal' in msg_lower or 'breakfast' in msg_lower or 'lunch' in msg_lower or 'dinner' in msg_lower:
            if language == 'ml':
                return 'നല്ല ഭക്ഷണ പദ്ധതി:\n- പ്രാതൽ: ഇഡ്ഡലി + സാമ്പാർ\n- ഉച്ച: ചെറിയ അരി + മത്സ്യ കറി + പച്ചക്കറി\n- രാത്രി: അപ്പം + വെജിറ്റബിൾ സ്റ്റൂ\n\nഓരോ ഭക്ഷണത്തിനും 2 മണിക്കൂർ ശേഷം ഗ്ലൂക്കോസ് പരിശോധിക്കുക!'
            return 'Good meal plan:\n- Breakfast: Idli + Sambar\n- Lunch: Small rice + Fish curry + Vegetables\n- Dinner: Appam + Vegetable stew\n\nCheck glucose 2 hours after each meal!'
        
        # Default response
        if language == 'ml':
            return 'ക്ഷമിക്കണം, ഞാൻ ഇതുവരെ ആ ഉത്തരം പഠിച്ചിട്ടില്ല. എന്നെ കേരള ഭക്ഷണങ്ങളെ കുറിച്ച് ചോദിക്കൂ: അരി, ദോശ, ഇഡ്ഡലി, പുട്ട്, അപ്പം, മത്സ്യം, തേങ്ങ, പഴങ്ങൾ, പച്ചക്കറികൾ.'
        return 'I don\'t have information on that yet. Try asking me about Kerala foods: rice, dosa, idli, puttu, appam, fish, coconut, fruits, vegetables. Or ask about glucose tracking!'


# For testing
if __name__ == '__main__':
    bot = ChatbotRAG()
    
    # Test questions
    print("\nTest 1 - English:")
    print("Q: Can I eat dosa?")
    print("A:", bot.get_response("Can I eat dosa?", language='en'))
    
    print("\nTest 2 - Malayalam:")
    print("Q: ദോശ കഴിക്കാമോ?")
    print("A:", bot.get_response("ദോശ കഴിക്കാമോ?", language='ml'))
    
    print("\nTest 3 - General:")
    print("Q: What should I eat?")
    print("A:", bot.get_response("What should I eat for breakfast?", language='en'))