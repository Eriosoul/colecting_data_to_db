from typing import List
from mysql.connector import Error
from templates.lb.data_class_music import MusicEntry
from templates.data_base_connection.connection_db import DataBaseMusic
class InsertDataDB:
    def __init__(self):
        self.db: DataBaseMusic = DataBaseMusic()
    def insert_data(self, data: List[MusicEntry]):
        try:
            cursor = self.db.conn.cursor()

            # Check for existing data based on tema and interprete
            for entry in data:
                cursor.execute('SELECT COUNT(*) FROM musica WHERE tema=%s AND interprete=%s',
                               (entry.tema, entry.interprete))
                existing_count = cursor.fetchone()[0]

                if existing_count == 0:
                    cursor.execute(''' 
                        INSERT INTO musica 
                        (`tema`, `interprete`, `ano`, `semanas`, `pais`) 
                        VALUES (%s, %s, %s, %s, %s)
                    ''', (entry.tema, entry.interprete, entry.ano, entry.semanas, entry.pais))
                    print(f'Data inserted for {entry.tema} by {entry.interprete}')
                else:
                    print(f'Data already exists for {entry.tema} by {entry.interprete}')

            self.db.conn.commit()
            print("Datos insertados exitosamente.")
        except Error as ex:
            print("Error al introducir los datos: ", ex)