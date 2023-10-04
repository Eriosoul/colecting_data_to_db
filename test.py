import requests
from requests import Response
from bs4 import BeautifulSoup
from templates.lb.data_class_music import MusicEntry

class MusicFromWeb:
    def __init__(self):
        self.url = 'https://es.wikipedia.org/wiki/Anexo:Sencillos_n%C3%BAmero_uno_en_Espa%C3%B1a#Canciones_con_m%C3%A1s_semanas_en_el_n%C3%BAmero_uno'

    def extract_country(self, column):
        # Find the appropriate <a> element for the country
        country_link = column.find('a', {'title': True})
        country = None
        if country_link:
            country = country_link.get('title')
            # Extract the country name after the last '/'
            country = country.split('/')[-1].replace('_', ' ')
            # Remove 'Bandera de' prefix if present
            country = country.replace('Bandera de ', '').replace('Bandera del ', '')
        return country or ''


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
                    country = self.extract_country(columns[4])
                    continent = self.get_geography(country)
                    info_content = MusicEntry(
                        tema=columns[0].text.strip(),
                        interprete=columns[1].text.strip(),
                        ano=columns[2].text.strip(),
                        semanas=columns[3].text.strip(),
                        pais=country,
                        continent=continent,
                        idiomas=""
                    )
                    data_content.append(info_content)
            return data_content
        except Exception as e:
            print(f"Error al realizar la conexion con el servidor: {e}")
            return None

    def get_geography(self, country):
        continents = ["Europa", "Asia", "África", "América del Norte", "América del Sur", "Oceanía"]

        formatted_pais = country.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace(
            "ú", "u")
        formatted_pais = "_".join(formatted_pais.split())

        # Special case for "Reino Unido"
        if formatted_pais == "Reino_Unido":
            self.geography = 'https://es.wikipedia.org/wiki/Geografia_del_'
        elif formatted_pais == "Canada":
            self.geography = 'https://es.wikipedia.org/wiki/Geografia_de_'
        else:
            self.geography = 'https://es.wikipedia.org/wiki/Geografia_de_'

        link_geography = self.geography + formatted_pais
        try:
            r: Response = requests.get(link_geography)
            if r.status_code != 200:
                print("No se pudo conectar con el servidor")
                return None

            soup: BeautifulSoup = BeautifulSoup(r.content, "html.parser")
            infobox_tables = soup.find_all("table", class_="infobox")

            if infobox_tables:
                first_infobox = infobox_tables[0]
                for continent in continents:
                    title_element = first_infobox.find("a", title=continent)
                    if title_element:
                        # Return the continent
                        return title_element.text

                # Return None if continent is not found
                return None
            else:
                print("No infobox table found for", country)
                return None

        except Exception as e:
            print("Error con el servidor", e)
            return None

    def get_langue(self, langue):
        continents = ["Europa", "Asia", "África", "América del Norte", "América del Sur", "Oceanía"]

        formatted_pais = langue.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace(
            "ú", "u")
        formatted_pais = "_".join(formatted_pais.split())

        # Special case for "Reino Unido"
        if formatted_pais == "Reino_Unido":
            self.geography = 'https://es.wikipedia.org/wiki/Geografia_del_'
        elif formatted_pais == "Canada":
            self.geography = 'https://es.wikipedia.org/wiki/Geografia_de_'
        else:
            self.geography = 'https://es.wikipedia.org/wiki/Geografia_de_'

        link_geography = self.geography + formatted_pais
        try:
            r: Response = requests.get(link_geography)
            if r.status_code != 200:
                print("No se pudo conectar con el servidor")
                return None

            soup: BeautifulSoup = BeautifulSoup(r.content, "html.parser")
            infobox_tables = soup.find_all("table", class_="infobox")

            if infobox_tables:
                first_infobox = infobox_tables[0]
                for continent in continents:
                    title_element = first_infobox.find("a", title=continent)
                    if title_element:
                        # Return the continent
                        return title_element.text

                # Return None if continent is not found
                return None
            else:
                print("No infobox table found for", langue)
                return None

        except Exception as e:
            print("Error con el servidor", e)
            return None

def main_request():
    m: MusicFromWeb = MusicFromWeb()

    data_content = m.get_info()
    print(data_content)
    if data_content:
        for data in data_content:
            print(f"Tema: {data.tema}, Intérprete: {data.interprete}, "
                  f"Año: {data.ano}, Semanas: {data.semanas}, País: {data.pais}, "
                  f"Continente: {data.continent}")
main_request()
