import tkinter as tk
from tkinter import ttk
import webbrowser
import subprocess

from assets.icon import icon
from toxic_typer import TOXICTyper

__version__ = "2.0.0"
toxic_typer = TOXICTyper(mode=1)

root = tk.Tk()
root.title("Toxic Typer")
root.geometry("800x350")
root.resizable(False, False)

img = tk.PhotoImage(data=icon)
root.tk.call("wm", "iconphoto", root._w, img)

# Left frame for Toxic Typer controls
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))  # Added left padding

# Clipboard history frame on the right with padding
clipboard_frame = tk.Frame(root)
clipboard_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=(10, 10))  # Added right and bottom padding

# Set the background color for the main window and frames
root.configure(bg="#313131")  # Background color for the main window
left_frame.configure(bg="#313131")  # Background color for the left frame
clipboard_frame.configure(bg="#313131")  # Background color for the clipboard frame

# Toxic Typer Controls
tk.Label(left_frame, text="Toxic Typer", font=("Courier", 30, "bold"), fg="#eeeeee", bg="#313131").pack()

link_to_profile = tk.Label(
    left_frame, text="Little modification done by me on toxic TYPER", fg="yellow", bg="#313131", cursor="hand2"
)
link_to_profile.pack()
link_to_profile.bind(
    "<Button-1>", lambda e: webbrowser.open_new("https://github.com/G0dVai/")
)

updates_label = tk.Label(
    left_frame, text=f"v{__version__} click here to see updates", fg="#eeeeee", bg="#313131", cursor="hand2"
)
updates_label.pack()
updates_label.bind(
    "<Button-1>",
    lambda e: webbrowser.open_new(
        "https://github.com/G0dVai/Toxic-Typer/releases"
    ),
)

tk.Label(
    left_frame, text="Press shortcut key to paste from clipboard", font=("Arial", 12), fg="#eeeeee", bg="#313131"
).pack(pady=(0, 20))

mode_frame = tk.Frame(left_frame, bg="#313131")
mode_frame.pack(anchor=tk.W, padx=20)

tk.Label(mode_frame, text="Mode:", font=("Arial", 12), bg="#313131", fg="#eeeeee").pack(side=tk.LEFT)

for mode in toxic_typer.modes:
    radio = tk.Radiobutton(
        mode_frame,
        text=mode.capitalize(),
        value=mode,
        font=("Arial", 12),
        bg="#313131",
        fg="#eeeeee",
        activebackground="#313131",
        activeforeground="#eeeeee",
        selectcolor="#313131",
        command=lambda mode=mode: toxic_typer.set_mode(mode),
    )
    radio.pack(side=tk.LEFT)
    if mode == toxic_typer.mode:
        radio.select()

shortcut_frame = tk.Frame(left_frame, bg="#313131")
shortcut_frame.pack(anchor=tk.W, padx=20)

shortcut_key = tk.StringVar(value="Right Ctrl")

tk.Label(shortcut_frame, text="Shortcut key:", font=("Arial", 12), bg="#313131", fg="#eeeeee").pack(side=tk.LEFT)

for key in toxic_typer.shortcut_keys:
    radio = tk.Radiobutton(
        shortcut_frame,
        text=key,
        value=key,
        font=("Arial", 12),
        bg="#313131",
        fg="#eeeeee",
        activebackground="#313131",
        activeforeground="#eeeeee",
        selectcolor="#313131",
        command=lambda key=key: toxic_typer.set_shortcut_key(key),
        variable=shortcut_key,
    )
    radio.pack(side=tk.LEFT)
    if key == toxic_typer.shortcut_key:
        radio.select()

line_break_frame = tk.Frame(left_frame, bg="#313131")
line_break_frame.pack(anchor=tk.W, padx=20)

line_break = tk.BooleanVar(value=toxic_typer.line_break)

tk.Checkbutton(
    line_break_frame,
    text="Line Break",
    font=("Arial", 12),
    fg="#eeeeee",
    bg="#313131",
    activebackground="#313131",
    activeforeground="#eeeeee",
    selectcolor="#313131",
    variable=line_break,
    command=lambda: toxic_typer.set_line_break(line_break.get()),
).pack(side=tk.LEFT)

