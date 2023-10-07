
import time
from tqdm import tqdm
from templates.data_base_connection.connection_db import main_db


def cls():
    print('\n' * 20)


def main():
    try:
        main_db()
        # print("Mostrando resultado del request")
        # main_request()
        print("\n realizando insercion a db \n")
        for _ in tqdm(range(50), desc="Cargando Menu", unit="iter"):
            time.sleep(0.1)

        time.sleep(0.5)
        # cls()
    except Exception as e:
        print("Error", e)


if __name__ == '__main__':
    main()
