"""
Author: Vaibhav Pathak
Github: https://www.github.com/G0dVai
About: Auto-Typer for codetantra web and codetantra-sea with great features.

[!] Tested on Windows and linux only yet.
"""

import tkinter as tk
from tkinter import ttk
import webbrowser

# Importing logic file and icons
from assets.icon import icon
from toxic_typer import TOXICTyper

toxic_typer = TOXICTyper(mode=1)

# Main GUI window
root = tk.Tk()
root.title("Toxic Typer")
root.geometry("800x400")
root.resizable(False, False)
root.config(bg="#313131")

# calling icon
img = tk.PhotoImage(data=icon)
root.tk.call("wm", "iconphoto", root._w, img)

# Configure style for ttk elements
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground="#313131", background="#313131", foreground="#313131", font=("Arial", 14))

# creating 2 frames left and clipboard_frame
left_frame = tk.Frame(root, bg="#313131")
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10,0))  # Added left padding

# clipboard frame
clipboard_frame = tk.Frame(root, bg="#313131")
clipboard_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=(10, 10))

# heading
tk.Label(left_frame, text="Toxic Typer", font=("Courier", 30, "bold"), bg="#313131", fg="#eeeeee").pack(anchor=tk.W, padx=(50,0))

# profile text
profile_link = tk.Label(left_frame, text="This helping hand is developed by G0dVai", fg="yellow", cursor="hand2", bg="#313131")
profile_link.pack(anchor=tk.W, padx=(60, 0))
profile_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/G0dVai"))

tk.Label(left_frame, text="Press LCTRL + Left/Right Arrow", font=("Arial", 12), bg="#313131", fg="#eeeeee").pack(pady=(5, 0))

tk.Label(left_frame, text="Press shortcut key to paste from the selected tab", font=("Arial", 12), bg="#313131", fg="#eeeeee").pack(pady=(0, 10))

# Controls in left frame
# For Mode Selection
mode_frame = tk.Frame(left_frame, bg="#313131")
mode_frame.pack(anchor=tk.W, padx=20)

tk.Label(mode_frame, text="Mode: ", font=("Arial", 12), bg="#313131", fg="#eeeeee").pack(side=tk.LEFT)

mode_combo = ttk.Combobox(
    mode_frame,
    values=toxic_typer.modes,
    state="readonly", 
    style="TCombobox", 
    width=10
)
mode_combo.current(0)
mode_combo.pack(padx=10, ipadx=1, ipady=1)
mode_combo.bind("<<ComboboxSelected>>", lambda event: toxic_typer.set_mode(mode_combo.get()))  
mode_combo.current(toxic_typer.modes.index(toxic_typer.mode))

shortcut_frame = tk.Frame(left_frame, bg="#313131")
shortcut_frame.pack(anchor=tk.W, padx=20)

shortcut_key = tk.StringVar(value="Right Ctrl")

tk.Label(shortcut_frame, text="Shortcut key:", font=("Arial", 12), bg="#313131", fg="#eeeeee").pack(side=tk.LEFT)

shortcut_combo = ttk.Combobox(
    shortcut_frame, 
    values=toxic_typer.shortcut_keys,
    state="readonly", 
    style="TCombobox", 
    width=10
)
shortcut_combo.current(0)
shortcut_combo.pack(padx=10, pady=10)
shortcut_combo.bind("<<ComboboxSelected>>", lambda event: toxic_typer.set_shortcut_key(shortcut_combo.get()))  
shortcut_combo.current(toxic_typer.shortcut_keys.index(toxic_typer.shortcut_key))

line_break_frame = tk.Frame(left_frame)
line_break_frame.pack(anchor=tk.W, pady=3, padx=20)
line_break = tk.BooleanVar(value=toxic_typer.line_break)

tk.Checkbutton(
    line_break_frame, 
    text="Line Break", 
    font=("Arial", 12), 
    bg="#313131", 
    fg="#eeeeee",
    selectcolor="#313131",
    activebackground="#313131",
    activeforeground="#eeeeee",
    variable=line_break,
    command=lambda: toxic_typer.set_line_break(line_break.get()),
).pack(side=tk.LEFT)

