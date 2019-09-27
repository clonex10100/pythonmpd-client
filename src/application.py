import gi
import sys
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
from mp import MpdClient
from AlbumTreeView import AlbumTreeView
from playback_queue import PlaybackQueue

class Application(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        self.win = AppWindow(self)
        self.win.connect("destroy", Gtk.main_quit)
        self.win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(title="Testing", application=app)
        pane = HorzPane(Container(self.add))
        self.client = MpdClient()
        play_pause = Gtk.Button(label="Toggle")
        play_pause.connect("clicked", self.on_click)

        album_list = AlbumTreeView(self.client)
        album_list.populate(self.client.list_albums())

        playback_queue = PlaybackQueue(self.client)
        playback_queue.populate(self.client.list_queue())

        #self.add(album_list.get_view())

        #image = Gtk.Image()
        #image.set_from_file("test.png")
        #image2 = Gtk.Image()
        #image2.set_from_file("test.png")

        pane.get_cont1().add(album_list.get_view())
        #pane.get_cont2().add(playback_queue.get_view())
        
        pane2 = VertPane(pane.get_cont2())
        pane2.get_cont1().add(playback_queue.get_view())
        pane2.get_cont2().add(play_pause)

        pane.add()
        pane2.add()
        GLib.timeout_add(500, playback_queue.update_current_song)
        #Glib.MainLoop().run()


    def on_click(self, widget):
        print(self.get_size())
        self.client.toggle()

class Container():
    def __init__(self, addMethod):
        self.a = addMethod
    def add(self,child):
        self.a(child)

class Pane():
    def __init__(self, container, paneType):
        self.pane = Gtk.Paned.new(paneType)
        self.container = container
        self.cont1 = Container(self.pane.add1)
        self.cont2 = Container(self.pane.add2)
    def add(self):
        self.container.add(self.pane)

    def get_cont1(self):
        return self.cont1
    def get_cont2(self):
        return self.cont2
    def set_pos(self, pos):
        self.pane.set_position(pos)
    def get_pos(self):
        return self.pane.get_position()

class VertPane(Pane):
    def __init__(self, container):
        super().__init__(container, Gtk.Orientation.VERTICAL)

class HorzPane(Pane):
    def __init__(self, container):
        super().__init__(container, Gtk.Orientation.HORIZONTAL)

app = Application()
app.run(sys.argv)
