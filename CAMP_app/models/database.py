import mysql.connector
from mysql.connector import Error, pooling

class Database:
    def __init__(self):
        try:
            self.db_pool = pooling.MySQLConnectionPool(
                pool_name="my_pool",
                pool_size=5,
                host="localhost",
                user="root",
                password="1234",
                database="db_camp"
            )
        except Error as e:
            print(e)

    def get_connection(self):
        try:
            connection = self.db_pool.get_connection()
            if connection.is_connected():
                return connection
        except Error as e:
            print(e)