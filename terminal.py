#!/usr/bin/env python3
from gi.repository import Gtk, Vte, Gdk, GLib
import os, sys
class QuickTerm(Gtk.Window):
#Destroy function a.k.a. closing the window function
    def destroy (self, widget):
        Gtk.main_quit()
        
    def copy(self, widget):
        self.vte.copy_clipboard()
        self.vte.grab_focus()
        
    def paste(self, widget):
        self.vte.paste_clipboard()
        self.vte.grab_focus()                                
###################################################################################
#About dialog function
    def about1 (self, widget):
        about1 = Gtk.AboutDialog()
        about1.set_program_name("Quick Terminal-GTK3 ")
        about1.set_version("V.0.7")
        about1.set_copyright(" Copyright (c) 2017 JJ Posti <techtimejourney.net>")
        about1.set_comments("Quick terminal is a terminal emulator written with Python. The program comes with ABSOLUTELY NO WARRANTY; for details see: http://www.gnu.org/copyleft/gpl.html. This is free software, and you are welcome to redistribute it under GPL Version 2, June 1991.")
        about1.set_website("www.techtimejourney.net")
        about1.run()
        about1.destroy()
#################################################Right click 
    def right_click(self, widget, event):
        if event.button == 3:
            self.menu.show_all()            
            self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
############Make the window	
    def __init__(self):    
    # Create THE WINDOW
        self.window1=Gtk.Window()
        self.window1.set_position(Gtk.WindowPosition.CENTER)
        self.window1.set_title("Quick Terminal-GTK3")
        self.window1.connect("button_press_event", self.right_click)
#Menu
        self.menu=Gtk.Menu()
#Menu buttons
        #Copy&Paste
        self.copy_it = Gtk.MenuItem("Copy")
        self.copy_it.connect("activate", self.copy)

        self.paste_it = Gtk.MenuItem("Paste")
        self.paste_it.connect("activate", self.paste)
        
        self.menu.append(self.copy_it)
        self.menu.append(self.paste_it)
        
        #About Quick Terminal
        self.about_ter = Gtk.MenuItem("About Quick Terminal")
        self.about_ter.connect("activate", self.about1)
        self.menu.append(self.about_ter)                          

#Terminal
        self.vte = Vte.Terminal()
        self.vte.connect ("child-exited", Gtk.main_quit)

#Fork
        self.vte.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/bin/bash"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            )
#Make a clipboard for copy and paste
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

#Scrolled window
        self.scroll=Gtk.ScrolledWindow()
        self.scroll.set_min_content_height(350)
        self.scroll.set_min_content_width(640)
        self.scroll.add(self.vte)

#Vertical box/buttons container
        self.vbox=Gtk.VBox(False)
        self.vbox.pack_start(self.scroll, True, True, True)

#Show everything		
        self.window1.add(self.vbox)
        self.window1.show_all()
         
#Making window resizable and enabling the close window connector        
        self.window1.set_resizable(True)
        self.window1.connect("destroy", Gtk.main_quit)

class CSS():
#CSS Styles
        style_provider = Gtk.CssProvider()
        css = open('/usr/share/base.css', 'rb')
        css_data = css.read()
        css.close()
        style_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION) 
def main():
    Gtk.main()
    return 0

if __name__ == "__main__":
    QuickTerm()
    main()
