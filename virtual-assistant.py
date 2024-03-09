from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_phone()
        
    def validate_phone(self):
        if len(self.value) != 10 or not self.value.isdigit():
            raise ValueError("Phone number must be a 10-digit string.")
        
class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_birthday()

    def validate_birthday(self):
        try:
            datetime.strptime(self.value, '%d-%m-%Y')
        except ValueError:
            raise ValueError("Incorrect birthday format. Use DD-MM-YYYY.")

    
class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        if birthday:
            self.add_birthday(birthday)

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)
    
    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return
        raise ValueError("No such phone number exists")
    
    def edit_phone(self, old_number, new_number):
        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)
                return
        raise ValueError("No such phone number exists")
    
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return "Match"
        return 'No such phone number exists'
    
    def add_birthday(self, birthday):
        if self.birthday:
            raise ValueError("Birthday already exists for this contact.")
        self.birthday = Birthday(birthday)
        
    def __str__(self):
        return f'{self.name}: {", ".join(str(phone) for phone in self.phones)} and was born {self.birthday}'

class AddressBook(UserDict):
    def add_record(self, args):
        if (len(args) == 3):            
            name, phone, birthday = args
            if name in self.data:
                self.data[name].add_phone(phone)
                return f"Phone added to contact {name}."
            else:
                contact = Record(name)
                contact.add_phone(phone)
                contact.add_birthday(birthday) 
                self.data[name] = contact
                return "Contact added."
        else:
            name, phone = args
            if name in self.data:
                self.data[name].add_phone(phone)
                return f"Phone added to contact {name}."
            else:
                contact = Record(name)
                contact.add_phone(phone)
                self.data[name] = contact
                return "Contact added."
        
    def change_contact(self, args):
        name, phone, new_phone = args
        if name in self.data:
            if phone in self.data[name].phones:
                self.data[name].phones[phone] = Phone(new_phone)
            return "Phone number updated."
        else:
            return "Contact does not exist."
    
    def find(self, args):
        if args.name in self.data:
            return str(self.data[args.name].phones)
        else:
            return "Contact does not exist."
        
    def show_all(self):
        print(self)
        
    def add_birthday(self, args):  
        name, birthday = args      
        if name in self.data:
            self.data[name].add_birthday(birthday)
            return "Birthday added."
        else:
            return "Contact does not exist."
        
    def show_birthday(self, args):
        if args[0] in self.records and self.records[args[0]].birthday:
            return str(self.records[args[0]].birthday)
        else:
            return "Contact does not exist or birthday not set."
        
    def get_birthdays_per_week(self):
        today = datetime.now()
        next_week = [today + timedelta(days=i) for i in range(1, 8)]
        birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, '%d-%m-%Y')
                for date in next_week:
                    if birthday_date.month == date.month and birthday_date.day == date.day:
                        birthdays.append(f'{date}:{record.name}')
        return ' | '.join(birthdays)
    
    def __str__(self):
        result = ""
        for contact in self.data.values():
            result += str(contact) + "\n"
        return result
    
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "No such record exists"
        except IndexError:
            return "Give me name and phone please."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    address_book = AddressBook()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(address_book.add_record(args))
        elif command == "change":
            print(address_book.change_contact(args))
        elif command == "phone":
            print(address_book.find(args))
        elif command == "all":
            print(address_book.show_all())
        elif command == "add-birthday":
            print(address_book.add_birthday(args))
        elif command == "show-birthday":
            print(address_book.show_birthday(args))
        elif command == "birthdays":
            print(address_book.get_birthdays_per_week())
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()