remove_everything_frame = tk.Frame(left_frame, bg="#313131")
remove_everything_frame.pack(anchor=tk.W, padx=20)

remove_everything = tk.BooleanVar(value=toxic_typer.remove_everything)
remove_auto_brackets = tk.BooleanVar(value=toxic_typer.remove_auto_brackets)

tk.Checkbutton(
    remove_everything_frame,
    text="Remove everything before pasting",
    font=("Arial", 12),
    fg="#eeeeee",
    bg="#313131",
    activebackground="#313131",
    activeforeground="#eeeeee",
    selectcolor="#313131",
    variable=remove_everything,
    command=lambda: toxic_typer.set_remove_everything(remove_everything.get()),
).pack(side=tk.LEFT)

tk.Checkbutton(
    remove_everything_frame,
    text="Remove Auto Brackets",
    font=("Arial", 12),
    fg="#eeeeee",
    bg="#313131",
    activebackground="#313131",
    activeforeground="#eeeeee",
    selectcolor="#313131",
    variable=remove_auto_brackets,
    command=lambda: toxic_typer.set_remove_auto_brackets(remove_auto_brackets.get()),
).pack(side=tk.LEFT)

ruuning_label = tk.Label(
    left_frame, text="Toxic Typer is running...", font=("Courier", 10, "bold"), fg="green", bg="#313131"
)

is_enabled = tk.StringVar()
is_enabled.set("START")

def toggle():
    if is_enabled.get() == "START":
        toxic_typer.start()
        is_enabled.set("STOP")
        ruuning_label.pack()
        print("Toxic Typer is enabled.")
    else:
        toxic_typer.stop()
        is_enabled.set("START")
        ruuning_label.pack_forget()
        print("Toxic Typer is disabled.")

tk.Button(
    left_frame, textvariable=is_enabled, font=("Arial", 12, "bold"), command=toggle, width=20
).pack(pady=(15, 10))

class ScrolledFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Create a canvas and scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Configure the canvas
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Clipboard history column using a Notebook for tabs
clipboard_history_label = tk.Label(clipboard_frame, text="Clipboard Content", font=("Courier", 13, "bold"), fg="#eeeeee", bg="#313131", )
clipboard_history_label.pack(pady=10)

style = ttk.Style()

# Ensure your style changes apply to the correct theme
style.theme_use("default")

# Configure the TNotebook tab
style.configure(
    "TNotebook.Tab",
    background="#313131",   # Tab background color
    foreground="#eeeeee",   # Tab text color
    padding=[2, 2],        # Padding around the tab text
)

# Configure the selected tab
style.map(
    "TNotebook.Tab",
    background=[("selected", "#217346")],  # Selected tab background color
    foreground=[("selected", "#ffffff")],  # Selected tab text color
)

clipboard_notebook = ttk.Notebook(clipboard_frame)  # Create a Notebook
clipboard_notebook.pack(fill=tk.BOTH, expand=True, padx=(5, 5), pady=(5, 10))  # Add padding

text_widgets = []

copied_items = []

def update_clipboard_history():
    try:
        # Get the current clipboard content
        clipboard_content = root.clipboard_get()

        # If it's a new item, add it to the history
        if clipboard_content and clipboard_content not in copied_items:
            copied_items.append(clipboard_content)
            # Create a new tab for the copied content
            tab = ttk.Frame(clipboard_notebook)
            clipboard_notebook.add(tab, text=f"Tab {len(copied_items)}")  # Set tab title

            # Create a ScrolledFrame for the new tab
            scrolled_frame = ScrolledFrame(tab)
            scrolled_frame.pack(fill=tk.BOTH, expand=True)  # Ensure the ScrolledFrame expands to fill the tab

            # Create a Text widget for clipboard content
            text_widget = tk.Text(
                scrolled_frame.scrollable_frame,
                wrap=tk.WORD,  # Enable word wrapping
                padx=10,
                pady=10,
                bg="#313131",
                fg="#eeeeee",
            )
            text_widget.pack(fill=tk.BOTH, expand=True)  # Ensure it fills the space

            # Insert the copied content into the Text widget
            text_widget.insert(tk.END, clipboard_content)

            # Make the Text widget read-only (optional)
            text_widget.config(state=tk.DISABLED)  # Disable editing

            # Store the reference to the Text widget
            text_widgets.append(text_widget)

            # Scroll to the latest entry
            clipboard_notebook.select(tab)  # Automatically switch to the new tab
    except tk.TclError:
        # Handle the case when clipboard is empty or invalid content
        pass

    # Check again after 1 second
    root.after(1000, update_clipboard_history)

