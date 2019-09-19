class Song:
    def __init__(self, song_hash):
        self.title = song_hash["title"]
    def get_title(self):
        return self.title
