# -*- coding: utf-8 -*-
import os
from scaffolding import Scaffold


static_path = os.path.join(os.path.abspath(os.curdir), 'static')
app = Scaffold(debug=True)
app.set_staticdir(static_path)


@app.route('/')
def home(env, res):
    return app.serve_static('index.html', mimetype='text/html')


@app.route('/foo/')
def foo(env, res):
    return 'Welcome to the foo page!'


@app.route('/bar/')
def bar(env, res):
    return app.serve_static('bar.html', mimetype='text/html')


@app.route('/baz/')
def baz(env, res):
    params = env.get('QUERY_STRING', False)
    if not params:
        res.set_headers({'Location': 'https://github.com/Nudies/scaffolding'})
        return res.set_response('Such redirect', 307)
    return res.set_response('%s' % params, 200)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8000, app)
    print 'Server running on port 8000'
    httpd.serve_forever()
