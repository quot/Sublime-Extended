import sublime_plugin
import traceback

class _Super_ExtendedTextCommand(sublime_plugin.TextCommand):
    def visible_to_palette(self) -> bool: return True

    def is_visible_(self, args):
        # TODO:
        # Replace with co_qualname when it becomes available
        # https://docs.python.org/3/library/inspect.html#types-and-members
        #
        # This seems to be the best way to tell if a keypress is the origin
        # of the command event. Requests from the command palette will originate
        # from the `is_visible_` method.
        # Ideally, this can be replaced with something that is sure the request
        # is from a key press.
        return (self.visible_to_palette() or (traceback.extract_stack()[0].name == "run_")) and super().is_visible_(args)
