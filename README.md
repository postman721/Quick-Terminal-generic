Quick Terminal-GTK3

A modern and lightweight GTK3-based terminal emulator with tab support and a stylish dark mode theme.

Screenshot of Quick Terminal-GTK3

Features

    Tab Support: Easily manage multiple terminal sessions in one window.
    Drag & Drop: Drag files and directories into the terminal to use them.
    Context Menu: Right-click to access commonly used functions like copy, paste, and open new tab.
    Stylish Appearance: Dark mode theme for the terminal and buttons.
    Customizable: Uses GTK, making it easy to theme and customize further.

Dependencies
General:

    Python 3
    GTK3
    Vte 2.91

### Usage

    Open a new tab: Double click on any tab. Entry to create new tab is also within the right-click menu.
    Close a tab: Click the close button on the tab.
    Copy & Paste: Right-click to open the context menu and select the copy or paste option.



### Debian/Ubuntu as an example

To install the dependencies on Debian or Ubuntu, use the following commands:



sudo apt update
sudo apt install python3 python3-gi gir1.2-gtk-3.0 gir1.2-vte-2.91

Running: python3 terminal.py

