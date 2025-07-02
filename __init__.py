import sublime

from .base.super_command import _Super_ExtendedTextCommand
from .base.super_handler import _Super_ExtendedListHandler

class ExtendedTextCommand(_Super_ExtendedTextCommand):
    """
    Command that can be used with an input handler without displaying in the command palette.

    - Use `visible_to_palette -> False` to hide the command
    """

    def visible_to_palette(self) -> bool:
        """
        Determine if this command should show in the command palette when
        the command is set up in a sublime-commands file.
        """
        return True

class ExtendedListHandler(_Super_ExtendedListHandler):
    """
    List Handler with a text listener that is triggered on any modification
    to the overlay's view.
    """

    def accept_input(self, view: sublime.View) -> bool:
        """
        Called when the handler is active and text input is modified.
        Completes the input handler when ``True`` is returned. When completed
        this way, the user's text input will be passed to `confirm`.

        Handler must be initialized with the calling command passed
        in for the text to be returned.

        ```python
        class ExampleCommand(sublime_plugin.TextCommand):
            def input(self, args):
                return ExtendedListHandler(self)
        ```
        """
        return True
