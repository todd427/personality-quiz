from flask import Flask, request, send_from_directory, jsonify
import os
import json
import uuid

app = Flask(__name__, static_folder='.')

SUBMISSIONS_FILE = os.path.join(os.path.dirname(__file__), 'submissions.json')

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
        if os.path.exists(SUBMISSIONS_FILE):
            with open(SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
                try:
                    submissions = json.load(f)
                except Exception:
                    submissions = []
        else:
            submissions = []
        submissions.append(submission)
        with open(SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(submissions, f, indent=2)
        return jsonify({'success': True, 'uuid': submission['uuid']})
    except Exception as e:
        print('Error writing to submissions.json:', e)
        return jsonify({'success': False, 'error': 'Failed to save submission.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True) 