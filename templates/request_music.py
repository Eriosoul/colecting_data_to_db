import requests
from requests import Response
from bs4 import BeautifulSoup
from templates.lb.data_class_music import MusicEntry


class MusicFromWeb:
    def __init__(self):
        self.url = 'https://es.wikipedia.org/wiki/Anexo:Sencillos_n%C3%BAmero_uno_en_Espa%C3%B1a#Canciones_con_m%C3%A1s_semanas_en_el_n%C3%BAmero_uno'

    def get_info(self):
        try:
            r: Response = requests.get(self.url)
            if r.status_code != 200:
                return r.status_code
            soup: BeautifulSoup = BeautifulSoup(r.content, 'html.parser')
            content = soup.find_all("table")[1]
            rows = content.find_all("tr")[1:]

            data_content: list = []
            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 5:
                    info_content = MusicEntry(
                        tema=columns[0].text.strip(),
                        interprete=columns[1].text.strip(),
                        ano=columns[2].text.strip(),
                        semanas=columns[3].text.strip(),
                        pais=columns[4].text.strip()
                    )
                    data_content.append(info_content)

            return data_content
        except Exception as e:
            print(f"Error al realizar la conexion con el servidor: {e}")
            return None


def main_request():
    m: MusicFromWeb = MusicFromWeb()
    data_content = m.get_info()
    print(data_content)
    if data_content:
        for data in data_content:
            print(f"Tema: {data.tema}, Intérprete: {data.interprete}, "
                  f"Año: {data.ano}, Semanas: {data.semanas}, País: {data.pais}")


main_request()
