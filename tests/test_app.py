import conftest
import pytest
from flask_app import render_tabbed_page
from flask_app import render_tabbed_content

def test_hello_world(client):
    # client.get for GET request, client.post for POST, etc. 
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Hello from Flask' in rv.data

def test_json_api(client):
    res = client.post("/api/submit_credentials")
    assert res.status_code == 200
    assert res.json == {'OK': 'in json'}

def test_empty_creds(app):
    with app.app_context():
        doc = render_tabbed_page(provider=None, filename=None, creds={ "S3": [], "AZ": [], "GS": []})
        assert "<h1>You will need to import some credentials to get started.</h1>" in doc

def test_first_empty_creds(app):
    with app.app_context():
        doc = render_tabbed_page(provider="AZ", filename="file1", creds={ "S3": [], "AZ": ["file1"], "GS": ["file2"]})
        assert "Provider is AZ" in doc
        assert "Filename is file1" in doc

def test_second_empty_creds(app):
    with app.app_context():
        doc = render_tabbed_page(provider="S3", filename="file1", creds={ "S3": ["file1"], "AZ": [], "GS": ["file2"]})
        assert "Provider is S3" in doc
        assert "Filename is file1" in doc

def test_tabbed_content_method(app):
    with app.app_context():
        doc = render_tabbed_content(provider="S3", file="file1")
        assert "Provider is S3" in doc
        assert "Filename is file1" in doc