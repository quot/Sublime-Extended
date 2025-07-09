from typing import Optional
from re import Pattern

class RegexListItem():
    """
    List entries used with `RegexListHandler`.

    :param title:
        Value title display within the list. Also used as the `*_item` key
        passed back to a command.
    :param desc:
        Initial description for the item before user input.
    :param search_regex:
        Regex pattern used to determine if the item displays with the
        current user input.
    :param match_desc:
        Optional description used when `search_regex` matches on a user's
        input. Use `{text}` within the string to have the user input inserted
        into the description.
    :param complete_regex:
        Optional regex used to automatically accept a user's input and confirm
        that this item is to be used. List order will determine priority when
        matching multiple entries.
    """

    def __init__(self, title: str, desc: str, search_regex: Pattern, match_desc: Optional[str] = None, complete_regex: Optional[Pattern] = None):
        self.title = title
        self.desc = desc
        self.match_desc = match_desc
        self.search_regex = search_regex

        if (isinstance(complete_regex, Pattern)):
            self.complete_regex = complete_regex
        else:
            self.complete_regex = None

    def match(self, text: str) -> bool:
        return self.search_regex.fullmatch(text) != None
