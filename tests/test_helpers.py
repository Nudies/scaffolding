# -*- coding: utf-8 -*-
import pytest

from scaffolding.helpers import fix_path, get_status


def test_fix_path():
    assert fix_path('/foo') == '/foo/'
    assert fix_path('/foo/') == '/foo/'
    assert fix_path('/foo/bar') == '/foo/bar/'


def test_get_status():
    assert get_status(100) == '100 Continue'
    assert get_status(999) == '999'
    with pytest.raises(ValueError) as exc_info:
        get_status('foo')
    assert 'Expected int' in str(exc_info.value)
