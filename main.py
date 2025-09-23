from datetime import datetime
import re


class Lesson:
    def __init__(self, date: datetime.date, class_name: str, teacher_name: str):
        self.date = date
        self.class_name = class_name
        self.teacher_name = teacher_name

    def __str__(self):
        return (f"Класс: {self.__class__.__name__};\n"
                f"Дата: {self.date.strftime('%Y.%m.%d')};\n"
                f"Название аудитории: {self.class_name};\n"
                f"Имя преподавателя: {self.teacher_name}")

    @classmethod
    def str_to_lesson(cls, s: str):
        parts = re.findall(r'[^"\s]\S*|"[^"]*"', s)

        date_str = None
        class_str = None
        teacher_str = None
        for part in parts:
            clean_value = part.strip('"')

            if re.match(r'^(19|20)\d{2}\.(0[1-9]|1[0-2])\.(0[1-9]|[12][0-9]|3[01])$', clean_value):
                date_str = clean_value

            elif re.match(r'^[1-5]-(?:[1-9]|1[0-9]|20)$', clean_value):
                class_str = clean_value

            elif re.match(r'^[а-яА-ЯёЁ\s\.]+$', clean_value):
                teacher_str = clean_value

        date_obj = datetime.strptime(date_str, '%Y.%m.%d').date()
        return cls(date_obj, class_str, teacher_str)

filename = "input.txt"
lessons = []

with open(filename, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        lesson = Lesson.str_to_lesson(line)
        lessons.append(lesson)
for i, lesson in enumerate(lessons, 1):
    print(f"\nУрок {i}:")
    print(lesson)