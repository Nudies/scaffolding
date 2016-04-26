# -*- coding: utf-8 -*-
import os
import random

from scaffolding import Scaffold


app = Scaffold(debug=True)
static_path = os.path.join(os.path.abspath(os.curdir), 'static')
app.set_staticdir(static_path)


@app.route('/')
def home(env, res):
    return app.serve_static('index.html', mimetype='text/html')


@app.route('/upper/')
def to_upper(env, res):
    if env['QUERY_STRING'] is not None:
        for param in env['QUERY_STRING'].split('&'):
            if param.startswith('name='):
                result = param.split('=')[1].upper()
                return res.set_response(result, 200, 'text/plain')
    return res.redirect_for('/')


def rand(env, res):
    return str(random.randrange(1, 11))


# Another way to establish routes instead of with the decorator
app.set_routes({
    '/random/': rand
})


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8000, app)
    print 'Server running on port 8000'
    httpd.serve_forever()
