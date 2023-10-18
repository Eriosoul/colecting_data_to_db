import re
import time

import requests
from tqdm import tqdm
from requests import Response
from bs4 import BeautifulSoup
from templates.lb.data_class_music import MusicEntry

class MusicFromWeb:
    def __init__(self):
        self.url = 'https://es.wikipedia.org/wiki/Anexo:Sencillos_n%C3%BAmero_uno_en_Espa%C3%B1a#Canciones_con_m%C3%A1s_semanas_en_el_n%C3%BAmero_uno'
        self.valid_language = ['español', 'inglés', 'alemán', 'sueco', 'portugués', 'francés']
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

    def extract_language(self, country):
        self.generate_link = 'https://es.wikipedia.org/wiki/' + country
        try:
            r: Response = requests.get(self.generate_link)
            if r.status_code != 200:
                print(f"No se pudo conectar con el servidor para {country}")
                return None

            soup: BeautifulSoup = BeautifulSoup(r.content, "html.parser")
            language_elements = soup.find_all("a", href="/wiki/Idioma_oficial")

            if language_elements:
                languages = []
                for element in language_elements:
                    language_text = element.find_next('td').text.strip()
                    match = re.search(r'(\b\w+\b)', language_text)
                    if match:
                        language_text = match.group(1).lower()

                        # Handle specific cases for language mapping
                        language_mapping = {
                            'castellano': 'español',
                            'spanish': 'español',
                            'español': 'español',
                            'ninguno': 'inglés'
                        }

                        language_text = language_mapping.get(language_text, language_text)

                        # Check if the language is valid
                        if language_text in self.valid_language:
                            languages.append(language_text)

                return languages if languages else None
            else:
                print(f"No se encontró información de idiomas oficiales para {country}")
                return None

        except Exception as e:
            print(f"Error al obtener información para {country}: {str(e)}")
            return None

    def get_langue(self, country_list):
        self.generate_link = 'https://es.wikipedia.org/wiki/'
        for country in country_list:
            formatted_country = "_".join(country.split())
            link_langue = self.generate_link + formatted_country
            # print(link_langue)
            try:
                r: Response = requests.get(link_langue)
                if r.status_code != 200:
                    print("No se pudo conectar con el servidor")
                    return None

                soup: BeautifulSoup = BeautifulSoup(r.content, "html.parser")
                language = self.extract_language(soup)

                if language:
                    print(f"Idiomas oficiales para {country}: {language}")
                else:
                    print(f"No se encontró información de idiomas oficiales para {country}")

            except Exception as e:
                print(f"Error al obtener información para {country}: {str(e)}")
                return None

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
                    idiomas = self.extract_language(country)
                    idiomas_str = ", ".join(idiomas) if idiomas else ''
                    info_content = MusicEntry(
                        tema=columns[0].text.strip(),
                        interprete=columns[1].text.strip(),
                        ano=columns[2].text.strip(),
                        semanas=columns[3].text.strip(),
                        pais=country,
                        continent=continent,
                        idiomas=idiomas_str
                    )
                    # print(info_content)
                    data_content.append(info_content)
            return data_content
        except Exception as e:
            print(f"Error al realizar la conexion con el servidor: {e}")
            return None

    def get_geography(self, country):
        continents = ["Europa", "Asia", "África", "América del Norte", "América del Sur", "Oceanía"]
        # Define a mapping of countries to continents
        country_to_continent = {
            "Venezuela": "América del Sur",
            "Estados Unidos": "América del Norte",
            "Canadá": "América del Norte",
            "Cuba": "América Central"
            # Add more mappings as needed
        }

        # Try to directly map the country to a continent
        if country in country_to_continent:
            return country_to_continent[country]

        formatted_pais = country.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace(
            "ú", "u")
        formatted_pais = "_".join(formatted_pais.split())

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
                        return title_element.text

                return None
            else:
                print("No infobox table found for", country)
                return None

        except Exception as e:
            print("Error con el servidor", e)
            return None


def main_request():
    m: MusicFromWeb = MusicFromWeb()
    data_content = m.get_info()
    for _ in tqdm(range(50), desc="Obteniendo datos de la web ...", unit="iter"):
        time.sleep(0.5)
        # print(data_content)
    if data_content:
        print("Imprimi las cosas")
        for data in data_content:
            print(f"Tema: {data.tema}, Intérprete: {data.interprete}, "
                  f"Año: {data.ano}, Semanas: {data.semanas}, País: {data.pais}, "
                  f"Continente: {data.continent}, Idioma: {data.idiomas}")

main_request()
