# -*- coding: utf-8 -*-
import pytest

from scaffolding.response import Response


@pytest.fixture
def res():
    return Response()


def test_can_set_headers(res):
    headers = {
        'Content-Length': '0',
        'Content-Type': 'text/plain',
        'X-XSS-Protection': '1; mode=block'
    }
    res.set_headers(headers)
    assert res.headers == headers
    with pytest.raises(ValueError) as exc_info:
        res.set_headers(['Content-Length', '22'])
    assert 'Expected a dict' in str(exc_info.value)


def test_can_set_response(res):
    res.set_response(u'<b>Hello World!</b>', mimetype='text/html')
    assert isinstance(res.body, str)
    assert res.body == '<b>Hello World!</b>'
    assert res.status_code == 200
    assert res.mimetype == 'text/html'
    res.set_response('No such page!', 404)
    assert res.status_code == 404
    assert res.mimetype == 'text/plain'


def test_can_build_headers(res):
    res.set_response('foo')
    headers = res._build_headers()
    # Make sure some defaults are provided
    assert isinstance(headers, list)
    for header in headers:
        if header[0] == 'Content-type':
            assert header[1] == 'text/plain; charset=utf-8'


def test_dump_response(res):
    res.status_code = 200
    status, headers, body = res._dump_response()
    assert isinstance(status, str)
    assert '200 OK' in status
    assert isinstance(headers, list)
    assert isinstance(body, str)
