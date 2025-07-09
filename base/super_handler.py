import sublime
import sublime_plugin

import re
from typing import List

from ..model import RegexListItem

class _Super_ExtendedListHandler(sublime_plugin.ListInputHandler):
    sourceCommand = None
    acceptedInput = None

    def accept_input(self, view: sublime.View) -> bool: return True

    def __init__(self, command = None, *args, **kwargs):
        if (isinstance(command, sublime_plugin.Command)):
            self.sourceCommand = command
        else:
            self.sourceCommand = None
        self.acceptedInput = None
        _manager_set_active_handler(self)
        super().__init__(*args, **kwargs)

    def _on_modified(self, view: sublime.View):
        if self.accept_input(view) and self.validate(view.substr(view.full_line(0))):
            self.acceptedInput = view.substr(view.full_line(0))
            sublime.active_window().run_command("hide_overlay")

    def _cleanup(self):
        _manager_set_inactive()

    def cancel_(self):
        if (isinstance(self.acceptedInput, str)):
            self.confirm_(self.acceptedInput, None)
        else:
            self._cleanup()
            super().cancel_()

    def confirm_(self, v, event):
        self._cleanup()
        if self.want_event():
            self.confirm(v, event)
        else:
            self.confirm(v)
        if (self.acceptedInput != None
                and isinstance(self.sourceCommand, sublime_plugin.TextCommand)
                or isinstance(self.sourceCommand, sublime_plugin.ApplicationCommand)
                or isinstance(self.sourceCommand, sublime_plugin.WindowCommand)):
            view = sublime.active_window().active_view()
            if (view != None): view.run_command(self.sourceCommand.name(), {self.name(): v})

class _Super_RegexListHandler(sublime_plugin.TextInputHandler):
    sourceCommand = None
    acceptedItem = None
    acceptedInput = None
    currentInput = ""

    def list_items(self) -> List[str]:
        return []

    def name(self) -> str:
        return super().name() + "_value"

    def item_name(self) -> str:
        if self.name().endswith("_value"):
            return self.name()[0:-6] + "_item"
        else: return self.name() + "_item"

    def match_preview(self, matched_item: RegexListItem) -> str:
        return ""

    def list_styles(self) -> str:
        return ""

    def __init__(self, command = None, *args, **kwargs):
        if (isinstance(command, sublime_plugin.Command)):
            self.sourceCommand = command
        else:
            self.sourceCommand = None
        self.acceptedInput = None
        _manager_set_active_handler(self)
        super().__init__(*args, **kwargs)

    def _on_modified(self, view: sublime.View):
        self.currentInput = view.substr(view.full_line(0))

        completedItem = ""
        for item in self.list_items():
            if (isinstance(item.complete_regex, re.Pattern) and item.complete_regex.fullmatch(self.currentInput)):
                completedItem = item.title
                break

        if (completedItem != ""):
            self.acceptedItem = completedItem
            self.acceptedInput = self.currentInput
            sublime.active_window().run_command("hide_overlay")

    def _cleanup(self):
        _manager_set_inactive()

    def cancel_(self):
        if (isinstance(self.acceptedInput, str) and isinstance(self.acceptedItem, str)):
            self.confirm_(self.acceptedInput, None)
        else:
            self._cleanup()
            super().cancel_()

    def confirm_(self, v, event):
        self._cleanup()

        if self.want_event():
            self.confirm(v, event)
        else:
            self.confirm(v)

        if (self.acceptedInput != None
                and isinstance(self.sourceCommand, sublime_plugin.TextCommand)
                or isinstance(self.sourceCommand, sublime_plugin.ApplicationCommand)
                or isinstance(self.sourceCommand, sublime_plugin.WindowCommand)):
            view = sublime.active_window().active_view()
            if (view != None): view.run_command(self.sourceCommand.name(), {self.item_name(): self.acceptedItem, self.name(): v})


    def preview(self, text: str):
        matched = []

        if (text != ""):
            for i in range(0, len(self.list_items())):
                if (self.list_items()[i].match(text)):
                    matched.append(self.list_items()[i])
        else:
            matched = self.list_items()

        ret = """
            <html>
                <body>
                    <style>
                    """ + self.list_styles() + """
                    </style>
            """

        for i in range(0, len(matched)):
            if (i != 0):
                ret += "\n<div class=\"hr\"></div>\n"
            ret += "<div class=\"row\">" + self.match_preview(matched[i]) + "</div>"

        return sublime.Html(ret + """
                </body>
            </html>
            """)


############################
### Input Handler Manager

global activeHandler
activeHandler = None

def _manager_set_active_handler(newHandler):
    if (newHandler == None
        or issubclass(type(newHandler), _Super_ExtendedListHandler)
        or issubclass(type(newHandler),_Super_RegexListHandler)):
        global activeHandler
        activeHandler = newHandler

def _manager_set_inactive():
    _manager_set_active_handler(None)

def _manager_pass_on_modified(view: sublime.View):
    global activeHandler
    if (issubclass(type(activeHandler), _Super_ExtendedListHandler)
        or issubclass(type(activeHandler), _Super_RegexListHandler)):
        activeHandler._on_modified(view)
