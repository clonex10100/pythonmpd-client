import gi
import sys
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from mp import MpdClient
from AlbumTreeView import AlbumTreeView

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
        #pane = HorzPane(Container(self.add))
        self.client = MpdClient()
        #button = Gtk.Button(label="Toggle")
        #button.connect("clicked", self.on_click)
        album_list = AlbumTreeView(self.client)
        album_list.populate(self.client.list_albums())
        self.add(album_list.get_view())

        #image = Gtk.Image()
        #image.set_from_file("test.png")
        #image2 = Gtk.Image()
        #image2.set_from_file("test.png")

        #pane2 = VertPane(pane.get_cont1())
        #pane.get_cont2().add(image2)
        #pane2.get_cont1().add(button)
        #pane2.get_cont2().add(image)

        #pane.set_pos(100)
        #pane2.set_pos(100)


    def on_click(self, widget):
        self.client.toggle()

class Container():
    def __init__(self, addMethod):
        self.a = addMethod
    def add(self,child):
        self.a(child)

class Pane():
    def __init__(self, container, paneType):
        self.pane = Gtk.Paned.new(paneType)
        container.add(self.pane)

        self.cont1 = Container(self.pane.add1)
        self.cont2 = Container(self.pane.add2)
    def get_cont1(self):
        return self.cont1
    def get_cont2(self):
        return self.cont2
    def set_pos(self, pos):
        self.pane.set_position(pos)

class VertPane(Pane):
    def __init__(self, container):
        super().__init__(container, Gtk.Orientation.VERTICAL)

class HorzPane(Pane):
    def __init__(self, container):
        super().__init__(container, Gtk.Orientation.HORIZONTAL)

app = Application()
app.run(sys.argv)
