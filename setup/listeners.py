import sublime
import sublime_plugin

from ..base import super_handler

class PaletteListener(sublime_plugin.EventListener):
    def on_modified(self, view: sublime.View):
        if (view.element() == "command_palette:input"):
            super_handler._manager_pass_on_modified(view)
