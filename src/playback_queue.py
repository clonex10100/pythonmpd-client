import gi 
import sys
gi.require_version ("Gtk", "3.0")
from gi.repository import Gtk

class PlaybackQueue():
    def __init__(self, client):
        #Sets mpd client
        self.client = client

        #Sets up list store, for now each row only contains a song name
        self.list_store = Gtk.ListStore(str)

        #Sets up treeview
        self.tree_view = Gtk.TreeView(self.list_store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Song", renderer, text = 0)
        self.tree_view.append_column(column)

        self.selection = self.tree_view.get_selection()

        #Links queue to mpd client, so it can be updated when the queue changes
        self.client.link_queue(self)

    def populate(self, song_list):
        self.list_store.clear()
        for song in song_list:
            self.list_store.append([song.get_title()])
    def get_view(self):
        return self.tree_view

    def update_current_song(self):
        #Current_song_iter is the iter corrasponding to the current song, how do I highlight it in the tree view?
        current_song_iter = self.get_current_song()
        return True

