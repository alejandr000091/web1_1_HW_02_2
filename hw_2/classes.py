import os
import re
import pickle


from collections import UserDict
from datetime import date, datetime

# const directory and filename 
# DIRECTORY = '.APP_HOME' #docker directory
DIRECTORY = 'C:\\py_robot'
FILE_NAME = "address_book.bin"

class Field():
    def __init__(self, value):
        self.__value = None
        self.value = value


    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, value):
        self.__value = value


    def __str__(self):
        return str(self.value)


class Name(Field):
    ...

class Location(Field):
    ...


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value
        

    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, new_value):
        collected_phone = ""
        for ch in new_value:
            collected_phone += ch
        sanitized_new_phone = (
            collected_phone.strip()
                .removeprefix("+38")
                .replace("(", "")
                .replace(")", "")
                .replace("-", "")
                .replace(" ", "")
        )
        if len(sanitized_new_phone) != 10 or not sanitized_new_phone.isdigit():
            raise ValueError("Invalid phone number, should contain 10 digits")
        else:
            self.__value = sanitized_new_phone

    
    def __str__(self):
        return f"Phone: {self.value}"


class Mail(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        patern_mail = r"[A-z.]+\w+@[A-z]+\.[A-z]{2,}"
        try:
            if bool(re.match(patern_mail, value)):
                self.__value = value
            else:
                raise ValueError("Mail should have the following format nickname@domen.yy")
        except ValueError as e:
            raise ValueError("Mail should have the following format nickname@domen.yy") from e


    # def __str__(self):
    #     return f"Mail: {self.__value}"
    def __str__(self) -> str:
        return f"Mail: {self.__value}"

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value
        

    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, new_value):
        collected_new_value = ""
        for ch in new_value:
            collected_new_value += ch
        sanitize_new_value = (
            collected_new_value.strip()
                .replace(" ", "-")
                .replace("(", "")
                .replace(")", "")
                .replace(".", "-")
                .replace(",", "-")
                .replace("/", "-")
                .replace("\\", "-")
            )
        try:
            try:
                chek_data = datetime.strptime(sanitize_new_value, "%Y-%m-%d")
                if chek_data:
                    self.__value = sanitize_new_value
            except:
                chek_data = datetime.strptime(sanitize_new_value, "%d-%m-%Y")
                if chek_data:
                    standardized_date = chek_data.strftime("%Y-%m-%d")
                    self.__value = standardized_date
        except:
            raise ValueError("Invalid data format")


class Record:
    def __init__(self, name, phone = None, mail = None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.mails = [Mail(mail)] if mail else []
        # self.location = Location(location)

    def add_location(self, location):
        self.location = Location(location)

    def add_phone(self, phone):
        # new_phone = ''.join(filter(str.isdigit, phone))
        self.phones.append(Phone(phone))
        return f"phone {phone} added succefully."


    def add_mail(self, value):
        self.mails.append(Mail(value))

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
        if not found:
            raise ValueError(f"The phone {old_phone} is not found.")
            # return f"The phone {old_phone} is not found."

    
    def edit_mail(self, old_mail, new_mail):
        found = False
        for mail in self.mails:
            if mail.value == old_mail:
                mail.value = new_mail
                found = True
        if not found:
            raise ValueError(f"The mail {old_mail} is not found.")
            # return f"The phone {old_phone} is not found."


    def find_phone(self, phone:str):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None
    

    def remove_phone(self, phone):
        del_phone = None
        for ph in self.phones:
            if ph.value == phone:
                del_phone = ph
        self.phones.remove(del_phone)


    def add_birthday(self, birthday = None):
        self.birthday = Birthday(birthday)


    def days_to_birthday(self):
        today = date.today()
        d_bd = datetime.strptime(self.birthday.value, "%Y-%m-%d")
        if d_bd.month - today.month < 0:
            next_bd = date(2024,d_bd.month, d_bd.day)
            delta_days = next_bd - today
            return delta_days.days
        else:
            if d_bd.day - today.day < 0:
                next_bd = date(2024,d_bd.month, d_bd.day)
                delta_days = next_bd - today
                return delta_days.days
            else:
                next_bd = date(2023,d_bd.month, d_bd.day)
                delta_days = next_bd - today
                if delta_days.days == 0:
                    return "today"
                else:
                    return delta_days.days


    def __str__(self):
        return_res = f"Contact name: {self.name.value}"

        if hasattr(self, 'phones') and self.phones:
            return_res += f", phones: {'; '.join(p.value for p in self.phones)}"

        if hasattr(self, 'birthday') and self.birthday:
            return_res += f", birthday: {self.birthday}"

        if hasattr(self, 'mails') and self.mails:
            return_res += f", mail: {'; '.join(m.value for m in self.mails)}"

        if hasattr(self, 'location') and self.location:
            return_res += f", location: {self.location}"

        return return_res
        

class AddressBook(UserDict):
    def add_record(self,new_contact:Record) -> None:
        self.data[new_contact.name.value] = new_contact
        return f"Contact {new_contact.name.value}, "


    def find(self, name):
        for rec in self.data:
            if rec == name:
                return self.data[rec]
        if not self.data.get(name):
            return None
        

    def search(self, arg):
        return_str = "didn'd find number or characters"
        for rec, phone in self.data.items():
            # print(rec, phone)
            if arg in str(phone):
                if return_str ==  "didn'd find number or characters":
                    return_str = ""
                return_str += str(self.data[rec]) + "\n"
            # else:
            #     return "didn'd find number or characters"
        return return_str
        

    def delete(self, name):
        if not self.data.get(name):
            return f"did't delete contact {name}, not exsist"
        else:
            del self.data[name]
            return f"Contact {name} delete succsefull"
        

    def iterator(self, n=2):
        self.counter = 0
        self.list = []
        #self.data_list = list(self.data.items())
        if len(self.data) >=1:
            for _, val in self.data.items():
                self.list.append(str(val ))
            while self.counter < len(self.list):
                yield self.list[self.counter: self.counter + n]
                self.counter += n
            raise StopIteration("End of list")
        else:
            raise StopIteration("Empty list")
        
     
    def save_address_book(self):
        self.file_name = os.path.join(DIRECTORY, FILE_NAME)
        os.makedirs(DIRECTORY, exist_ok=True)
        with open(self.file_name, "wb") as file:
            pickle.dump(self, file)

    def load_address_book(self):
        self.file_name = os.path.join(DIRECTORY, FILE_NAME)
        os.makedirs(DIRECTORY, exist_ok=True)
        try:
            if os.path.exists(self.file_name):
                with open(self.file_name, "rb") as file:
                    unpacked = pickle.load(file)
                return unpacked
        except:
            return "File not found"