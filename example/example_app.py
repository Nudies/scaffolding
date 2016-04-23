# -*- coding: utf-8 -*-
import os
from scaffolding import Scaffold


static_path = os.path.join(os.path.abspath(os.curdir), 'static')
app = Scaffold(debug=True)
app.set_staticdir(static_path)


@app.route('/')
def home(env):
    return app.serve_static('index.html')


@app.route('/bar/')
def bar(env):
    return app.serve_static('bar.html')


@app.route('/foo/')
def foo(env):
    return 'Welcome to the foo page!'


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8000, app)
    print 'Server running on port 8000'
    httpd.serve_forever()
