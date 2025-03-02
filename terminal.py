#!/usr/bin/env python3

import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, Gdk, GLib

def apply_css():
    css_provider = Gtk.CssProvider()
    css_data = """
* {
    background-color: #1e1e1e;  /* Darker gray for background (still close to black) */
    color: #d1d1d1;  /* Light gray text for better readability */
    font-family: "Monospace";
    font-size: 12px;
    border-radius: 6px;
    transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out;  /* Smooth transition for hover effects */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);  /* Subtle shadow for depth */
}

button {
    background-color: #333;  /* Dark button background */
    color: #d1d1d1;  /* Light gray text for buttons */
    border: 1px solid #555;
    font-weight: 500;
    padding: 4px 8px;
    margin: 2px;
    min-width: 16px;
    min-height: 16px;
    border-radius: 4px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease-in-out;
}

button:hover {
    background-color: #555;  /* Slightly lighter on hover */
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.25);
}

menuitem {
    border-bottom: 1px solid #444;  /* Subtle separation */
    padding: 4px 8px;
}

menuitem:hover {
    background-color: #444;  /* Darker hover background */
    color: #fff;  /* White text on hover for contrast */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);
}

GtkLabel {
    color: #d1d1d1;  /* Light gray for labels */
}

GtkButton {
    border-radius: 5px;  /* More rounded buttons */
}

GtkEntry {
    background-color: #333;  /* Dark input fields */
    color: #d1d1d1;  /* Light gray text */
    border: 1px solid #555;
}

GtkEntry:focus {
    border-color: #ff5500;  /* Highlight input field on focus */
}

    """
    css_provider.load_from_data(css_data.encode())
    screen = Gdk.Screen.get_default()
    style_context = Gtk.StyleContext()
    style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class QuickTerm(Gtk.Window):
    def __init__(self):    
        super().__init__()
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title("Quick Terminal-GTK3")
        self.connect("button-press-event", self.on_button_press_event)
        # Menu
        self.menu = Gtk.Menu()

        # Menu buttons
        self.copy_it = Gtk.MenuItem(label="Copy")
        self.copy_it.connect("activate", self.copy)

        self.paste_it = Gtk.MenuItem(label="Paste")
        self.paste_it.connect("activate", self.paste)

        self.new_tab_item = Gtk.MenuItem(label="New Tab")
        self.new_tab_item.connect("activate", self.new_tab)

        self.menu.append(self.copy_it)
        self.menu.append(self.paste_it)
        self.menu.append(self.new_tab_item)

        # About Quick Terminal
        self.about_ter = Gtk.MenuItem(label="About Quick Terminal")
        self.about_ter.connect("activate", self.about1)
        self.menu.append(self.about_ter)

        # Create the Notebook for tabs
        self.notebook = Gtk.Notebook()

        # Initial terminal
        term = self.create_terminal()
        self.notebook.append_page(term, self.create_tab_label("Terminal", term))

        self.add(self.notebook)
        self.show_all()

        self.set_resizable(True)
        self.connect("destroy", Gtk.main_quit)

    def copy(self, widget):
        current_term = self.notebook.get_nth_page(self.notebook.get_current_page())
        current_term.copy_clipboard()
        current_term.grab_focus()

    def paste(self, widget):
        current_term = self.notebook.get_nth_page(self.notebook.get_current_page())
        current_term.paste_clipboard()
        current_term.grab_focus()

    def about1(self, widget):
        about1 = Gtk.AboutDialog()
        about1.set_program_name("Quick Terminal-GTK3")
        about1.set_version("V.1.0")
        about1.set_copyright("Copyright (c) 2017 JJ Posti <techtimejourney.net>")
        about1.set_comments(("Quick terminal is a terminal emulator written with Python. "
                             "The program comes with ABSOLUTELY NO WARRANTY; for details see: "
                             "http://www.gnu.org/copyleft/gpl.html. This is free software, "
                             "and you are welcome to redistribute it under GPL Version 2, June 1991."))
        about1.set_website("www.techtimejourney.net")
        about1.run()
        about1.destroy()
        

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        uris = data.get_uris()
        if uris:
            try:
                path = GLib.filename_from_uri(uris[0])[0]
                if os.path.isdir(path):
                    print("Dropped item is a folder.")
                else:
                    print("Dropped item is a file.")
                widget.feed_child(f'"{path}"'.encode())
            except Exception as e:
                print(f"Error processing dropped item: {e}")
            finally:
                drag_context.finish(True, False, time)      


    def close_tab(self, button, terminal_widget):
        """Close the tab by using the terminal widget as a reference."""
        if self.notebook.get_n_pages() == 1:  # If only one tab is open
            return  # Don't close it
        page_num = self.notebook.page_num(terminal_widget)
        if page_num != -1:
            self.notebook.remove_page(page_num)

    def create_tab_label(self, title, terminal_widget):
        """Create a custom tab label with a title and a close button."""
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        label = Gtk.Label(label=title)

        close_btn = Gtk.Button.new_from_icon_name("window-close", Gtk.IconSize.BUTTON)
        close_btn.set_relief(Gtk.ReliefStyle.NONE)
        close_btn.connect("clicked", self.close_tab, terminal_widget)

        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(close_btn, False, False, 0)
        hbox.show_all()
        return hbox

    def new_tab(self, widget):
        term = self.create_terminal()
        tab_label = self.create_tab_label("Terminal", term)
        self.notebook.append_page(term, tab_label)
        self.notebook.show_all()

    def on_button_press_event(self, widget, event):
        if event.button == 3:  # Right click
            self.menu.show_all()
            self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
        elif event.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:        
            self.new_tab(widget)
            return True


    def create_terminal(self):
        vte = Vte.Terminal()
        vte.connect("child-exited", self.on_terminal_child_exited)

        # Drag and drop
        vte.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        vte.drag_dest_add_uri_targets()
        vte.connect("drag-data-received", self.on_drag_data_received)

        # Setting background color and foreground (text) color for the terminal
        vte.set_color_background(Gdk.RGBA(0.164, 0.164, 0.164, 1))  # RGBA values for #2a2a2a
        vte.set_color_foreground(Gdk.RGBA(0.960, 0.960, 0.960, 1))  # RGBA values for #f5f5f5

        try:
            vte.spawn_async(
                Vte.PtyFlags.DEFAULT,
                os.environ['HOME'],
                ["/bin/bash"],
                None,
                0,
                None,
                None,
                -1,
                None,
                None
            )
        except Exception as e:
            print(f"Error spawning terminal: {e}")
        return vte


    def on_terminal_child_exited(self, terminal, status):
        """Close the tab when the terminal child process exits."""
        page_num = self.notebook.page_num(terminal)
        if page_num != -1:
            self.notebook.remove_page(page_num)
            self.notebook.queue_draw()
        # If no more pages left, quit the application
        if self.notebook.get_n_pages() == 0:
            Gtk.main_quit()    
def main():
    Gtk.main()
    return 0

if __name__ == "__main__":
    apply_css()  # Apply CSS first
    QuickTerm()
    main()
