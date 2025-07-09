import sublime

from typing import List

from .model import RegexListItem
from .base.super_command import _Super_ExtendedTextCommand
from .base.super_handler import _Super_ExtendedListHandler
from .base.super_handler import _Super_RegexListHandler

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


class RegexListHandler(_Super_RegexListHandler):
    """
    Input handler that displays a list of items that can be searched
    with custom regex for each item.

    ## Setup

    ### Creation

    The andler must be initialized with the calling command passed
    in for the text to be returned.

    ```python
    class ExampleCommand(sublime_plugin.TextCommand):
        def input(self, args):
            return RegexListHandler(self)
    ```

    ### Run Function

    This handler will return up to 2 values when input is recieved.
    One for the item selected and one for the user's input into the search box.

    - `*_value` and `*_item` -> Returned when the user's input matches with a list item's `complete_regex`.

    - `*_value` with no item -> Returned when the user presses enter before a `complete_regex` is matched.

    To handle these situations, have your command's `run` always accept the `_value`
    with a default value used for the `_item`.

    ```python
    def run(self, edit, regex_list_value, regex_list_item=None):
    ```
    """

    def list_items(self) -> List[RegexListItem]:
        """
        This method should return the items to show in the list.
        """
        return []

    def match_preview(self, matched_item: RegexListItem) -> str:
        """
        Returns HTML string used to display an item that matched on
        the user's input.
        """

        row_title_text = "<div class=\"title\">{title}</div>"
        row_desc_text = "<div class=\"desc\">{desc}</div>"

        if (self.currentInput == ""):
            return row_title_text.format(title = matched_item.title) + row_desc_text.format(desc = matched_item.desc)
        else:
            title = row_title_text.format(title = matched_item.title)
            if (isinstance(matched_item.match_desc, str)):
                return title + row_desc_text.format(desc = matched_item.match_desc.format(text=self.currentInput))
            else:
                return title + row_desc_text.format(desc = self.currentInput)

    def list_styles(self) -> str:
        """
        Returns the CSS used to style list items.
        """

        return """
            html {
                --highlight-color: color(var(--foreground) min-contrast(var(--foreground) 7.5));
            }

            div.hr {
                background-color: var(--highlight-color);
                padding-top: 1px;
                margin-top: .7em;
                margin-bottom: .3em;
            }

            div.title {
                display: inline-block;
                border-radius: .2em;
                background-color: var(--highlight-color);
                color: var(--foreground);
                padding: .2em;
                padding-left: .4em;
                padding-right: 0em;
                margin-right: .85em;
                /*font-weight: bold;*/
                font-size: 1.1em;
            }

            div.desc {
                display: inline-block;
            }
        """
