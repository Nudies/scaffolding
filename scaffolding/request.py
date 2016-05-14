# -*- coding: utf-8 -*-


class Request(object):

    def __init__(self, environ):
        self.method = None
        self.headers = None
        self.params = None
        self.body = None

        self._parse_environ(environ)

    def _parse_environ(self, environ):
        """Parse a environ dict and set the request objects state

        :param environ: Environ dict
        """
        pass
