from mpd import MPDClient

def mpd_client_call(func):
    def ensure_connected(self, *args, **kwargs):
        print("Testing connection")
        try:
            self.client.status()
        except:
            self.client.connect("localhost", 6600)
        return func(self, *args, **kwargs)
    return ensure_connected

class MpdClient():
    def __init__(self):
        self.client = self.connect()

    #Connects self.client to the MPD Client
    def connect(self, ip="localhost", port=6600):
        client = MPDClient()
        client.idletimeout = None
        client.connect(ip, port)
        return client
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
    def play_album(self, album_name):
        self.client.clear()
        self.client.findadd("album", album_name)
        self.client.play(0)

    #Just for repl tests, TODO remove
    @mpd_client_call
    def client(self):
        return self.client
