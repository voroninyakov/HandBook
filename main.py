class Note:
    def __init__(self, last_name: str, first_name: str, patronymic: str, organization: str, work_phone: str,
                 personal_phone: str, is_new: bool = False, note_id: str = ""):
        self.last_name: str = last_name
        self.first_name: str = first_name
        self.patronymic: str = patronymic
        self.organization: str = organization
        self.work_phone: str = work_phone
        self.personal_phone: str = personal_phone
        self.id: str = note_id
        if is_new:
            self.update_text_data()

    def __str__(self):
        return '|'.join([self.id, self.last_name, self.first_name, self.patronymic, self.organization, self.work_phone,
                         self.personal_phone, '\n'])

    def update_from_string(self, string: str):
        """
        Обновление записи как python объекта
        """
        self.last_name: str = string.split('|')[0] if string.split('|')[0] else self.last_name
        self.first_name: str = string.split('|')[1] if string.split('|')[1] else self.first_name
        self.patronymic: str = string.split('|')[2] if string.split('|')[2] else self.patronymic
        self.organization: str = string.split('|')[3] if string.split('|')[3] else self.organization
        self.work_phone: str = string.split('|')[4] if string.split('|')[4] else self.work_phone
        self.personal_phone: str = string.split('|')[5] if string.split('|')[5] else self.personal_phone
        self.update_text_data()

    def update_text_data(self):
        """
        Обновление текстовых данных: создание новой или редактирование текстовой записи
        """
        try:
            with open('notes.txt', 'r+', encoding='utf-8') as f:
                lines = [line for line in f.readlines()]
            with open('notes.txt', 'w+', encoding='utf-8') as f:
                if not self.id:
                    self.id = str(len(lines) + 1)
                    lines.append(str(self))
                    f.writelines(lines)
                else:
                    for line in range(len(lines)+1):
                        if lines[line].split("|")[0] == self.id:
                            lines[line] = str(self)
                            f.writelines(lines)
                            break
        except FileNotFoundError:
            file = open('notes.txt', 'w+', encoding='utf-8')
            file.close()


def search_note(fields: list[str]):
    """
    Поиск записи в текстовом файле по полям
    """
    try:
        with open('notes.txt', 'r+', encoding='utf-8') as f:
            lines = [line for line in f.readlines()]
    except FileNotFoundError:
        file = open('notes.txt', 'w+', encoding='utf-8')
        file.close()
    searched = 0
    for line in lines:
        for i in range(5):
            if fields[i] and (fields[i] in line.split("|")[i] or fields[i] == line.split("|")[i]):
                print(line, end="")
                searched += 1
                break
    if searched > 0:
        print("Найдено:", searched)
    else:
        print("Ничего не найдено")


def run():
    """
    Запуск интерфейса через консоль
    """
    fields = ['фамилия', 'имя', 'отчество', 'название организации', 'телефон рабочий', 'телефон личный (сотовый)']
    try:
        file = open('notes.txt', 'r+', encoding='utf-8')
    except FileNotFoundError:
        file = open('notes.txt', 'w+', encoding='utf-8')
    file.close()
    with open('notes.txt', 'r+', encoding='utf-8') as f:
        notes = [Note(line.split("|")[1],
                      line.split("|")[2],
                      line.split("|")[3],
                      line.split("|")[4],
                      line.split("|")[5],
                      line.split("|")[6], id=line.split("|")[0]) for line in f.readlines()]
    print("Справочник 1.0.0\nДля просмотра списка команд введите 'помощь'")
    while True:
        command = input(">>>")
        if command == 'помощь':
            print("Список команд:\n 'новая запись' создаёт новую запись \n 'все записи' выводит все записи \n \
'поиск' поиск по полям записей \n 'редактировать {номер}' редактирование записи по номеру (например 'редактировать 1')")
        elif command == 'новая запись':
            note_fields = []
            for field in fields:
                note_fields.append(input(field + ': '))
            notes.append(
                Note(note_fields[0], note_fields[1], note_fields[2], note_fields[3], note_fields[4], note_fields[5],
                     is_new=True))
        elif command == 'все записи':
            try:
                with open('notes.txt', 'r', encoding='utf-8') as f:
                    for note in f.readlines():
                        print(note, end='')
                        break
                    else:
                        print('Записей нет')
            except FileNotFoundError:
                print("Файл не найден, создаётся...")
                file = open('notes.txt', 'w+', encoding='utf-8')
                file.close()
                print("Файл создан, записей нет")
        elif command[0:5] == 'поиск':
            print('Напишите для каждой характеристики данные для поиска, если для какого-то поля их нет то пропускайте \
его')
            search_note([input(field + ': ') for field in fields])
        elif command.split(' ')[0] == 'редактировать':
            print("Поиск записи...")
            try:
                for note in notes:
                    if note.id == command.split(" ")[1]:
                        print("Запись найдена")
                        note_fields = [input(field + ': ') for field in fields]
                        note.update_from_string('|'.join(note_fields))
                        print(note)
                        break
                else:
                    print("Запись не найдена")
            except IndexError:
                print('Введите номер id')


if __name__ == '__main__':
    run()
