# -*- coding: utf-8 -*-
import os
import re
from functools import wraps

from .helpers import fix_path
from .response import Response


class Router(object):

    PathVarRx = re.compile(r'<(\w+)>')

    def __init__(self):
        self.routes = {}

    def set_routes(self, routes):
        """Establish multiple routes via a dict object where the key is the
        path and the value is the handler.

        :param routes: A dict of paths with handler values
        """
        if not isinstance(routes, dict):
            raise TypeError('Expected dict instead got %s' % type(routes))
        for k, v in routes.iteritems():
            assert hasattr(v, '__call__'), 'Route handler must be callable'
            self.routes[fix_path(k)] = v

    def route(self, path):
        """Register routes via a decorator. Usage looks something like this:

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

    def resolve(self, path):
        """Resolve requests to a specific path and return the callable
        TODO: Add path variable sub

        :param path: The requested path
        """
        handler = self.routes.get(fix_path(path), False)
        if not handler:
            return None
        return handler


class Scaffold(object):
    """Ultra minimal wsgi framework for building python web apps

    :param debug: If this is enabled the /debug/ path will display the environ
                  variables
    """

    def __init__(self, debug=False):
        self.staticdir = None
        self.router = Router()
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

    def route(self, path):
        """Wrapper for the `Router.route`"""
        return self.router.route(path)

    def set_routes(self, routes):
        """Wrapper for the `Router.set_routes`"""
        return self.router.set_routes(routes)

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
            body = ['%s: %s' % (k, v) for k, v in env.iteritems()]
            return res.set_response('\n'.join(body), 200, 'text/plain')

        # Setup debuging route
        if self.debug:
            self.set_routes({'/debug/': debug})

        # Try to resolve a requested path
        if self.router.resolve(path) is not None:
            # Normaly this is none, unless the route returns a string then it
            # should be used as the response body, everything else ignore.
            handler = self.router.resolve(path)
            res = handler(environ, self.response)
            if res is not None and isinstance(res, str):
                self.response.set_response(res)

        # User created a route, but didn't return a valid response
        if self.response.status_code is None and \
                self.router.resolve(path) is not None:
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
