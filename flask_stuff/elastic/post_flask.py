#!/usr/bin/env python3 


from flask import Flask, request, abort
import json


app = Flask(__name__)

@app.route("/")
def hello():
    return "Server: %s, Tags: %s, message=%s\n" % (request.args.get('server'), request.args.get('tags'), request.args.get('message'))

@app.route("/data", methods=['POST'])
def data():
    if not request.json:
        abort(400)
    print(request.json)
    return json.dumps(request.json)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
