class Song:
    def __init__(self, song_hash):
        self.title = song_hash["title"]
        self.album = song_hash["album"]
        self.artist = song_hash["artist"]
        self.duration = song_hash["time"]
    def get_title(self):
        return self.title
    def get_album(self):
        return self.album
    def get_artist(self):
        return self.artist
    def get_duration(self):
        return self.duration
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.album == other.title and self.title == other.title
