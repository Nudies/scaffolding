# -*- coding: utf-8 -*-
from scaffolding.helpers import fix_path


def test_fix_path():
    assert '/foo/' == fix_path('/foo')
    assert '/foo/' == fix_path('/foo/')
    assert '/foo/bar/' == fix_path('/foo/bar')
