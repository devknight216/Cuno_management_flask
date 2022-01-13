# Following the guide at https://pytest-flask.readthedocs.io/en/latest/tutorial.html
# combined with https://flask.palletsprojects.com/en/2.0.x/testing/

# import os
# import tempfile
import pytest 

from flask_app import create_app
import config 

@pytest.fixture
def app():
    test_config = config.DebugConfig()
    test_config.update(
        TESTING=True
    )
    return create_app(test_config) 

@pytest.fixture
def custom_client():
    # db_fd, db_path = tempfile.mkstemp()
    test_config = config.DebugConfig()
    test_config.update(
        TESTING=True
    )
    app = create_app(test_config)

    with app.test_client() as client:
        with app.app_context():
            pass
            # init_db()
        yield client

    # os.close(db_fd)
    # os.unlink(db_path)
