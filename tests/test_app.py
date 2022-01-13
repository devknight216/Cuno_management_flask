import conftest
import pytest

def test_hello_world(client):
    # client.get for GET request, client.post for POST, etc. 
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Hello from Flask' in rv.data

def test_json_api(client):
    res = client.post("/api/submit_credentials")
    assert res.status_code == 200
    assert res.json == {'OK': 'in json'}
