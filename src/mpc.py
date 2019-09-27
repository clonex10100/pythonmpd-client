from mpd import MPDClient
from song import Song

#Decortor for all functions that use self.client
def mpd_client_call(func):
    #Test if connection to client has timed out, if so reconnect
    def ensure_connected(self, *args, **kwargs):
        print("Testing connection")
        try:
            self.client.status()
        except:
            print("Connection lost, recconencting")
            self.client.connect("localhost", 6600)
        return func(self, *args, **kwargs)
    return ensure_connected

#decorator for all functions updating the queue, to ensure PlaybackQueue is updated
def updates_queue(func):
    def update_queue(self, *args, **kwargs):
        out = func(self, *args, **kwargs)
        self.playback_queue.populate(self.list_queue())
        return out
    return update_queue

class MpdClient():
    def __init__(self):
        self.client = self.connect()

    #Connects self.client to the MPD Client
    def connect(self, ip="localhost", port=6600):
        client = MPDClient()
        client.idletimeout = None
        client.connect(ip, port)
        return client

    def link_queue(self, playback_queue):
        self.playback_queue = playback_queue

    @mpd_client_call
    def quit(self):
        self.client.close()
        self.client.disconnect()

    #Simple methods for playback control

    @mpd_client_call
    def play(self):
        self.client.pause(0)

    @mpd_client_call
    def pause(self):
        self.client.pause(1)

    @mpd_client_call
    def stop(self):
        self.client.stop()

    @mpd_client_call
    def toggle(self):
        state = self.client.status().get("state")
        self.play() if state == "pause" or state == "stop" else self.pause()
        print(self.client.status().get("state"))

    @mpd_client_call
    def list_albums(self):
        return self.client.list("album")

    @mpd_client_call
    def list_queue(self):
        return [Song(song_hash) for song_hash in self.client.playlistinfo()]

    @mpd_client_call
    @updates_queue
    def play_album(self, album_name):
        self.client.clear()
        self.client.findadd("album", album_name)
        self.client.play(0)

    @mpd_client_call
    def current_song(self):
        return Song(self.client.currentsong())

    @mpd_client_call
    def current_song_index(self):
        print(self.list_queue())
        current_song = self.current_song()
        j = 0
        for i in self.list_queue():
            if i == current_song: return j
            j += 1

    #Just for repl tests, TODO remove
    @mpd_client_call
    def client(self):
        return self.client
