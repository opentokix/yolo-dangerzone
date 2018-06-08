#!/usr/bin/env python3

from flask import Flask
from flask import jsonify
import random

app = Flask(__name__)

@app.route("/")
def root_route():
    content = """
<html>
<head>
<title>
Flask test server
</title>
<body>
<h1>This is a test api server</h1>
<p>It will return some different return codes and content to test monitoring systems on different urls.</p>
<ul>
"""
    links = []
    for rule in app.url_map.iter_rules():
        content = content + "<li>" + rule.rule
    content = content + "</ul></body></html>"
    return content, 200

@app.route("/hello")
def hello_world():
    return 'Hello world!'

@app.route("/501")
def fiveoone():
    return "501", 501

@app.route("/503")
def fiveothree():
    return "503", 503


@app.route("/403")
def fourothree():
    return "403", 403

@app.route("/404")
def fourofour():
    return "404", 404
    
@app.route("/json")
def return_json():
    a = {'block':
            {'route':'json', 'status': True},
        'info': 'hello world',
        'number': 1234,
        'string': 'This is a string!%¤#"',
        }
    return jsonify(a), 200

@app.route("/random")
def return_random():
    codes = [200, 301, 302, 401, 403, 404, 501, 503 ]
    return "This a random response code!", random.choice(codes)

@app.route("/alwaysok")
def return_randomok():
    codes = []
    for i in range(200,206):
        codes.append(i)
    return "This a random response code, but ok", random.choice(codes)
