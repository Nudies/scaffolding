# Scaffolding
### What is it?
Scaffolding is a ultra minimal framework, supporting the WSGI protocol, for bulding web application in python.

### Why?
Mostly an attempt/reason to learn more about python webframeworks and the WSGI protocol.

### Do you really expect people to use it?
No. In fact you really shouldn't use it as it doesn't provide much of anything ATM.

### Planned additions
- Request and Response objects
- Cookie handling

### How do I use it?
```python
from scaffolding import Scaffold

# debug param sets a `/debug/` route for inspecting the environ dict
app = Scaffold(debug=True)

@app.route('/')
def home(env):
  return 'Hello world!'


if __name__ == '__main__':
  from wsgired.simple_server import make_server

  httpd = make_server('', 8000, app)
  http.serve_forever()
```
To see how to serve static html pages checkout the [example app](https://github.com/Nudies/scaffolding/blob/master/example/example_app.py) in `example/`.


### It kinda looks like flask...
It was inspired by flask, but there are plans to register routes in otherways than just a decorator.