def enable_clipboard_history():
    try:
        subprocess.run(
            ["powershell", "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Clipboard' -Name 'EnableClipboardHistory' -Value 1"], check=True
        )
        print("Clipboard history enabled")
    except subprocess.CalledProcessError as e:
        print(f"Error enabling clipboard history: {e}")

enable_clipboard_history()

def switch_tab(event):
    if event.state == 12:  # Ctrl pressed
        tab_index = event.keysym[-1]  # Get the last character of the key (e.g., '1' from '1')
        if tab_index.isdigit():
            index = int(tab_index) - 1  # Convert to zero-based index
            if 0 <= index < len(copied_items):
                clipboard_notebook.select(index)

                # Get the content of the selected tab
                if index < len(text_widgets):
                    text_widget = text_widgets[index]
                    text_widget.config(state=tk.NORMAL)  # Temporarily enable editing to read the content
                    content = text_widget.get("1.0", tk.END).strip()  # Get the content
                    text_widget.config(state=tk.DISABLED)  # Disable editing again

                    # Set the content to be typed
                    toxic_typer.set_text_to_type(content)  # Set content to type

# Bind the key combination for Ctrl + Number
root.bind('<Control-KeyPress>', switch_tab)

# Start updating the clipboard history
update_clipboard_history()

try:
    print("Toxic Typer is running...")
    root.mainloop()
except KeyboardInterrupt:
    pass
print("Toxic Typer is stopped.")
import tkinter as tk
from tkinter import ttk
import webbrowser
import subprocess

from assets.icon import icon
from toxic_typer import TOXICTyper

__version__ = "2.0.0"
toxic_typer = TOXICTyper(mode=1)

root = tk.Tk()
root.title("Toxic Typer")
root.geometry("800x350")
root.resizable(False, False)

img = tk.PhotoImage(data=icon)
root.tk.call("wm", "iconphoto", root._w, img)

# Left frame for Toxic Typer controls
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))  # Added left padding

# Clipboard history frame on the right with padding
clipboard_frame = tk.Frame(root)
clipboard_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=(10, 10))  # Added right and bottom padding

# Set the background color for the main window and frames
root.configure(bg="#313131")  # Background color for the main window
left_frame.configure(bg="#313131")  # Background color for the left frame
clipboard_frame.configure(bg="#313131")  # Background color for the clipboard frame

# Toxic Typer Controls
tk.Label(left_frame, text="Toxic Typer", font=("Courier", 30, "bold"), fg="#eeeeee", bg="#313131").pack()

link_to_profile = tk.Label(
    left_frame, text="Little modification done by me on toxic TYPER", fg="yellow", bg="#313131", cursor="hand2"
)
link_to_profile.pack()
link_to_profile.bind(
    "<Button-1>", lambda e: webbrowser.open_new("https://github.com/G0dVai/")
)

updates_label = tk.Label(
    left_frame, text=f"v{__version__} click here to see updates", fg="#eeeeee", bg="#313131", cursor="hand2"
)
updates_label.pack()
updates_label.bind(
    "<Button-1>",
    lambda e: webbrowser.open_new(
        "https://github.com/G0dVai/Toxic-Typer/releases"
    ),
)

tk.Label(
    left_frame, text="Press shortcut key to paste from clipboard", font=("Arial", 12), fg="#eeeeee", bg="#313131"
).pack(pady=(0, 20))

mode_frame = tk.Frame(left_frame, bg="#313131")
mode_frame.pack(anchor=tk.W, padx=20)

