from mysql.connector import Error
from templates.data_base_connection.connection_db import DataBaseMusic

class CreateTable:
    def __init__(self):
        self.db: DataBaseMusic = DataBaseMusic()

    def create_table_musica(self):
        try:
            cursor = self.db.conn.cursor()
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
            self.db.conn.commit()

        except Error as ex:
            print("Error al crear la tabla:", ex)