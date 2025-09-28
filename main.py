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
        date_str = re.search(r'(19|20)\d{2}\.(0[1-9]|1[0-2])\.(0[1-9]|[12][0-9]|3[01])', s).group()

        class_match =re.search(r'"([1-5]-(?:0[1-9]|1[0-9]|20))"', s)
        class_str = class_match.group(1) if class_match else None
        print(class_str)

        teacher_match = re.search(r'"([а-яА-ЯёЁ\s\.]{2,})"', s)
        teacher_str = teacher_match.group(1) if teacher_match else None
        print(teacher_str)



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

sorted_lessons = sorted(lessons, key=lambda x: x.date)

print("\n\nОтсортированный список уроков по дате\n")
for i, lesson in enumerate(sorted_lessons, 1):
    print(lesson, "\n")

print("Введите название аудитории: ")
auditory = input()
filtered_lessons = []
for lesson in lessons:
    if lesson.class_name == auditory:
        filtered_lessons.append(lesson)

print(f"\nУроки в аудитории {auditory}\n")
if filtered_lessons:
    for i, lesson in enumerate(filtered_lessons, 1):
        print(lesson, "\n")
else:
    print("Нет уроков в этой аудитории.")



