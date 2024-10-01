import pyperclip
from pynput.keyboard import Controller, Key, Listener
from typing import Union


KEYS_MAP = {
    "Right Ctrl": Key.ctrl_r,
    "Esc": Key.esc,
    "Right Shift": Key.shift_r,
}
MODES = ["normal", "ace-editor"]

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
        self.text_to_type = ""
        self.listener = None
        self.__modes = MODES
        self.__keys_map = KEYS_MAP
        self.__line_break = line_break
        self.__remove_everything = remove_everything
        self.__remove_auto_brackets = remove_auto_brackets
        self.set_mode(mode)
        self.set_shortcut_key(shortcut_key)

    def on_release(self, key):
        if key == self.__shortcut_key:
            self.paste_from_clipboard()

    def paste_from_clipboard(self):
        print("Pasting from clipboard using mode:", self.__mode)
        text = self.text_to_type if self.text_to_type else pyperclip.paste()  # Use the stored text if available
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

    def set_text_to_type(self, text: str):
        """Set the text to be typed when the shortcut key is pressed."""
        self.text_to_type = text

    def switch_tab(self, tab_content: str):
        # Store the content to type
        self.set_text_to_type(tab_content)
        print(f"Switched tab")

    def set_mode(self, mode):
        if mode in self.__modes or (isinstance(mode, int) and mode < len(self.__modes)):
            if isinstance(mode, int):
                mode = self.__modes[mode]
            self.__mode = mode
            print("Mode set to:", mode)
        else:
            raise Exception("Invalid mode:", mode)

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

    def start(self):
        if self.listener:
            self.listener.stop()

        self.listener = Listener(on_release=self.on_release)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

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