tk.Label(mode_frame, text="Mode:", font=("Arial", 12), bg="#313131", fg="#eeeeee").pack(side=tk.LEFT)

for mode in toxic_typer.modes:
    radio = tk.Radiobutton(
        mode_frame,
        text=mode.capitalize(),
        value=mode,
        font=("Arial", 12),
        bg="#313131",
        fg="#eeeeee",
        activebackground="#313131",
        activeforeground="#eeeeee",
        selectcolor="#313131",
        command=lambda mode=mode: toxic_typer.set_mode(mode),
    )
    radio.pack(side=tk.LEFT)
    if mode == toxic_typer.mode:
        radio.select()

shortcut_frame = tk.Frame(left_frame, bg="#313131")
shortcut_frame.pack(anchor=tk.W, padx=20)

shortcut_key = tk.StringVar(value="Right Ctrl")

tk.Label(shortcut_frame, text="Shortcut key:", font=("Arial", 12), bg="#313131", fg="#eeeeee").pack(side=tk.LEFT)

for key in toxic_typer.shortcut_keys:
    radio = tk.Radiobutton(
        shortcut_frame,
        text=key,
        value=key,
        font=("Arial", 12),
        bg="#313131",
        fg="#eeeeee",
        activebackground="#313131",
        activeforeground="#eeeeee",
        selectcolor="#313131",
        command=lambda key=key: toxic_typer.set_shortcut_key(key),
        variable=shortcut_key,
    )
    radio.pack(side=tk.LEFT)
    if key == toxic_typer.shortcut_key:
        radio.select()

line_break_frame = tk.Frame(left_frame, bg="#313131")
line_break_frame.pack(anchor=tk.W, padx=20)

line_break = tk.BooleanVar(value=toxic_typer.line_break)

tk.Checkbutton(
    line_break_frame,
    text="Line Break",
    font=("Arial", 12),
    fg="#eeeeee",
    bg="#313131",
    activebackground="#313131",
    activeforeground="#eeeeee",
    selectcolor="#313131",
    variable=line_break,
    command=lambda: toxic_typer.set_line_break(line_break.get()),
).pack(side=tk.LEFT)

remove_everything_frame = tk.Frame(left_frame, bg="#313131")
remove_everything_frame.pack(anchor=tk.W, padx=20)

remove_everything = tk.BooleanVar(value=toxic_typer.remove_everything)
remove_auto_brackets = tk.BooleanVar(value=toxic_typer.remove_auto_brackets)

tk.Checkbutton(
    remove_everything_frame,
    text="Remove everything before pasting",
    font=("Arial", 12),
    fg="#eeeeee",
    bg="#313131",
    activebackground="#313131",
    activeforeground="#eeeeee",
    selectcolor="#313131",
    variable=remove_everything,
    command=lambda: toxic_typer.set_remove_everything(remove_everything.get()),
).pack(side=tk.LEFT)

tk.Checkbutton(
    remove_everything_frame,
    text="Remove Auto Brackets",
    font=("Arial", 12),
    fg="#eeeeee",
    bg="#313131",
    activebackground="#313131",
    activeforeground="#eeeeee",
    selectcolor="#313131",
    variable=remove_auto_brackets,
    command=lambda: toxic_typer.set_remove_auto_brackets(remove_auto_brackets.get()),
).pack(side=tk.LEFT)

ruuning_label = tk.Label(
    left_frame, text="Toxic Typer is running...", font=("Courier", 10, "bold"), fg="green", bg="#313131"
)

is_enabled = tk.StringVar()
is_enabled.set("START")

def toggle():
    if is_enabled.get() == "START":
        toxic_typer.start()
        is_enabled.set("STOP")
        ruuning_label.pack()
        print("Toxic Typer is enabled.")
    else:
        toxic_typer.stop()
        is_enabled.set("START")
        ruuning_label.pack_forget()
        print("Toxic Typer is disabled.")

tk.Button(
    left_frame, textvariable=is_enabled, font=("Arial", 12, "bold"), command=toggle, width=20
).pack(pady=(15, 10))

class ScrolledFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Create a canvas and scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Configure the canvas
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Clipboard history column using a Notebook for tabs
clipboard_history_label = tk.Label(clipboard_frame, text="Clipboard Content", font=("Courier", 13, "bold"), fg="#eeeeee", bg="#313131", )
clipboard_history_label.pack(pady=10)

style = ttk.Style()

# Ensure your style changes apply to the correct theme
style.theme_use("default")

# Configure the TNotebook tab
style.configure(
    "TNotebook.Tab",
    background="#313131",   # Tab background color
    foreground="#eeeeee",   # Tab text color
    padding=[2, 2],        # Padding around the tab text
)

# Configure the selected tab
style.map(
    "TNotebook.Tab",
    background=[("selected", "#217346")],  # Selected tab background color
    foreground=[("selected", "#ffffff")],  # Selected tab text color
)

clipboard_notebook = ttk.Notebook(clipboard_frame)  # Create a Notebook
clipboard_notebook.pack(fill=tk.BOTH, expand=True, padx=(5, 5), pady=(5, 10))  # Add padding

text_widgets = []

copied_items = []

def update_clipboard_history():
    try:
        # Get the current clipboard content
        clipboard_content = root.clipboard_get()

        # If it's a new item, add it to the history
        if clipboard_content and clipboard_content not in copied_items:
            copied_items.append(clipboard_content)
            # Create a new tab for the copied content
            tab = ttk.Frame(clipboard_notebook)
            clipboard_notebook.add(tab, text=f"Tab {len(copied_items)}")  # Set tab title

            # Create a ScrolledFrame for the new tab
            scrolled_frame = ScrolledFrame(tab)
            scrolled_frame.pack(fill=tk.BOTH, expand=True)  # Ensure the ScrolledFrame expands to fill the tab

            # Create a Text widget for clipboard content
            text_widget = tk.Text(
                scrolled_frame.scrollable_frame,
                wrap=tk.WORD,  # Enable word wrapping
                padx=10,
                pady=10,
                bg="#313131",
                fg="#eeeeee",
            )
            text_widget.pack(fill=tk.BOTH, expand=True)  # Ensure it fills the space

            # Insert the copied content into the Text widget
            text_widget.insert(tk.END, clipboard_content)

            # Make the Text widget read-only (optional)
            text_widget.config(state=tk.DISABLED)  # Disable editing

            # Store the reference to the Text widget
            text_widgets.append(text_widget)

            # Scroll to the latest entry
            clipboard_notebook.select(tab)  # Automatically switch to the new tab
    except tk.TclError:
        # Handle the case when clipboard is empty or invalid content
        pass

    # Check again after 1 second
    root.after(1000, update_clipboard_history)

def enable_clipboard_history():
    try:
        subprocess.run(
            ["powershell", "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Clipboard' -Name 'EnableClipboardHistory' -Value 1"], check=True
        )
        print("Clipboard history enabled")
    except subprocess.CalledProcessError as e:
        print(f"Error enabling clipboard history: {e}")

enable_clipboard_history()

def switch_tab(event):
    if event.state == 12:  # Ctrl pressed
        tab_index = event.keysym[-1]  # Get the last character of the key (e.g., '1' from '1')
        if tab_index.isdigit():
            index = int(tab_index) - 1  # Convert to zero-based index
            if 0 <= index < len(copied_items):
                clipboard_notebook.select(index)

                # Get the content of the selected tab
                if index < len(text_widgets):
                    text_widget = text_widgets[index]
                    text_widget.config(state=tk.NORMAL)  # Temporarily enable editing to read the content
                    content = text_widget.get("1.0", tk.END).strip()  # Get the content
                    text_widget.config(state=tk.DISABLED)  # Disable editing again

                    # Set the content to be typed
                    toxic_typer.set_text_to_type(content)  # Set content to type

# Bind the key combination for Ctrl + Number
root.bind('<Control-KeyPress>', switch_tab)

# Start updating the clipboard history
update_clipboard_history()

try:
    print("Toxic Typer is running...")
    root.mainloop()
except KeyboardInterrupt:
    pass
print("Toxic Typer is stopped.")