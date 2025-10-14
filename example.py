"""
Example Python code for testing the pytest generator.
"""

import requests
import sqlite3
from typing import List, Dict, Optional


def calculate_total(items: List[Dict[str, float]], tax_rate: float = 0.1) -> float:
    """Calculate total with tax for a list of items."""
    if not items:
        return 0.0
    
    subtotal = sum(item.get('price', 0) for item in items)
    return subtotal * (1 + tax_rate)


def fetch_user_data(user_id: int) -> Optional[Dict[str, str]]:
    """Fetch user data from external API."""
    try:
        response = requests.get(f"https://api.example.com/users/{user_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


class UserService:
    """Service for managing user data."""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_user(self, user_id: int) -> Optional[Dict[str, str]]:
        """Get user from database."""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'email': result[2]
            }
        return None
    
    def create_user(self, name: str, email: str) -> int:
        """Create a new user."""
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        self.db.commit()
        return cursor.lastrowid
