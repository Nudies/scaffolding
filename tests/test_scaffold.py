# -*- coding: utf-8 -*-
import os
import tempfile

import pytest

from scaffolding.core import Scaffold


@pytest.fixture
def app():
    return Scaffold()


@pytest.fixture
def tempdir():
    return tempfile.mkdtemp()


def mock_func(*args, **kwargs):
    pass


def test_can_call_app(app):
    response = app({'PATH_INFO': '/'}, mock_func)
    assert isinstance(response, list)
    assert response[0] == '404 Not Found'


def test_can_register_routes(app):
    @app.route('/foo/')
    def foo(env, res):
        return 'foo'

    response = app({'PATH_INFO': '/foo/'}, mock_func)
    assert response[0] == 'foo'


def test_bad_route_returns_404(app):
    response = app({'PATH_INFO': '/baz/'}, mock_func)
    assert response[0] == '404 Not Found'


def test_no_status_code_returns_500(app):
    @app.route('/foo/')
    def foo(env, res):
        return res.set_response('Hello', status_code=None)

    response = app({'PATH_INFO': '/foo/'}, mock_func)
    assert response[0] == '500 Server Error'


def test_can_set_debug():
    app = Scaffold(debug=True)
    response = app({'PATH_INFO': '/debug/'}, mock_func)
    assert response[0] == 'PATH_INFO: /debug/'


def test_set_staticdir(app, tempdir):
    try:
        with pytest.raises(IOError) as exc_info:
            app.set_staticdir('/not/a/dir')
        assert '/not/a/dir' in str(exc_info.value)
        app.set_staticdir(tempdir)
        assert app.staticdir == tempdir
    finally:
        os.rmdir(tempdir)


def test_can_serve_static(app, tempdir):
    try:
        app.set_staticdir(tempdir)
        htmlfile = os.path.join(tempdir, 'index.html')
        with open(htmlfile, 'w') as f:
            f.write('<h1>Hello World!</h1>')

        @app.route('/')
        def home(env, res):
            return app.serve_static(htmlfile, mimetype='text/html')

        response = app({'PATH_INFO': '/'}, mock_func)
        assert response[0] == '<h1>Hello World!</h1>'
    finally:
        os.remove(htmlfile)
        os.rmdir(tempdir)
