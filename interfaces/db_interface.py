import psycopg2
from typing import List, Dict

class DB_Interface:
    def __init__(self, **kwargs):
        self.conn = psycopg2.connect(*kwargs, row_factory=psycopg2.row.dict_row)
    
    def get_users(self) -> List[Dict]:
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM users')
        return cur.fetchall()
    
    

    

