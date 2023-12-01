# import os
# import re
# import pickle


# from collections import UserDict
# from datetime import date, datetime
#######################
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
    # from .notes_class import NoteBook, add, edit, search_note, delete
    # from .sort_folder import main as sort_files
    #hw_1_01
# try:
from .birthday import get_birthdays_per_week as birthday_from_now
from .convert import convert_str_dict
from .classes import AddressBook, Record
from .notes_class import NoteBook, add, edit, search_note,delete
    # from notes_class import NoteBook, add, edit, search_note, delete
    # from sort_folder import main as sort_files
# except:
# from birthday import get_birthdays_per_week as birthday_from_now
# from convert import convert_str_dict
# from classes import AddressBook, Record
# from notes_class import NoteBook, add, edit, search_note,delete
#######################
from abc import ABC, abstractmethod

class BotView(ABC):
    # @staticmethod
    @abstractmethod
    def display_content(data):
        print(data)

class BotInput(ABC):
    # @staticmethod
    @abstractmethod
    def input(data):
        return input(data)


    # @staticmethod
    @abstractmethod
    def prompt(data, completer=None):
        if completer:
            return prompt(data, completer=completer)
        else:
            return input(data)


records = AddressBook()
notes_obj = NoteBook()


def search_user(*args):
    global records
    return records.search(*args)


def save_ab(*args):
    records.save_address_book()
    return "Address book saved successful"

def save_notes(*args):
    global notes_obj
    notes_obj.save_notes()
    return "Notes book saved successful"


def load_ab(*args):
    global records
    load_records = records.load_address_book()
    if load_records is not None:
        records = load_records
        return "Address book loaded successfully"
    else:
        return "Failed to load address book"
    
def load_notes(*args):
    global notes_obj
    load_records = notes_obj.load_notes()
    if load_records is not None:
        notes_obj = load_records
        return "Note book loaded successfully"
    else:
        return "Failed to load note book"


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        # except AttributeError:
            # return "ab empty"
        except IndexError:
            return "Give me name and phone please"
        except KeyError:
            return "Enter correct user name"
        except RuntimeError:
            return "Nothing more. End of list"
        except StopIteration as e:
            if str(e) == "End of list":
                return "End of list"
            if str(e) == "Empty list":
                return "Empty list"
            else:
                raise e
        except ValueError as e:
            if str(e) == "Not enough number":
                return "Not enought number"
            if str(e) == "Invalid data format":
                return "Invalid data format"
            if str(e) == "Invalid phone number, should contain 10 digits":
                return "Invalid phone number, should contain 10 digits"
            if str(e) == "Mail should have the following format nickname@domen.yy":
                return "Mail should have the following format nickname@domen.yy"
            if str(e) == "wrong name, try again":
                return "wrong name, try again"
            else:
                raise e  # Піднімаэмо помилку наверх, якщо вона іншого типу
    return inner




def sanitize_phone_number(phone):
    collected_phone = ""
    for ch in phone:
        collected_phone += ch
    new_phone = (
        collected_phone.strip()
            .removeprefix("+38")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
    )
    return new_phone
    

def sanitize_db(db):
    collected_db = ""
    for ch in db:
        collected_db += ch
    new_db = (
        collected_db.strip()
            .replace(" ", "-")
            .replace("(", "")
            .replace(")", "")
            .replace(".", "-")
            .replace(",", "-")
            .replace("/", "-")
            .replace("\\", "-")
    )
    return (new_db)
    

@user_error
def add_record(*args):
    global records
    name = args[0]
    phone_number = sanitize_phone_number(args[1:])
    # phone_number = (args[1:])
    if not records.data.get(name):
        name_record = Record(name)
        name_record.add_phone(phone_number)
        records.add_record(name_record)
        # pho = name_record.add_phone(phone_number)
        # return(records.add_record(name_record), pho)
    else:
        name_record = records.data.get(name)
        return(name_record.add_phone(phone_number))
    return f"Add record {name = }, {phone_number = }"


@user_error 
def bd_add(*args):
    global records
    name = args[0]
    bd = sanitize_db(args[1:])
    if not records.data.get(name):
        name_record = Record(name)
        name_record.add_birthday(bd)
        records.add_record(name_record)
    else:
        name_record = records.data.get(name)
        name_record.add_birthday(bd)
    return f"Add record {name = }, {bd = }"


def loc_add(*args):
    global records
    name = args[0]
    loc = args[1:]
    location = ""
    for ch in loc:
        location +=  " " + ch
    if not records.data.get(name):
        name_record = Record(name)
        name_record.add_location(location)
        records.add_record(name_record)
    else:
        name_record = records.data.get(name)
        name_record.add_location(location)
    return f"Add record {name = }, {location = }"

