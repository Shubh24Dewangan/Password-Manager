import mysql.connector as mycon
from config import DB_host, DB_user, DB_passwd, DB_name

class Database:
    def __init__(self):
        self.conn = mycon.connect (
            host = DB_host,
            user = DB_user,
            password = DB_passwd,
            database = DB_name
        )

        self.cursor = self.conn.cursor()

    def execute(self, query, inp = None):
        self.cursor.execute(query, inp or ())
        if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
            self.conn.commit()
        return self.cursor
    
    def close(self):
        self.cursor.close()
        self.conn.close()

    #------ USER METHODS ------

    def get_user(self, username):
        cur = self.execute('SELECT * FROM users WHERE username = %s', (username,))
        return cur.fetchone()

    def add_user(self, username, master_hash):
        self.execute('INSERT INTO users (username, master_hash) VALUES (%s, %s)', (username, master_hash))

    def delete_user(self, username, master_hash):
        self.execute('DELETE FROM users WHERE username = %s and master_hash = %s', (username, master_hash))

    def add_vault(self, user_id, site,  pass_encrypted, login_user=' '):
        self.execute('INSERT INTO vault (user_id, site_name, login_username, password_encrypted) VALUES (%s, %s, %s, %s)', (user_id, site, login_user, pass_encrypted))

    def get_vault(self, user_id):
        cur = self.execute('SELECT site_name, login_username, password_encrypted FROM vault WHERE user_id = %s', (user_id,))
        return cur.fetchall()
    
    def delete_vault(self, user_id, site):
        cur = self.execute('DELETE FROM vault WHERE user_id = %s and site_name = %s', (user_id, site))
        return cur.rowcount()
