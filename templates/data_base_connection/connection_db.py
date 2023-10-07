import time
import mysql.connector
from mysql.connector import Error
from templates.lb.data_class_music import MusicEntry
# importo tqdm para realizar un progressbar ya que cuando se crea la tabla queda bonito
from tqdm import tqdm
from typing import List
from templates.request_music import MusicFromWeb


class DataBaseMusic:
    def __init__(self):
        self.conn: mysql = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="ejercicio5py"
        )

    def get_conncetion(self):
        try:
            if self.conn.is_connected():
                print("Conexión exitosa")
                info_server = self.conn.get_server_info()
                print("Información del servidor:", info_server)
                # Comprobacion de que la taba exista
                cursor = self.conn.cursor()
                cursor.execute("SHOW TABLES LIKE 'musica'")
                rsult = cursor.fetchone()
                if rsult:
                    print("La tabla 'musica' ya existe")
                else:
                    print("La tabla 'musica' no existe. Creando tabla....")
                    for _ in tqdm(range(50), desc="Creando tabla 'musica'", unit="iter"):
                        time.sleep(0.1)
                    self.create_table_musica()

        except Error as ex:
            print("Error a la hora de realizar la conexion con bases de datos : {0}".format(ex))
            return None

    def close_connection(self):
        if self.conn.is_connected():
            self.conn.close()
            print("Conexión cerrada")

    def create_table_musica(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS musica (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        tema VARCHAR(255),
                        interprete VARCHAR(255),
                        ano INT,
                        semanas INT,
                        pais VARCHAR(255),
                        idiomas VARCHAR(255),
                        continentes VARCHAR(255)
                    )
                ''')
            print("\nTabla 'musica' creada exitosamente.\n")

            # Count all records in the table
            cursor.execute('SELECT COUNT(*) FROM musica')
            total_records = cursor.fetchone()[0]
            print(f'Total records in musica table: {total_records}')

            # Count distinct values in the 'semanas' column
            cursor.execute('SELECT COUNT(DISTINCT semanas) FROM musica')
            distinct_semanas = cursor.fetchone()[0]
            print(f'Distinct semanas in musica table: {distinct_semanas}')

            # Update 'ano' for entries with 52 semanas
            cursor.execute('UPDATE musica SET ano = ano + 1 WHERE semanas = 52')
            print("Se ha actualizado el año para las canciones con 52 semanas.")
            self.conn.commit()

        except Error as ex:
            print("Error al crear la tabla:", ex)

    def insert_data(self, data: List[MusicEntry]):
        try:
            cursor = self.conn.cursor()

            # Check for existing data based on tema and interprete
            for entry in data:
                cursor.execute('SELECT COUNT(*) FROM musica WHERE tema=%s AND interprete=%s',
                               (entry.tema, entry.interprete))
                existing_count = cursor.fetchone()[0]

                if existing_count == 0:
                    cursor.execute(''' 
                        INSERT INTO musica 
                        (`tema`, `interprete`, `ano`, `semanas`, `pais`, `idiomas`,`continentes`) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        entry.tema, entry.interprete, entry.ano, entry.semanas, entry.pais,entry.idiomas, entry.continent))
                    print(f'Data inserted for {entry.tema} by {entry.interprete}')
                else:
                    print(f'Data already exists for {entry.tema} by {entry.interprete}')

            self.conn.commit()
            print("Datos insertados exitosamente.")
        except Error as ex:
            print("Error al introducir los datos: ", ex)
    def get_data_sql(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM musica')
            count = cursor.fetchone()[0]
            print(f'Total rows in musica table: {count}')
            return count
        except Error as ex:
            print("Error: ", ex)
            return None

    def get_artist(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT `interprete`, COUNT(`interprete`) AS `count` FROM `musica` GROUP BY `interprete` HAVING COUNT(`interprete`) > 1")
            return cursor.fetchall()  # Fetch all results
        except Exception as e:
            print("Error:", e)
            return None

    def get_old_song(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT * FROM `musica` ORDER BY `ano` ASC LIMIT 1"
            )
            return cursor.fetchall()
        except Exception as e:
            print("Error: ",e)
            return None
# Inside main_db()
def main_db():
    m = MusicFromWeb()
    data_content = m.get_info()
    if data_content:
        d = DataBaseMusic()
        d.get_conncetion()
        d.insert_data(data_content)
        d.get_data_sql()
        cancion_vieja = d.get_old_song()
        if cancion_vieja:
            for cancion in cancion_vieja:
                print("¿Cuál es la canción más antigua de la lista?")
                print(f"La cancion mas antigua fue en el año {cancion[3]}, nombre de la cancion es: {cancion[1]}"
                      f", y los artistas son {cancion[2]}")
        artists = d.get_artist()
        if artists:
            print("Artist information:")
            for artist in artists:
                print("¿Qué artista aparece más veces en esta lista?")
                print(f"El/la artista: {artist[0]}, se repite: {artist[1]}")

        d.close_connection()
    else:
        print("No se pudo obtener datos de la web.")