#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import hashlib
import sqlite3
import sys
from OpenSSL import SSL
from flask import Flask,request
app = Flask(__name__)


def setup_ssl():
    try:
        context = SSL.Context(SSL.SSLv23_METHOD)
        context.use_privatekey_file("ssl/fakeserver.key")
        context.use_certificate_file("ssl/fakeserver.crt")
    except Exception,e:
        print "Something happened in the ssl context, exiting...\nError: %s" % str(e)
        sys.exit(2)
    return context

def read_db(username):
    con = sqlite3.connect('db/main.db')
    try:
        cur = con.cursor()
        query = 'select * from users where username="%s"' % (username)
        cur.execute(query)
        answer = cur.fetchone()
        if len(answer) == 0:
            return False
        else:
            return answer
        return cur.fetchone()
    except:
        return False
    finally:
        con.close()


def check_password(password, hashstring):
    hash_object = hashlib.sha256(password)
    return hash_object.hexdigest() in hashstring


@app.route("/")
def hello():
    return "Hello World"


@app.route("/api", methods=['POST'])
def api():
    name=request.form['user']
    password=request.form['pass']
    db_data = read_db(name)
    if db_data is False:
        return "Unauthorized"
    print db_data
    if name in db_data[0]:
        print check_password(password, db_data[1])
        if check_password(password, db_data[1]) is True:
            uid = db_data[2]
            del password
            del db_data
            return "Hello %s, you are authorized and have uid: %d" % (name, uid)
        else:
            return "Wrong password"
def main():
    ssl = setup_ssl()
    app.run(host='::', ssl_context=ssl)

if __name__ == '__main__':
    main()
