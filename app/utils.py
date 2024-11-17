from flask import jsonify

def validate_fields(data, required_fields):
    for field in required_fields:
        if field not in data or not isinstance(data[field], str):
            return False, f"{field} must be a string"
    return True, None


def error_response(message, status_code):
    """Generate a standardized error response."""
    return jsonify({"error": message}), status_code
