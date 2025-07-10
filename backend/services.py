import os
import random
import google.generativeai as genai
from datetime import datetime

# --- Configuration ---
CACHE_SIZE = 20
REFILL_THRESHOLD = 10 

# --- Caching Mechanism (Global Scope) ---
phrase_cache = []

# --- Securely Configure the Gemini API ---
# This setup runs once when the function instance starts.
# We will add a try-except block here as well for maximum safety.
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
    else:
        print("CRITICAL: GOOGLE_API_KEY environment variable not set.")
except Exception as e:
    print(f"FATAL: Could not configure Google AI. Error: {e}")
    api_key = None # Ensure api_key is None if configuration fails

def _refill_cache_from_api():
    """
    This is the core AI logic. It fetches new phrases and adds them to the cache.
    """
    global phrase_cache
    print(f"Refilling cache. Current size: {len(phrase_cache)}")
    try:
        if not api_key:
            raise ValueError("API key is not configured or failed to initialize.")
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Generate 10 blunt motivational phrases for someone quitting smoking. Make them cheeky or slightly rude. Every once in a while, sneak a very comforting and nurturing phrase. Maximum 15 words each."
        
        response = model.generate_content(prompt)
        phrases = response.text.strip().split('\n')
        
        new_phrases = [p.split('. ', 1)[-1].strip() for p in phrases if '. ' in p]
        
        for phrase in new_phrases:
            if phrase not in phrase_cache:
                phrase_cache.append(phrase)
        
        print(f"Refill complete. New cache size: {len(phrase_cache)}")

    except Exception as e:
        print(f"Cache refill failed: {e}")
        # If the refill fails, add a fallback so the app doesn't break.
        if not phrase_cache:
            phrase_cache.append("Could not reach the AI. You're stronger than this moment.")

def get_new_phrase():
    """
    This is the main function called by our API.
    It is wrapped in a try-except block to be completely crash-proof.
    """
    try:
        if not phrase_cache:
            _refill_cache_from_api()

        try:
            random_index = random.randrange(len(phrase_cache))
            phrase_to_return = phrase_cache.pop(random_index)
        except (ValueError, IndexError):
            phrase_to_return = "Getting a new batch of phrases, please wait a moment."
            _refill_cache_from_api()

        if len(phrase_cache) < REFILL_THRESHOLD:
            _refill_cache_from_api()

        return phrase_to_return
    except Exception as e:
        # This is the ultimate safety net. If anything above fails,
        # we log the error and return a safe response.
        print(f"FATAL ERROR in get_new_phrase: {e}")
        return "An error occurred, but you're still on the right track."

def calculate_day_count(start_date_str: str):
    """The core logic for calculating the day count."""
    # This function is already safe because main.py handles its ValueError.
    # No changes are needed here.
    if not start_date_str:
        raise ValueError("startDate parameter is required.")
    
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    today = datetime.utcnow().date()
    return (today - start_date).days + 1

