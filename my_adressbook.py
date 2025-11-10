from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self._validate_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)
    
    def _validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 10


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)
        return f"Phone {phone} added to contact {self.name.value}"

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return f"Phone {phone} removed from contact {self.name.value}"
        raise ValueError(f"Phone {phone} not found in contact {self.name.value}")

    def edit_phone(self, old_phone, new_phone):
        # Валідуємо новий телефон
        Phone(new_phone)
        
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                message = f"Phone {old_phone} changed to {new_phone}"
                return f"{message} for contact {self.name.value}"
        raise ValueError(f"Phone {old_phone} not found in contact {self.name.value}")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value in self.data:
            raise ValueError(f"Contact {record.name.value} already exists")
        self.data[record.name.value] = record
        return f"Contact {record.name.value} added successfully"

    def find(self, name):
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} deleted successfully"
        raise ValueError(f"Contact {name} not found")


# Використовуємо згідно з технічним завданням
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    if john:
        john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    if found_phone:
        print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    # book.delete("Jane")

    # Перевірка всіх контактів після видалення
    for name, record in book.data.items():
        print(record)