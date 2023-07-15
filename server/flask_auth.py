import time
import flask
import datetime
from uuid import uuid4
from hashlib import sha256
from psycopg2 import connection

class AuthenticationManager:
    def __init__(self, conn: connection, uauth_response: flask.Response):
        self.db_conn = conn
        self.uauth_response = uauth_response
    
    def _sha256hash(self, data: str) -> str:
        return sha256(data.encode('UTF-8')).hexdigest()
    
    def create_session(self, uid: str, response: flask.Response) -> flask.Response:
        cur = self.db_conn.cursor()
        token = uuid4()
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=30)
        cur.execute("INSERT INTO sessions VALUES (%s, %s, %s)", (uid, token, int(expire_date)))
        response.set_cookie('auth', token, expires=expire_date)
        return response

    def login(self, username: str, password: str, response: flask.Response) -> flask.Response | None:
        cur = self.db_conn.cursor()
        phash = self._sha256hash(password)
        cur.execute("SELECT * FROM users WHERE username=%s AND hash=%s", (username, phash))
        l = cur.fetchone()
        if l == None:
            return None
        
        cur.execute("SELECT * FROM sessions WHERE id=%s", (l[0],))
        if (l2 := cur.fetchone()) != None:
            if l2[2] < int(time.time()):
                cur.execute('DELETE FROM sessions WHERE id=%s', (l[0],))
            else:
                return None

        return self.create_session(l[0], response)
    
    def check_auth(self) -> bool:
        cur = self.db_conn.cursor()
        if type(token := flask.request.cookies.get('auth')) != str:
            return False
        
        cur.execute("SELECT * FROM sessions WHERE token=%s", (token,))
        l = cur.fetchone()
        if l == None:
            return False
        if l[2] < int(time.time()):
            return False
        
        return True

    def login_required(self, func):
        def inner():
            if not self.check_auth():
                return self.uauth_response()
            func()

        return inner
    



        


        
