# from typing import List
import requests
from bs4 import BeautifulSoup
from requests import Response

from templates.request_music import MusicFromWeb
# from templates.lb.data_class_music import MusicEntry

class ExtractCountry:
    def __init__(self):
        self.content = MusicFromWeb()
        self.geography = 'https://es.wikipedia.org/wiki/Geografia_de_'

    def get_geography(self):
        data_content = self.content.data_content  # Access the data_content
        link_data: list = []
        for music_entry in data_content:
            formatted_pais = music_entry.pais.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace(
                "ú", "u")
            formatted_pais = "_".join(formatted_pais.split())
            if formatted_pais == "Reino_Unido":
                self.geography = 'https://es.wikipedia.org/wiki/Geografia_del_'
            elif formatted_pais == "Canada":
                self.geography = 'https://es.wikipedia.org/wiki/Geografia_de_'
            else:
                self.geography = 'https://es.wikipedia.org/wiki/Geografia_de_'

            link_geography = self.geography + formatted_pais
            link_data.append(link_geography)
        return link_data

    def extract_country_name(self, url):
        # Implement the logic to extract the country name from the URL
        # For demonstration purposes, let's assume the country name is the last part of the URL
        parts = url.split('/')
        country_name = parts[-1].replace('_', ' ')
        return country_name

    def check_data_country(self, link_data):
        continents = ["Europa", "Asia", "África", "América del Norte", "América del Sur", "Oceanía"]
        data_content = self.content.data_content

        country_to_url_mapping = {}  # Map country names to their corresponding URLs

        # Populate the mapping of country names to URLs
        for link in link_data:
            country_name = self.extract_country_name(link)
            if country_name:
                country_to_url_mapping[country_name] = link

        # Iterate through the music entries and associate continent information
        for music_entry in data_content:
            country_name = music_entry.pais.lower()
            if country_name in country_to_url_mapping:
                url = country_to_url_mapping[country_name]
                try:
                    r: Response = requests.get(url)
                    if r.status_code != 200:
                        continue
                    soup: BeautifulSoup = BeautifulSoup(r.content, "html.parser")
                    infobox_tables = soup.find_all("table", class_="infobox")

                    if infobox_tables:
                        print(infobox_tables)
                        first_infobox = infobox_tables[0]
                        for continent in continents:
                            title_element = first_infobox.find("a", title=continent)
                            print(title_element)
                            if title_element:
                                continent_name = title_element.text
                                music_entry.continent = continent_name
                                print(f"Added continent info for {music_entry.pais}: {continent_name}")
                                break  # Break the loop once we find the continent info
                        else:
                            print(f"No geography data available for {music_entry.pais}")
                except Exception as ex:
                    print("Error en el servidor: ", ex)
                    return None

        return data_content

if __name__ == '__main__':
    e = ExtractCountry()
    link_data = e.get_geography()
    data_content = e.check_data_country(link_data)
    print(data_content)
    # Print the data
    # for music_entry in data_content:
    #     print(f"Music Entry - "
    #           f"Tema: {music_entry.tema}, Intérprete: {music_entry.interprete}, Año: {music_entry.ano}, "
    #           f"Semanas: {music_entry.semanas}, País: {music_entry.pais}, Continente: {music_entry.continent}")
