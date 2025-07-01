Extend the functionality of the Sublime Text plugin APIs using hacky workarounds.

## Added Features

### ExtendedTextCommand

- Hide from the command palette while still usable through a keybind.
	- Useful if you want a command to use an InputHandler but you don't want it to always show in the Command Palette.

### ExtendedListHandler

- ListHandler with a callback function for any text modifications to the overlay's view.
	- Allows for reading/modifying the overlay's text input as well as accepting input before the user presses enter.
	- Requires `from <Plugin>.subl_ext.setup import *` to be called from a package/plugin's root for the text listener to be enabled.
