from flask import Flask, request, render_template, redirect
import psycopg2
import flask_auth

conn = psycopg2.connect()
app = Flask(__name__)
auth = flask_auth.AuthenticationManager(conn, redirect('/login'))


@app.route("/login")
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    auth.login()

        