remove_everything_frame = tk.Frame(left_frame)
remove_everything_frame.pack(anchor=tk.W, pady=3, padx=20)
remove_everything = tk.BooleanVar(value=toxic_typer.remove_everything)

tk.Checkbutton(
    remove_everything_frame, 
    text="Remove everything before pasting", 
    font=("Arial", 12), 
    bg="#313131", 
    fg="#eeeeee",
    activebackground="#313131",
    activeforeground="#eeeeee",
    selectcolor="#313131",
    variable=remove_everything,
    command=lambda: toxic_typer.set_remove_everything(remove_everything.get())
).pack(side=tk.LEFT)

remove_auto_bracket_frame = tk.Frame(left_frame)
remove_auto_bracket_frame.pack(anchor=tk.W, pady=3, padx=20)
remove_auto_bracket = tk.BooleanVar(value=toxic_typer.remove_auto_brackets)

tk.Checkbutton(
    remove_auto_bracket_frame, 
    text="Remove Auto Brackets", 
    font=("Arial", 12), 
    bg="#313131", 
    fg="#eeeeee",
    activebackground="#313131",
    activeforeground="#eeeeee",
    selectcolor="#313131",
    variable=remove_auto_bracket,
    command=lambda: toxic_typer.set_remove_auto_brackets(remove_auto_bracket.get())
).pack(side=tk.LEFT)


# Right section for clipboard
# Clipboard content heading
tk.Label(clipboard_frame, text="Clipboard Content", font=("Courier", 12, "bold"), bg="#313131", fg="#eeeeee").pack()

# Start Button status label
running_label = tk.Label(left_frame, text="Typer is running...", font=("Courier", 10, "bold"), fg="yellow", bg="#313131")

is_enabled = tk.StringVar()
is_enabled.set("START")

# Start\Stop button 
def toggle():
    if is_enabled.get() == "START":
        toxic_typer.start()
        is_enabled.set("STOP")
        running_label.pack()
        print("Toxic Typer is enabled.")
    else:
        toxic_typer.stop()
        is_enabled.set("START")
        running_label.pack_forget()
        print("Toxic Typer is disabled.")

tk.Button(
    left_frame, 
    textvariable=is_enabled, 
    font=("Arial", 12, "bold"), 
    command=toggle, 
    width=20
).pack(pady=(30, 10))


# Clipboard widget
clipboard_notebook = ttk.Notebook(clipboard_frame)
clipboard_notebook.pack(fill=tk.BOTH, expand=True, padx=(50, 30), pady=(10, 10))

text_widgets = []
copied_items = []

# clipboard content checker
def update_clipboard_history():
    try:
        clipboard_content = root.clipboard_get()
        if clipboard_content and clipboard_content not in copied_items:
            copied_items.append(clipboard_content)
            tab = ttk.Frame(clipboard_notebook)
            clipboard_notebook.add(tab, text=f"Tab {len(copied_items)}")
            
            # Add a Text widget with a Scrollbar for each tab
            text_widget = tk.Text(
                tab,
                wrap=tk.WORD,
                padx=10,
                pady=10,
                bg="#2b2b2b",
                fg="#eeeeee",
                font=("Courier", 12)
            )
            text_widget.insert("1.0", clipboard_content)
            text_widget.config(state="disabled")
            
            # Add the text widget to both lists
            text_widgets.append(text_widget)
            toxic_typer.add_text_widget(text_widget)  # Add to TOXICTyper's list
            
            text_widget.pack(fill=tk.BOTH, expand=True)

            # Update the tabs in the switch_tab module
            toxic_typer.set_tabs(clipboard_notebook)

    except tk.TclError:
        pass

    root.after(1000, update_clipboard_history)
update_clipboard_history()

# Try running main GUI
try:
    print("Toxic Typer is running...")
    root.mainloop()
except KeyboardInterrupt:
    pass
print("Toxic Typer is stopped.")
