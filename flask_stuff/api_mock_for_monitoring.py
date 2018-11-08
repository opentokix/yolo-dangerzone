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

@app.route("/html")
def return_html():
    content = """
<!DOCTYPE html>
<html>
	<head>
		<title>Lists, Tables and Forms</title>
		<style type='text/css'>
			body {
				font-family: Arial, Verdana, sans-serif;
				font-size: 90%;
				color: #666666;
				background-color: #f8f8f8;}
			li {
				list-style-image: url('images/icon-plus.png');
				line-height: 1.6em;}
			table {
				border-spacing: 0px;}
			th, td {
				padding: 5px 30px 5px 10px;
				border-spacing: 0px;
				font-size: 90%;
				margin: 0px;}
			th, td {
				text-align: left;
				background-color: #e0e9f0;
				border-top: 1px solid #f1f8fe;
				border-bottom: 1px solid #cbd2d8;
				border-right: 1px solid #cbd2d8;}
			tr.head th {
				color: #fff;
				background-color: #90b4d6;
				border-bottom: 2px solid #547ca0;
				border-right: 1px solid #749abe;
				border-top: 1px solid #90b4d6;
				text-align: center;
				text-shadow: -1px -1px 1px #666666;
				letter-spacing: 0.15em;}
			td {
				text-shadow: 1px 1px 1px #ffffff;}
			tr.even td, tr.even th {
				background-color: #e8eff5;}
			tr.head th:first-child {
				-webkit-border-top-left-radius: 5px;
				-moz-border-radius-topleft: 5px;
				border-top-left-radius: 5px;}
			tr.head th:last-child {
				-webkit-border-top-right-radius: 5px;
				-moz-border-radius-topright: 5px;
				border-top-right-radius: 5px;}
			fieldset {
				width: 310px;
				margin-top: 20px;
				border: 1px solid #d6d6d6;
				background-color: #ffffff;
				line-height: 1.6em;}
			legend {
				font-style: italic;
				color: #666666;}
			input[type='text'] {
				width: 120px;
				border: 1px solid #d6d6d6;
				padding: 2px;
				outline: none;}
			input[type='text']:focus,
			input[type='text']:hover {
				background-color: #d0e2f0;
				border: 1px solid #999999;}
			input[type='submit'] {
				border: 1px solid #006633;
				background-color: #009966;
				color: #ffffff;
				border-radius: 5px;
				padding: 5px;
				margin-top: 10px;}
			input[type='submit']:hover {
				border: 1px solid #006633;
				background-color: #00cc33;
				color: #ffffff;
				cursor: pointer;}
			.title {
				float: left;
				width: 160px;
				clear: left;}
			.submit {
				width: 310px;
				text-align: right;}
		</style>
	</head>
	<body>
		<h1>Poetry Workshops</h1>
		<p>We will be conducting a number of poetry workshops and symposiums throughout the year.</p>
		<p>Please note that the following events are free to members:</p>
		<ul>
			<li>A Poetic Perspective</li>
			<li>Walt Whitman at War</li>
			<li>Found Poems and Outsider Poetry</li>
		</ul>
		<table>
			<tr class='head'>
				<th></th>
				<th>New York</th>
				<th>Chicago</th>
				<th>San Francisco</th>
			</tr>
			<tr>
				<th>A Poetic Perspective</th>
				<td>Sat, 4 Feb 2012<br />11am - 2pm</td>
				<td>Sat, 3 Mar 2012<br />11am - 2pm</td>
				<td>Sat, 17 Mar 2012<br />11am - 2pm</td>
			</tr>
			<tr class='even'>
				<th>Walt Whitman at War</th>
				<td>Sat, 7 Apr 2012<br />11am - 1pm</td>
				<td>Sat, 5 May 2012<br />11am - 1pm</td>
				<td>Sat, 19 May 2012<br />11am - 1pm</td>
			</tr>
			<tr>
				<th>Found Poems &amp; Outsider Poetry</th>
				<td>Sat, 9 Jun 2012<br />11am - 2pm</td>
				<td>Sat, 7 Jul 2012<br />11am - 2pm</td>
				<td>Sat, 21 Jul 2012<br />11am - 2pm</td>
			</tr>
			<tr class='even'>
				<th>Natural Death: An Exploration</th>
				<td>Sat, 4 Aug 2012<br />11am - 4pm</td>
				<td>Sat, 8 Sep 2012<br />11am - 4pm</td>
				<td>Sat, 15 Sep 2012<br />11am - 4pm</td>
			</tr>
		</table>
		<form action='http://www.example.com/form.php' method='get'>
			<fieldset>
				<legend>Register your interest</legend>
				<p><label class='title' for='name'>Your name:</label>
					 <input type='text' name='name' id='name'><br />
					 <label class='title' for='email'>Your email:</label>
					 <input type='text' name='email' id='email'></p>
				<p><label for='location' class='title'>Your closest center:</label>
					 <select name='location' id='location'>
						 <option value='ny'>New York</option>
						 <option value='il'>Chicago</option>
						 <option value='ca'>San Francisco</option>
					 </select></p>
				<span class='title'>Are you a member?</span>
				<label><input type='radio' name='member' value='yes' /> Yes</label>
				<label><input type='radio' name='member' value='no' /> No</label>
			</fieldset>
 	    <div class='submit'><input type='submit' value='Register' /></div>
		</form>
	</body>
</html>
"""
    return content, 200