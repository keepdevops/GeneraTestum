"""
A Flask API example for testing the test generator.
"""

from flask import Flask, request, jsonify
from typing import Dict, List, Optional
import json
import uuid
from datetime import datetime


app = Flask(__name__)

# In-memory storage for demo
users_db: Dict[str, Dict] = {}
posts_db: Dict[str, Dict] = {}


class User:
    """User model."""
    
    def __init__(self, username: str, email: str, name: str):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.name = name
        self.created_at = datetime.now().isoformat()
        self.is_active = True
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at,
            'is_active': self.is_active
        }
    
    def update(self, **kwargs) -> None:
        """Update user fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Post:
    """Post model."""
    
    def __init__(self, title: str, content: str, author_id: str):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = content
        self.author_id = author_id
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        self.likes = 0
    
    def to_dict(self) -> Dict:
        """Convert post to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'likes': self.likes
        }
    
    def like(self) -> None:
        """Increment like count."""
        self.likes += 1
        self.updated_at = datetime.now().isoformat()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['username', 'email', 'name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if username already exists
    for user_id, user_data in users_db.items():
        if user_data['username'] == data['username']:
            return jsonify({'error': 'Username already exists'}), 409
    
    user = User(
        username=data['username'],
        email=data['email'],
        name=data['name']
    )
    
    users_db[user.id] = user.to_dict()
    
    return jsonify(user.to_dict()), 201


@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id: str):
    """Get user by ID."""
    if user_id not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(users_db[user_id])


@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id: str):
    """Update user information."""
    if user_id not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update user data
    for key, value in data.items():
        if key in ['username', 'email', 'name']:
            users_db[user_id][key] = value
    
    users_db[user_id]['updated_at'] = datetime.now().isoformat()
    
    return jsonify(users_db[user_id])


@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id: str):
    """Delete a user."""
    if user_id not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    del users_db[user_id]
    
    # Also delete user's posts
    posts_to_delete = [post_id for post_id, post in posts_db.items() 
                      if post['author_id'] == user_id]
    for post_id in posts_to_delete:
        del posts_db[post_id]
    
    return jsonify({'message': 'User deleted successfully'}), 200


@app.route('/api/posts', methods=['POST'])
def create_post():
    """Create a new post."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['title', 'content', 'author_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if author exists
    if data['author_id'] not in users_db:
        return jsonify({'error': 'Author not found'}), 404
    
    post = Post(
        title=data['title'],
        content=data['content'],
        author_id=data['author_id']
    )
    
    posts_db[post.id] = post.to_dict()
    
    return jsonify(post.to_dict()), 201


@app.route('/api/posts/<post_id>', methods=['GET'])
def get_post(post_id: str):
    """Get post by ID."""
    if post_id not in posts_db:
        return jsonify({'error': 'Post not found'}), 404
    
    return jsonify(posts_db[post_id])


@app.route('/api/posts/<post_id>/like', methods=['POST'])
def like_post(post_id: str):
    """Like a post."""
    if post_id not in posts_db:
        return jsonify({'error': 'Post not found'}), 404
    
    posts_db[post_id]['likes'] += 1
    posts_db[post_id]['updated_at'] = datetime.now().isoformat()
    
    return jsonify(posts_db[post_id])


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all posts with optional filtering."""
    author_id = request.args.get('author_id')
    limit = request.args.get('limit', 10, type=int)
    
    posts = list(posts_db.values())
    
    if author_id:
        posts = [post for post in posts if post['author_id'] == author_id]
    
    # Sort by creation date (newest first)
    posts.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify(posts[:limit])


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
