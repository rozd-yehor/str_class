import pytest
from test_task19.app.application import Application


@pytest.fixture
def app(request):
    app = Application()
    request.addfinalizer(app.quit)
    return app
