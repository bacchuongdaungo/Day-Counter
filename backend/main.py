from flask import jsonify, request
import services

def main_handler(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    path = request.path

    if path.endswith("/get-phrase"):
        phrase = services.get_new_phrase()
        return (jsonify({"phrase": phrase}), 200, headers)

    elif path.endswith("/get-day-count"):
        start_date_str = request.args.get('startDate')
        try:
            day_count = services.calculate_day_count(start_date_str)
            return (jsonify({"day_count": day_count}), 200, headers)
        except ValueError as e:
            return (jsonify({"error": str(e)}), 400, headers)

    else:
        return (jsonify({"message": "API is running."}), 200, headers)