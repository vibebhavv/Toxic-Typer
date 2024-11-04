from pynput.keyboard import Controller, Key, Listener
from typing import Union

# mapping shortcut keys
KEYS_MAP = {
    "Right Ctrl": Key.ctrl_r,
    "Esc": Key.esc,
    "Right Shift": Key.shift_r,
}

# defining modes
MODES = ["normal", "ace-editor"]

# Defining main logic
class TOXICTyper:
    def __init__(
        self,
        mode: Union[str, int] = MODES[0],
        shortcut_key: str = "Right Ctrl",
        line_break: bool = True,
        remove_everything: bool = False,
        remove_auto_brackets: bool = False,
    ) -> None:
        self.typer = Controller()
        self.listener = None
        self.tab_listener = None
        self.__modes = MODES
        self.__keys_map = KEYS_MAP
        self.__line_break = line_break
        self.__remove_everything = remove_everything
        self.__remove_auto_brackets = remove_auto_brackets
        self.set_mode(mode)
        self.ctrl_pressed = False
        self.set_shortcut_key(shortcut_key)
        self.tabs = None
        self.text_widgets = []  # Add timestamp for debouncing
        
    # Tab changing logic
    def set_tabs(self, notebook):
        self.tabs = notebook

    def add_text_widget(self, text_widget):
        self.text_widgets.append(text_widget)

    def get_selected_tab_content(self):
        if self.tabs is not None:
            try:
                current_tab_index = self.tabs.index(self.tabs.select())
                if 0 <= current_tab_index < len(self.text_widgets):
                    text_widget = self.text_widgets[current_tab_index]
                    return text_widget.get("1.0", "end-1c")
            except Exception as e:
                print(f"Error getting tab content: {e}")
        return None

    def change_tab(self, index):
        if self.tabs is None:
            return
        try:
            tab_count = len(self.tabs.tabs())
            if 0 <= index < tab_count:  # Validate index is within bounds
                self.tabs.select(index)
                print(f"Switched to Tab {index+1}")
            else:
                print(f"Tab {index+1} does not exist. Available tabs: {tab_count}")
        except Exception as e:
            print(f"Error switching tabs: {e}")

    def tab_change(self, key):
        try:
            # Handle Ctrl key press
            if key == Key.ctrl_l:
                self.ctrl_pressed = True
                return
            
            # Handle Ctrl key release
            if hasattr(key, 'name') and key.name == 'ctrl_l':
                self.ctrl_pressed = False
                return

            # Handle number keys only when ctrl is pressed
            if self.ctrl_pressed and hasattr(key, 'vk') and key.vk is not None:
                # Map virtual key codes for number keys (1-9)
                if 49 <= key.vk <= 57:  # VK codes for 1-9
                    index = key.vk - 49  # Convert to 0-based index
                    self.change_tab(index)
        except Exception as e:
            print(f"Error in tab_change: {e}")

    # typer trigger logic
    def on_release(self, key):
        if key == self.__shortcut_key:
            self.paste_from_clipboard()
        elif key == Key.ctrl_l:
            self.ctrl_pressed = False
    
    # typing logic
    def paste_from_clipboard(self):
        print("Pasting from clipboard using mode:", self.__mode)
        text = self.get_selected_tab_content()
        if text is None:
            print("No text available in the selected tab")
            return

        # typer configuration logics
        if self.__remove_everything:
            with self.typer.pressed(Key.ctrl):
                self.typer.tap("a")
            self.typer.tap(Key.backspace)

        if self.__mode == "ace-editor":
            textlines = text.split("\n")
            for line in textlines:
                with self.typer.pressed(Key.alt):
                    self.typer.tap(Key.backspace)
                self.typer.type(line)
                if self.__line_break:
                    self.typer.tap(Key.enter)
        else:
            self.typer.type(text)

        if self.__remove_auto_brackets:
            with self.typer.pressed(Key.ctrl):
                with self.typer.pressed(Key.shift):
                    self.typer.tap(Key.end)
            self.typer.tap(Key.backspace)


    # mode logic
    def set_mode(self, mode):
        if mode in self.__modes or (isinstance(mode, int) and mode < len(self.__modes)):
            if isinstance(mode, int):
                mode = self.__modes[mode]
            self.__mode = mode
            print("Mode set to:", mode)
        else:
            raise Exception("Invalid mode:", mode)

    # shortcut key logic
    def set_shortcut_key(self, key):
        if key in self.__keys_map.keys():
            self.__shortcut_key = self.__keys_map[key]
            print("Shortcut key set to:", key)
        else:
            raise Exception("Invalid shortcut key:", key)

    def set_line_break(self, line_break):
        self.__line_break = bool(line_break)
        print("Line break set to:", bool(line_break))
    
    def set_remove_everything(self, remove_everything):
        self.__remove_everything = bool(remove_everything)
        print("Remove everything set to:", bool(remove_everything))
    
    def set_remove_auto_brackets(self, remove_auto_brackets):
        self.__remove_auto_brackets = bool(remove_auto_brackets)
        print("Remove auto brackets set to:", bool(remove_auto_brackets))

    # start typer logic
    def start(self):
        if self.listener:
            self.listener.stop()
        
        self.listener = Listener(on_release=self.on_release)
        self.listener.start()

        # Start the tab listener
        self.tab_listener = Listener(on_press=self.tab_change)
        self.tab_listener.start()
    
    # typer stoppping logic
    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
        if self.tab_listener:
            self.tab_listener.stop()
            self.tab_listener = None

    @property
    def mode(self):
        return self.__mode
    
    @property
    def modes(self):
        return self.__modes

    @property
    def shortcut_key(self):
        for key, value in self.__keys_map.items():
            if value == self.__shortcut_key:
                return key

    @property
    def shortcut_keys(self):
        return list(self.__keys_map.keys())

    @property
    def line_break(self):
        return self.__line_break
    
    @property
    def remove_everything(self):
        return self.__remove_everything
    
    @property
    def remove_auto_brackets(self):
        return self.__remove_auto_brackets
