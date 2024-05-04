from flask import Flask, render_template, request
from runner import Runner
import psycopg2

db = psycopg2.connect("")
runner = Runner(db, instance_cap=10)
app = Flask(__name__)

@app.route("/spawn")
def index():

