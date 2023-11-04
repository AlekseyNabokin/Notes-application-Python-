import json
from datetime import datetime


class Note:
    def __init__(self, id, title, body, created_at, updated_at):
        self.id = id
        self.title = title
        self.body = body
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, note_dict):
        return cls(
            note_dict["id"],
            note_dict["title"],
            note_dict["body"],
            note_dict["created_at"],
            note_dict["updated_at"]
        )

    def todict(self):
        pass


def create_note():
    id = input("Введите идентификатор заметки: ")
    title = input("Введите заголовок заметки: ")
    body = input("Введите текст заметки: ")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note = Note(id, title, body, created_at, updated_at)
    return note


def save_note(note, filename):
    with open(filename, "a") as file:
        json.dump(note.to_dict(), file)
        file.write("\n")


def read_notes(filename):
    notes = []
    with open(filename, "r") as file:
        for line in file:
            note_dict = json.loads(line)
            note = Note.from_dict(note_dict)
            notes.append(note)
    return notes


def edit_note(note):
    print("Редактирование заметки:")
    print("1. Заголовок")
    print("2. Текст")
    option = int(input("Выберите опцию: "))
    if option == 1:
        title = input("Введите новый заголовок заметки: ")
        note.title = title
    elif option == 2:
        body = input("Введите новый текст заметки: ")
        note.body = body
    note.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def delete_note(note, filename):
    notes = read_notes(filename)
    with open(filename, "w") as file:
        for n in notes:
            if n.id != note.id:
                file.write(json.dumps(n.to_dict()) + "\n")


def filter_notes_by_date(notes, date):
    filtered_notes = []
    for note in notes:
        if note.created_at.split()[0] == date:
            filtered_notes.append(note)
    return filtered_notes


def main():
    filename = "notes.json"
    while True:
        print("=== Меню ===")
        print("1. Создать заметку")
        print("2. Просмотреть список заметок")
        print("3. Редактировать заметку")
        print("4. Удалить заметку")
        print("5. Выход")
        option = int(input("Выберите опцию: "))
        if option == 1:
            note = create_note()
            save_note(note, filename)
            print("Заметка успешно создана.")
        elif option == 2:
            date_filter = input("Введите дату для фильтрации (гггг-мм-дд): ")
            notes = read_notes(filename)
            filtered_notes = filter_notes_by_date(notes, date_filter)
            for note in filtered_notes:
                print(f"ID: {note.id}")
                print(f"Заголовок: {note.title}")
                print(f"Текст: {note.body}")
                print(f"Создана: {note.created_at}")
                print(f"Обновлена: {note.updated_at}")
                print("---")
        elif option == 3:
            id = input("Введите ID заметки для редактирования: ")
            notes = read_notes(filename)
            for note in notes:
                if note.id == id:
                    edit_note(note)
            with open(filename, "w") as file:
                for note in notes:
                    file.write(json.dumps(note.todict()) + "\n")
            print("Заметка успешно отредактирована.")
        elif option == 4:
            id = input("Введите ID заметки для удаления: ")
            notes = read_notes(filename)
            for note in notes:
                if note.id == id:
                    delete_note(note, filename)
            print("Заметка успешно удалена.")
        elif option == 5:
            break


if __name__ == "__main__":
    main()
