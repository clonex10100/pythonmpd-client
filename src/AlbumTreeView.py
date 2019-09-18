import gi
import sys
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#Class in charge of the album picker list
class AlbumTreeView():
    def __init__(self, client):
        #Store mpd client
        self.client = client
        #Create store, list, and renderer for treeview
        self.list_store = Gtk.ListStore(str)
        self.tree_view = Gtk.TreeView(self.list_store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Album", renderer, text=0)
        self.tree_view.append_column(column)

        #define behavior for selected list item
        #select = self.tree_view.get_selection()
        #select.connect("changed", self._play_selection)

        #define activated behavior for row
        self.tree_view.connect("row_activated", self._play_album)
        self.tree_view.connect("button_press_event", self._button_press)

        #Define scrollable window to hold the treeview and make it scrollable
        self.scrollable_tree_view = Gtk.ScrolledWindow()
        self.scrollable_tree_view.add(self.tree_view)
    #accepts list of albums and populates treeview
    def populate(self,album_list):
        for album in album_list:
            self.list_store.append([album])

    def _play_album(self, tree_view, tree_path, tree_collumn):
        album_name = self.list_store[tree_path][0]
        self.client.play_album(album_name)

    def _button_press(self, tree_view, event):
        if event.button == 3:
            list_store, tree_iter = tree_view.get_selection().get_selected()
            print(list_store[tree_iter][0])

    #getter for treeview object
    def get_view(self):
        return self.scrollable_tree_view

