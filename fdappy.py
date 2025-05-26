from flask import Flask, request, send_from_directory, jsonify
import os
import sqlite3
import uuid
import json
from datetime import datetime

app = Flask(__name__, static_folder='.')

DATABASE_FILE = os.path.join(os.path.dirname(__file__), 'submissions.db')

def init_db():
    with sqlite3.connect(DATABASE_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid TEXT UNIQUE NOT NULL,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def get_db():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/submissions.json', methods=['POST'])
def save_submission():
    submission = request.get_json()
    if not submission:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    # Add or ensure UUID
    if 'uuid' not in submission or not submission['uuid']:
        submission['uuid'] = str(uuid.uuid4())
    
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            conn.execute(
                'INSERT INTO submissions (uuid, data) VALUES (?, ?)',
                (submission['uuid'], json.dumps(submission))
            )
            conn.commit()
        return jsonify({'success': True, 'uuid': submission['uuid']})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'UUID already exists'}), 400
    except Exception as e:
        print('Error writing to database:', e)
        return jsonify({'success': False, 'error': 'Failed to save submission.'}), 500

@app.route('/submissions.json', methods=['GET'])
def get_submissions():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page
    
    try:
        with get_db() as conn:
            # Get total count
            total = conn.execute('SELECT COUNT(*) FROM submissions').fetchone()[0]
            
            # Get paginated submissions
            cursor = conn.execute(
                'SELECT * FROM submissions ORDER BY created_at DESC LIMIT ? OFFSET ?',
                (per_page, offset)
            )
            submissions = []
            for row in cursor:
                submission = json.loads(row['data'])
                submission['created_at'] = row['created_at']
                submissions.append(submission)
            
            return jsonify({
                'success': True,
                'submissions': submissions,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'total_pages': (total + per_page - 1) // per_page
                }
            })
    except Exception as e:
        print('Error retrieving submissions:', e)
        return jsonify({'success': False, 'error': 'Failed to retrieve submissions.'}), 500

@app.route('/submissions/<uuid>', methods=['GET'])
def get_submission(uuid):
    try:
        with get_db() as conn:
            cursor = conn.execute('SELECT * FROM submissions WHERE uuid = ?', (uuid,))
            row = cursor.fetchone()
            
            if row is None:
                return jsonify({'success': False, 'error': 'Submission not found'}), 404
            
            submission = json.loads(row['data'])
            submission['created_at'] = row['created_at']
            return jsonify({'success': True, 'submission': submission})
    except Exception as e:
        print('Error retrieving submission:', e)
        return jsonify({'success': False, 'error': 'Failed to retrieve submission.'}), 500

if __name__ == '__main__':
    init_db()  # Initialize the database when starting the app
    app.run(host='0.0.0.0', port=3000, debug=True) 