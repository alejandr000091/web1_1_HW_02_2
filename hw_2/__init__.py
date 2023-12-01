# #work
from .bot import main
from .birthday import get_birthdays_per_week# as birthday_from_now
from .convert import convert_str_dict
from .notes_class import NoteBook, add, edit, search_note,delete
from .classes import AddressBook, Record

__all__ = ["main", "get_birthdays_per_week", "convert_str_dict", "AddressBook", "Record", "NoteBook", "add", "edit", "search_note", "delete"]#, "notes_class", "classes"]
# __all__ = ["hw_1_01", "birthday", "convert", "notes_class", "classes"]