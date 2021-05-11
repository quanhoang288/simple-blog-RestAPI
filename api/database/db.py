from mysql.connector import connect, Error
import configparser


class DatabaseAdapter:
    def __init__(self): 
        self.connect()
    def connect(self):
        config = configparser.ConfigParser()
        config.read('database/config.ini')
        db_config = {
            'host': config['mysql']['host'],
            'user': config['mysql']['user'],
            'password': config['mysql']['password'],
            'database': config['mysql']['database']
        }
        self.conn = connect(**db_config)
        self.cursor = self.conn.cursor(dictionary=True)
    def execute(self, query, params=None, commit=False):
        try:
            self.cursor.execute(query, params)
            if commit: 
                self.conn.commit()
                return True
            return self.cursor.fetchall()
        except Error as err: 
            return False
    def get_lastrowid(self):
        return self.cursor.lastrowid
    def close_connection(self):
        self.cursor.close()
        self.conn.close()

