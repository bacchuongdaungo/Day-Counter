import os
import random
import google.generativeai as genai
from flask import jsonify, request
from datetime import datetime

# --- Caching Mechanism (Global Scope) ---
phrase_cache = []
CACHE_SIZE = 10

# --- Securely Configure the Gemini API (Global Scope) ---
# This setup runs once when the function instance starts.
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    # This will be visible in the logs if the key is missing
    print("CRITICAL: GOOGLE_API_KEY environment variable not set.")

def _refill_cache():
    """Internal helper function to call the AI and refill the cache."""
    global phrase_cache
    print("Cache is empty. Refilling from Gemini API...")
    try:
        if not api_key:
            raise ValueError("API key is not configured.")
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Generate a numbered list of {CACHE_SIZE} short, blunt motivational phrases for someone quitting smoking. Make them cheeky or slightly rude. Maximum 15 words each."
        response = model.generate_content(prompt)
        phrases = response.text.strip().split('\n')
        cleaned_phrases = [p.split('. ', 1)[-1].strip() for p in phrases if '. ' in p]
        if cleaned_phrases:
            phrase_cache = cleaned_phrases
        else:
            phrase_cache = ["AI response format was unexpected. Try again."]
    except Exception as e:
        print(f"Cache refill failed: {e}. Using a single fallback phrase.")
        phrase_cache = ["Could not reach the AI. You're on your own, champ."]

# --- The MAIN ENTRY POINT for the Cloud Function ---
# This single function will handle all incoming requests.
def main_handler(request):
    """
    A single function that routes traffic based on the URL path.
    This is the standard pattern for multi-path Cloud Functions.
    """
    path = request.path

    # --- ROUTE 1: Get Phrase ---
    if path.endswith("/get-phrase"):
        if not phrase_cache:
            _refill_cache()
        phrase = phrase_cache.pop(0) if phrase_cache else "Cache is empty, try again."
        return jsonify({"phrase": phrase})

    # --- ROUTE 2: Get Day Count ---
    elif path.endswith("/get-day-count"):
        start_date_str = request.args.get('startDate')
        if not start_date_str:
            return jsonify({"error": "startDate parameter is required."}), 400
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            today = datetime.utcnow().date()
            day_count = (today - start_date).days
            return jsonify({"day_count": day_count + 1})
        except ValueError:
            return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400

    # --- Default Route ---
    else:
        return jsonify({
            "message": "Welcome to the Day Counter API. Use /get-phrase or /get-day-count endpoints."
        }), 200