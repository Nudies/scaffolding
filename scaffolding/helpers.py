# -*- coding: utf-8 -*-
"""Generic helper functions for the sacffolding framework"""

STATUS_CODES = {
    # 1XX Informational
    100: 'Continue',
    101: 'Switching Protocols',
    102: 'Processing',

    # 2XX Success
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',

    # 3XX Redirection
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    306: '(Unused)',
    307: 'Temporary Redirect',

    # 4XX Client Error
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Rquest Entity Too Large',
    414: 'Request-URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',

    # 5XX Server Error
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported'
}


def fix_path(path):
    """
    Simple function for appending a '/' character on the end of a path if it is
    missing.

    :param path: url path
    :returns: path appended with '/'
    """
    if not path.endswith('/'):
        path += '/'
    return path


def get_status(status_code):
    """Get a status string response given a particular status_code int

    :param status_code: HTTP status code int
    :returns: HTTP status code string
    """
    if not isinstance(status_code, int):
        raise TypeError('Expected int instead got %s' % type(status_code))

    if not STATUS_CODES.get(status_code, False):
        return str(status_code)

    return str(status_code) + ' ' + STATUS_CODES[status_code]