@user_error 
def mail_add(*args):
    global records
    name = args[0]
    mail = str(args[1])
    if not records.data.get(name):
        name_record = Record(name)
        name_record.add_mail(mail)
        records.add_record(name_record)
    else:
        name_record = records.data.get(name)
        name_record.add_mail(mail)
    return f"Add record {name = }, {mail = }"


@user_error
def mail_change(*args):
    global records
    name = args[0]
    old_mail = str(args[1])
    new_mail = str(args[2])
    if not records.data.get(name):
        raise ValueError("wrong name, try again")
    else:
        try:
            name_record = records.data.get(name)
            try:
                name_record.edit_mail(old_mail, new_mail)
                return f"Change record {name = }, {new_mail = }"
            except:
                return f"The mail {new_mail} is not valid."
        except:
            return f"The mail {old_mail} is not found."


def days_to_bd(*args):
    global records
    try:
        name = args[0]
        if name:
            if records.data.get(name):
                name_record = records.data.get(name)
                try:
                    result = name_record.days_to_birthday()
                    if result:
                        if result == "today":
                            return f"To {name } birthday today"
                        else:
                            return f"To {name } birthday,  left {result} days"
                    else:
                        return f"To {name } no data birthday"
                except:# AttributeError as e:
                    return(f"No birthday date for {name}")
            else:
                return(f"No contact find {name}")
    except:# AttributeError as e:
        return("No contact input")


@user_error
def change_record(*args):
    global records
    name = args[0]
    old_phone_number = sanitize_phone_number(args[1])
    new_phone_number = sanitize_phone_number(args[2])
    if not records.data.get(name):
        raise ValueError("wrong name")
    else:
        try:
            name_record = records.data.get(name)
            try:
                name_record.edit_phone(old_phone_number, new_phone_number)
                return f"Change record {name = }, {new_phone_number = }"
            except:
                return f"The phone {new_phone_number} is not valid."
        except:
            return f"The phone {old_phone_number} is not found."


def delete_record(*args):
    global records
    name = args[0]
    records.delete(name)
    return f"Contact name: {name}, delete successfull"

def add_note(*args):
    global notes_obj
    tag = []
    text = ''
    for i in args:
        if "#" in i:
             tag.append(i)
        else:
            text += i+" "
    notes_obj, text = add(notes_obj, tag, text)
    return text


def edit_note(*args):
    global notes_obj
    tag = []
    text = ''
    for i in args:
        if "#" in i:
             tag.append(i)
        else:
            text += i+" "
    result, to_write = edit(notes_obj, tag, text)
    if result == "error":
        return to_write
    else:
        notes_obj = result
        return to_write


def search_note_(*args):
    global notes_obj
    tag = args
    result = search_note(notes_obj, tag)
    if result == "error":
        return f"Note not found with this tags: {tag}"
    else:
        return result

def delete_note(*args):
    global notes_obj
    tag = args
    result, text = delete(notes_obj, tag)
    # if notes_obj == result:
    #     print(f"Tags:{tag} not found")
    # else:
    notes_obj = result
    return text

def unknown_cmd(*args):
    return "Unknown command. Try again. Or use 'help'"


def hello_cmd(*args):
    return "How can I help you?"


def help_cmd(*args):
    return_str = "\n"
    cmd_list = [
            "avalible command:",
            "hello - just say hello",
            "help - show avalible cmd",
            "add - add record - format 'name phone'",
            "mail_add - add mail - format 'name nickname@domen.yy'",
            "mail_change - change mail - format 'name old mail new mail'",
            "bd_add - add birthday/or replace, if data olready exist - format 'name date birthday (YYYY-MM-DD)'",
            "location_add - add location/or replace, if data olready exist",
            "days_to_bd - days to birthday",
            "bd_in_days - show all users who has bd in n(7day max) days format 'bd_in_days 2(n days)'",
            "add_note - add note - format: #tags text",
            "serch_note - exact match for tags - format: #tags",
            "edit_note - exact match for tags - format: #tags",
            "delete_note - exact match for tags - format: #tags",
            "change - change record - format 'name old phone new phone'",
            "delete - delete record - format 'name'",
            "phone - get phone by name - format 'phone name'",
            "show_all - show all phone book",
            "show_notes - show all notes",
            "save_ab - save address book",
            "search - search by characters in name, or by digits in phone",
            "sort_folder - sort dirty folder by Audio, Docs, Archives, Music, Images, Other",
            "good bye/close/exit - shotdown this script",
            "load_ab - load address book",
                ]
    for ch in cmd_list:
        return_str += ch + "\n"
    return return_str


