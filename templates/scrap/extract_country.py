from templates.request_music import MusicFromWeb

class ExtrarctContry:
    def __init__(self):
        self.music_web = MusicFromWeb()

    def get_contry(self):
        data = self.music_web.get_info()
        for entry in data:
            country = self.music_web.extract_country(entry.pais)
            print(f"Country for '{entry.pais}': {country}")

if __name__ == '__main__':
    e: ExtrarctContry = ExtrarctContry()
    e.get_contry()
