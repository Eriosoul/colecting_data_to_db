import time
from templates.data_base_connection.connection_db import main_db

def main():
    try:
        main_db()
        print("\n Realizando insercion a db \n")

        time.sleep(0.5)
    except Exception as e:
        print("Error", e)

if __name__ == '__main__':
    main()
