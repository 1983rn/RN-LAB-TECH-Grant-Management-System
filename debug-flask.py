#!/usr/bin/env python3
"""
Debug Flask app to identify the issue
"""

import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask app is working!"

@app.route('/test', methods=['POST'])
def test():
    """Simple test endpoint"""
    try:
        data = request.get_json()
        print(f"Received data: {data}")
        return jsonify({'success': True, 'received': data})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🔍 Starting debug Flask app on port 5174")
    app.run(debug=True, host='0.0.0.0', port=5174)
