from collections import UserDict
from genericpath import exists
import os
import pickle

# const directory and filename 
# DIRECTORY = '.APP_HOME' #docker directory
DIRECTORY = 'C:\\py_robot'
FILE_NAME = "notes.bin"

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Tag(Field):
    def __repr__(self):
        return str(self.value)

class Note(Field):
    def __repr__(self):
        return str(self.value)

class Record_note:
    def __init__(self, tags: tuple, note: str) -> None:
        self.tags = [Tag(tag) for tag in tags] if tags else []
        self.note = Note(note)

    def __str__(self):
        return f"note: {self.note}, with tags: {' '.join(str(tag) for tag in self.tags)}"


class NoteBook(UserDict):
    def add_record(self, new_note: Record_note) -> None:
        self.data[tuple(new_note.tags)] = new_note.note
        return self

    def save_notes(self):  # noqa: F821
        # file_name = os.getenv("SystemDrive")+"\\py_robot\\notes.bin"
        # os.makedirs(os.path.dirname(file_name), exist_ok=True)
        self.file_name = os.path.join(DIRECTORY, FILE_NAME)
        os.makedirs(DIRECTORY, exist_ok=True)
        with open(self.file_name, "wb") as fh:
            pickle.dump(self, fh)
    
    def load_notes(self):
        # file_name = os.getenv("SystemDrive")+"\\py_robot\\notes.bin"
        self.file_name = os.path.join(DIRECTORY, FILE_NAME)
        os.makedirs(DIRECTORY, exist_ok=True)
        try:
            if os.path.exists(self.file_name):
                with open(self.file_name, "rb") as file:
                    unpacked = pickle.load(file)
                return unpacked
        except:
            return "File not found"


def add(notebooks : NoteBook, tag:dict, text:str):
    new_note = Record_note(tag, text)
    notebooks = notebooks.add_record(new_note)
    tgs = ''
    for i in tag:
        tgs += i+", "
    return notebooks, f"Added note, tags:{tgs[:-2]}\nText: {text}"

def edit(notebooks : NoteBook, tag:dict, new_text:str):
    result = notebooks
    data_str = ''
    for tt in tag:
        data_str += tt

    for tags, text in notebooks.items():
        tag_str = ''
        for t in tags:
            tag_str += t.value
        if data_str == tag_str:
            result[tags] = new_text
            return result, f"Tags:{tag_str}\nNew text: {new_text}"
    return "error", f"Note with tags:{tag_str} not found"

def search_note(notebooks : NoteBook, tag:dict):
    result = notebooks
    data_str = ''
    for tt in tag:
        data_str += tt

    for tags, text in notebooks.items():
        tag_str = ''
        for t in tags:
            tag_str += t.value
        if data_str == tag_str:
            return f"Tags:{tag_str}\nText: {text}"
    return "error"

def delete(notebooks : NoteBook, tag:dict):
    result = notebooks
    data_str = ''
    for tt in tag:
        data_str += tt

    for tags, text in notebooks.items():
        tag_str = ''
        for t in tags:
            tag_str += t.value
        if data_str == tag_str:
            result.pop(tags)
            return result, f"Note:{tag_str}, {text}, was deleted"
    return result, f"Tags: {tag_str}, not found"