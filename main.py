import environ  
env = environ.Env()
env.read_env()

# test comment

import mysql.connector

def test_mysql_connection():
    try:
        # Replace the placeholders with your MySQL server details
        connection = mysql.connector.connect(
            host=env('DB_HOST'),
            port=3306,
            user=env('DB_USER'),
            password=env('DB_PASS'),
            database=env('DB_NAME')
        )

        if connection.is_connected():
            print('Successfully connected to the MySQL server!')
            connection.close()
        else:
            print('Failed to connect to the MySQL server.')

    except mysql.connector.Error as error:
        print('Error connecting to MySQL server:', error)

test_mysql_connection()
