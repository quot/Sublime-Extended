import sublime
import sublime_plugin

class _Super_ExtendedListHandler(sublime_plugin.ListInputHandler):
    acceptedInput = None

    def accept_input(self, view: sublime.View) -> bool: return True

    def __init__(self, *args, **kwargs):
        self.acceptedInput = None
        _manager_set_active_handler(self)
        super().__init__(*args, **kwargs)

    def _on_modified(self, view: sublime.View):
        if self.accept_input(view):
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

############################
### Input Handler Manager

global activeHandler
activeHandler = None

def _manager_set_active_handler(newHandler):
    if (newHandler == None) or issubclass(type(newHandler), _Super_ExtendedListHandler):
        global activeHandler
        activeHandler = newHandler

def _manager_set_inactive():
    _manager_set_active_handler(None)

def _manager_pass_on_modified(view: sublime.View):
    global activeHandler
    if (issubclass(type(activeHandler), _Super_ExtendedListHandler)):
        activeHandler._on_modified(view)
