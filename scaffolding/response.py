# -*- coding: utf-8 -*-
from .helpers import get_status


class Response(object):
    """Simple response object for use with WSGI applications"""

    def __init__(self):
        self.mimetype = None
        self.status_code = None
        self.charset = None
        self.headers = {}
        self.body = None

    def set_headers(self, headers):
        """Update `self.headers` with the provided `headers`.

        :param headers: A dictionary of headers
        """
        if not isinstance(headers, dict):
            raise TypeError('Expected a dict instead got %s' % type(headers))
        self.headers.update(headers)

    def set_response(self, body, status_code=200, mimetype='text/plain',
                     charset='utf-8'):
        """Set the response body and optionally status_code and charset.
        Attempt to coerce unicode to byte string.

        :param body: Response body to send
        :param status_code: Status code
        :param mimetype: The media type
        :param charset: The character encoding for the response body
        """
        if isinstance(body, unicode):
                body = body.encode('utf-8')
        if not isinstance(body, str):
            raise 'Expected byte string, instead got %s' % type(body)
        self.body = body
        self.status_code = status_code
        self.mimetype = mimetype
        self.charset = charset

    def redirect_for(self, location, body='', status_code=303,
                     mimetype='text/plain', charset='utf-8'):
        """Convenience method for redirecting requests

        :param location: Location to redirect to. This can be a local path or
                         the url to an exteternal resource
        :param body: Response body to send
        :param status_code: Status code
        :param mimetype: The media type
        :param charset: The character encoding for the response body
        """
        self.set_headers({'Location': location})
        self.set_response(body, status_code)

    def _build_headers(self):
        """Turn the headers dictionary into a what WSGI server will expect

        :returns: list of `(header, value)` tuples
        """
        headers = []
        # Add some default headers in
        if self.mimetype is not None:
            self.set_headers({'Content-Type': self.mimetype})
        if self.body is not None:
            self.set_headers({'Content-Length': str(len(self.body))})

        for k, v in self.headers.iteritems():
            if k.lower() == 'content-type' and self.charset is not None:
                v += '; charset=%s' % self.charset
            headers.append((k, v))
        return headers

    def _dump_response(self):
        """Everything needed to create a response.

        :returns: tuple of status msg, headers, and body
        """
        if self.body is not None:
            body = self.body
        else:
            body = ''
        status = get_status(self.status_code)
        headers = self._build_headers()
        return status, headers, body