@user_error
def get_phone(*args):
    global records
    name = args[0]
    rec = records.find(name)
    if rec:
        return rec

# def sort_folder_by_path(*args):
#     path = str(input("Write path to folder: "))
#     if os.path.exists(path):
#         result = sort_files(path)
#         return result
#         # sort_files(path)
#     else:
#         return "Path not exist."  

# @user_error 
def show_all(*args):
    global records
    n = None
    try:
        n = int(args[0])
        if n is not None:
            return_lst_result = []
            if len(records) >= 1:
                for cont in records.iterator(n):
                    return_lst = []
                    for ch in cont:
                        new_ch = (str(ch).strip()
                                        .replace("(", "")
                                        .replace(")", "")
                                        .replace("'", "")
                                )
                        return_lst.append(new_ch)
                    return_lst_result.append(return_lst)
                return return_lst_result
            else:
                return "Empty"
    except:
        if n is  None:
            return_str = "\n"
            if len(records) >=1:
                for _, numbers in records.data.items():
                    return_str += str(numbers) + "\n"
                return return_str
            else:
                return "Empty"
        else:
            return return_lst_result #"No records to show"

# @user_error 
def show_notes(*args):
    return_str = "\n"
    if len(notes_obj.data) >=1:
        for tags, notes in notes_obj.data.items() :
            return_str += "Tags: " + str([tag for tag in tags]) + ", notes: " + str(notes) + "\n"
        return return_str
    else:
        return "Empty"
    

def close_cmd(*args):
    return "Good bye!"

#################################
def bd_in_days(*args):
    text = ''
    in_days = int(args[0])
    if in_days > 7:
        print("seven days max")
        in_days = 7
    # print(in_days)
    result_str = show_all()
    result_dct = convert_str_dict(result_str)
    # pprint(result_dct)
    out_result = birthday_from_now(result_dct, in_days)
    
    for k,v in out_result.items():
        text += k+" - Name: "
        for i in v:
            text += i+", "
        text = text[:-2]+"\n"
        out_result = text
    return out_result
#################################

COMMANDS = {
            add_note:"add_note",
            edit_note:"edit_note",
            search_note_:"search_note",
            delete_note:"delete_note",
            add_record: "add",
            bd_add: "bd_add",
            mail_add: "mail_add",
            loc_add: "location_add",
            mail_change: "mail_change",
            days_to_bd: "days_to_bd",
            bd_in_days: "bd_in_days",
            delete_record: "delete",
            change_record: "change",
            hello_cmd: "hello",
            get_phone: "phone",
            show_all: "show_all",
            save_ab: "save_ab",
            load_ab: "load_ab",
            save_notes: "save_notes",
            show_notes: "show_notes",
            load_notes: "load_notes",
            # sort_folder_by_path: "sort_folder",
            search_user: "search",
            help_cmd: "help",
            close_cmd: ("good bye", "close", "exit")
            }

cmd_list = ["hello", "help", "add", "add_note", "edit_note", "search_note", "delete_note", "mail_add", "mail_change", "bd_add", "location_add",
            "days_to_bd", "bd_in_days", "change", "delete", "phone", "show_all", "show_notes", "save_ab","save_notes", "search", "sort_folder", "load_ab", "load_notes", "good bye", "close", "exit"]

def parser(text: str):
    for func, kw in COMMANDS.items():
        if text.lower().startswith(kw):
            return func, text[len(kw):].strip().split()
    return unknown_cmd, []


def main():
    load_ab("1")
    load_notes("1")

    completer = WordCompleter(cmd_list)
    while True:
        user_input = BotInput.prompt("Write comand:", completer=completer)
        func, data = parser(user_input)
        if func == show_all and data:
            result1 = show_all(*data)
            if result1 != "Empty":
                for el in result1:
                    BotInput.input("Press Enter for see next records")
                    for cont in el:
                        print(cont)
                BotInput.input("Press Enter to exit, and input new command")
            else:
                BotView.display_content(func(*data))
        else:
            BotView.display_content(func(*data))
        if func == close_cmd:
            save_ab("1")
            save_notes("1")
            break


if __name__ == "__main__":
    #################################
    # try:
    #     records = load_ab("1")
    #     # notes_obj = load_notes(notes_obj)
    main()
    # except:
    #     records = AddressBook()
    #     main()
    #################################
