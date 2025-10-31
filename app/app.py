
from flask import Flask, render_template, request, jsonify
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database configuration
DATABASE = '/app/data/visitors.db'

def init_db():
    """Initialize the database with a visitors table"""
    os.makedirs('/app/data', exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            visit_time TIMESTAMP,
            user_agent TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_visitor(ip_address, user_agent):
    """Log visitor information to database"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO visitors (ip_address, visit_time, user_agent)
        VALUES (?, ?, ?)
    ''', (ip_address, datetime.now(), user_agent))
    conn.commit()
    conn.close()

def get_visitor_count():
    """Get total number of visitors"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM visitors')
    count = cursor.fetchone()[0]
    conn.close()
    return count

@app.route('/')
def home():
    """Main page route"""
    # Log the visitor
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    user_agent = request.environ.get('HTTP_USER_AGENT', 'Unknown')
    log_visitor(ip_address, user_agent)
    
    # Get visitor count
    visitor_count = get_visitor_count()
    
    return f'''
    <html>
    <head>
        <title>Flask Docker App</title>
    </head>
    <body>
        <h1>Welcome to Flask Docker Application!</h1>
        <p><strong>Application Status:</strong> Running in Docker Container</p>
        <p><strong>Total Visitors:</strong> {visitor_count}</p>
        <p><strong>Your IP:</strong> {ip_address}</p>
        <p>This is a simple Flask web application running inside a Docker container.</p>
    </body>
    </html>
    '''

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'visitors': get_visitor_count()
    })

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
