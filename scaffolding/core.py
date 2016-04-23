# -*- coding: utf-8 -*-
import os
from functools import wraps

from .helpers import fix_path


class Scaffold(object):
    """Ultra minimal wsgi framework for building python web apps

    :param debug: If this is enabled the /debug/ path will display the environ
                  variables
    """

    def __init__(self, debug=False):
        self.mimetype = 'text/plain'
        self.staticdir = None
        self.routes = {}
        self.debug = debug

    def set_staticdir(self, dir):
        """Setup a staticdir for serving static files

        :param dir: Static directory
        """
        if os.path.isdir(dir):
            self.staticdir = dir
        else:
            raise IOError('%s is not a directory' % dir)

    def route(self, path):
        """Register routes with the framework. Usage looks something like this:

            @app.route('/foo/bar/')
            def bar(environ):
                response = 'Hello World!'
                return response

        :param path: The routing path to associate with a function
        """
        def establish_route(fun):
            self.routes[fix_path(path)] = fun
            @wraps(fun)
            def wrapper(*args, **kwargs):
                # In case the function is invoked by the user don't break the
                # world
                return None
            return wraps
        return establish_route

    def serve_static(self, file, mime='text/html'):
        """Used to serve static, often html files.

        :param file: File found in the `staticdir` location
        :param mime: mime type for the file, default is text/html
        :returns: HTTP response body
        """
        self.mimetype = mime
        response = []
        with open(os.path.join(self.staticdir, file), 'r') as f:
            for line in f:
                response.append(line)
        return ''.join(response)

    def app(self, environ, start_response):
        """Pull everything together

        :param environ: Dict of environment variables, this is provided by the
                        gateway server.
        :param start_response: Callable with the signature `status`,
                               `response_headers`, and `exc_info=None`
        :returns: HTTP response body
        """
        path = fix_path(environ['PATH_INFO'])
        response = None

        def debug(env):
            self.mimetype = 'text/plain'
            resp = ['%s: %s' % (k, v) for k, v in env.iteritems()]
            return '\n'.join(resp)

        # Setup debuging route
        if self.debug:
            self.routes['/debug/'] = debug

        # Try to resolve a requested path
        if self.routes.get(path, False):
            response = self.routes[path](environ)

        if response is not None:
            status = '200 OK'
        else:
            status = '404 Not Found'
            response = '404 Not Found'

        # Setup our headers
        headers = [
                ('Content-Type', self.mimetype),
                ('Content-Length', str(len(response)))
            ]

        start_response(status, headers)
        return [response]

    def __call__(self, environ, start_response):
        """Adhear to the WSGI standard of providing an invocable"""
        return self.app(environ, start_response)
