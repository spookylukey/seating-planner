#!/usr/bin/env python

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
