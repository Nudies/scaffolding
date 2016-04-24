# -*- coding: utf-8 -*-
import os
from functools import wraps

from .helpers import fix_path
from .response import Response


class Scaffold(object):
    """Ultra minimal wsgi framework for building python web apps

    :param debug: If this is enabled the /debug/ path will display the environ
                  variables
    """

    def __init__(self, debug=False):
        self.staticdir = None
        self.routes = {}
        self.debug = debug
        self.response = None

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

    def serve_static(self, file, status_code=200, mimetype='text/html'):
        """Used to serve static files, it really just a convenince wrappper
        for `Response.set_response`

        :param file: File found in the `staticdir` location
        :param mime: mime type for the file, default is text/html
        :returns: HTTP response body
        """
        body = []
        with open(os.path.join(self.staticdir, file), 'r') as f:
            for line in f:
                body.append(line)

        self.response.set_response(''.join(body), status_code, mimetype)

    def app(self, environ, start_response):
        """Pull everything together

        :param environ: Dict of environment variables, this is provided by the
                        gateway server.
        :param start_response: Callable with the signature `status`,
                               `response_headers`, and `exc_info=None`
        :returns: HTTP response body
        """
        path = fix_path(environ['PATH_INFO'])

        def debug(env, res):
            resp = ['%s: %s' % (k, v) for k, v in env.iteritems()]
            return self.response.set_response('\n'.join(resp), 200, 'text/plain')

        # Setup debuging route
        if self.debug:
            self.routes['/debug/'] = debug

        # Try to resolve a requested path
        if self.routes.get(path, False):
            # Normaly this is none, unless the route returns a string then it
            # should be used as the response body, everything else ignore.
            res = self.routes[path](environ, self.response)
            if res is not None and isinstance(res, str):
                self.response.set_response(res)

        # User created a route, but didn't return a valid response
        if self.response.status_code is None and self.routes.get(path, False):
            self.response.set_response('500 Server Error', 500)
        # There is no route for the request
        if self.response.status_code is None:
            self.response.set_response('404 Not Found', 404)

        status, headers, body = self.response._dump_response()
        start_response(status, headers)
        return [body]

    def __call__(self, environ, start_response):
        """Adhear to the WSGI standard of providing an invocable"""
        self.response = Response()
        return self.app(environ, start_response)
