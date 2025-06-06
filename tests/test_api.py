import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import fdappy


def setup_module(module):
    # use a temporary db file within tests directory if not provided
    fdappy.DATABASE_FILE = os.path.join(os.path.dirname(__file__), 'test.db')
    if os.path.exists(fdappy.DATABASE_FILE):
        os.remove(fdappy.DATABASE_FILE)
    fdappy.init_db()
    module.client = fdappy.app.test_client()


def teardown_module(module):
    if os.path.exists(fdappy.DATABASE_FILE):
        os.remove(fdappy.DATABASE_FILE)


def test_post_submission_returns_uuid_and_success():
    response = client.post('/submissions.json', json={'name': 'Tester'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'uuid' in data and isinstance(data['uuid'], str)


def test_get_submissions_returns_data_and_pagination():
    # Ensure there is at least one entry from previous test
    response = client.get('/submissions.json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'submissions' in data and isinstance(data['submissions'], list)
    assert len(data['submissions']) >= 1
    sub = data['submissions'][0]
    assert 'uuid' in sub and 'name' in sub
    assert 'pagination' in data
    pagination = data['pagination']
    assert pagination['page'] == 1
    assert 'total' in pagination and pagination['total'] >= 1
