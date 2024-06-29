# wait_for_mysql.py
import time
import pymysql

while True:
    try:
        connection = pymysql.connect(
                        host='mysql',
                        port=3306,
                        user='developer',
                        password='html4826',
                        db='pokemon_data'
        )
        connection.close()
        print("MySQL server is ready!")
        break
    except pymysql.err.OperationalError as e:
        print(f"Waiting for MySQL server to be ready... OperationalError: {e}")
        time.sleep(5)
    except pymysql.err.InternalError as e:
        print(f"Waiting for MySQL server to be ready... InternalError: {e}")
        time.sleep(5)
    except pymysql.MySQLError as e:
        print(f"Waiting for MySQL server to be ready... MySQLError: {e}")
        time.sleep(5)
    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(5)