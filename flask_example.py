"""
Flask API example for testing the pytest generator.
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID."""
    # Simulate database call
    user = {'id': user_id, 'name': f'User {user_id}', 'email': f'user{user_id}@example.com'}
    return jsonify(user)

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    user = {
        'id': 123,
        'name': data['name'],
        'email': data.get('email', '')
    }
    return jsonify(user), 201

if __name__ == '__main__':
    app.run(debug=True)
