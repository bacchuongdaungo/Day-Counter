import os
import random
import google.generativeai as genai
from flask import jsonify, request
from datetime import datetime

# Global cache and API key setup
phrase_cache = []
CACHE_SIZE = 10
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def _refill_cache():
    """Internal helper function to call the AI and refill the cache."""
    global phrase_cache
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Generate a numbered list of {CACHE_SIZE} short, blunt motivational phrases for someone quitting smoking. Make them cheeky or slightly rude."
        response = model.generate_content(prompt)
        phrases = response.text.strip().split('\n')
        cleaned_phrases = [p.split('. ', 1)[-1].strip() for p in phrases if '. ' in p]
        if cleaned_phrases:
            phrase_cache = cleaned_phrases
        else:
            phrase_cache = ["AI response format was unexpected. Try again."]
    except Exception as e:
        print(f"Cache refill failed: {e}")
        phrase_cache = ["Could not reach AI. You are strong enough without it."]

# The single entry point function for Google Cloud Functions
def main_handler(request):
    """
    This single function handles all requests and includes CORS headers.
    """
    # This block handles CORS preflight requests from the browser.
    # It's a standard requirement for cross-origin requests.
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # These headers are for the actual request, telling the browser the response is safe.
    cors_headers = {
        'Access-Control-Allow-Origin': '*'
    }

    path = request.path
    if path.endswith("/get-phrase"):
        if not phrase_cache:
            _refill_cache()
        phrase = phrase_cache.pop(0) if phrase_cache else "Cache empty, try again."
        return (jsonify({"phrase": phrase}), 200, cors_headers)

    elif path.endswith("/get-day-count"):
        start_date_str = request.args.get('startDate')
        if not start_date_str:
            return (jsonify({"error": "startDate parameter is required."}), 400, cors_headers)
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            today = datetime.utcnow().date()
            day_count = (today - start_date).days
            return (jsonify({"day_count": day_count + 1}), 200, cors_headers)
        except ValueError:
            return (jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400, cors_headers)
    
    else:
        return (jsonify({"message": "Welcome to the Day Counter API."}), 200, cors_headers)