import gi
import sys
gi.require_version ("Gtk", "3.0")
from gi.repository import Gtk

class PlaybackQueue():
    def __init__(self, client):
        #Sets mpd client
        self.client = client
                #Randomq
                
        #Sets up list store, for now each row only contains a song name
        self.list_store = Gtk.ListStore(str, str)

        #Sets up treeview
        self.tree_view = Gtk.TreeView(self.list_store)


        #Adding collumns
        for i, title in enumerate(["Song", "Playing"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text = i)
            self.tree_view.append_column(column)

        self.selection = self.tree_view.get_selection()

        self.scrollable_tree_view = Gtk.ScrolledWindow()
        self.scrollable_tree_view.add(self.tree_view)

        #Links queue to mpd client, so it can be updated when the queue changes
        self.client.link_queue(self)

    def populate(self, song_list):
        self.list_store.clear()
        for song in song_list:
            self.list_store.append([song.get_title(), ""])
    def get_view(self):
        return self.scrollable_tree_view

    def update_current_song(self):
        self.list_store[self.client.current_song_index()][1] = "X"
        return True
