from flask import Flask
from flask import render_template
import os
import sys

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template('index.html', title="title")
