from datetime import datetime, time
import re
from collections import defaultdict
from itertools import combinations

class Lesson:
    def __init__(self, date: datetime.date, class_name: str, teacher_name: str, start_time: time, end_time: time):
        self.date = date
        self.class_name = class_name
        self.teacher_name = teacher_name
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return (f"Класс: {self.__class__.__name__};\n"
                f"Дата: {self.date.strftime('%Y.%m.%d')};\n"
                f"Название аудитории: {self.class_name};\n"
                f"Имя преподавателя: {self.teacher_name};\n"
                f"Время: {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}")

    @classmethod
    def str_to_lesson(cls, s: str):
        date_str = re.search(r'(19|20)\d{2}\.(0[1-9]|1[0-2])\.(0[1-9]|[12][0-9]|3[01])', s).group()
        date_obj = datetime.strptime(date_str, '%Y.%m.%d').date()

        class_match =re.search(r'"([1-5]-(?:0[1-9]|1[0-9]|20))"', s)
        class_str = class_match.group(1) if class_match else None

        teacher_match = re.search(r'"([а-яА-ЯёЁ\s\.]{2,})"', s)
        teacher_str = teacher_match.group(1) if teacher_match else None

        time_match = re.search(r'"(\d{2}:\d{2}-\d{2}:\d{2})"', s)
        if time_match:
            start_time_str, end_time_str = time_match.group(1).split('-')
            start_time_obj = datetime.strptime(start_time_str, '%H:%M').time()
            end_time_obj = datetime.strptime(end_time_str, '%H:%M').time()
        else:
            start_time_obj, end_time_obj = time(0, 0), time(0, 0)

        return cls(date_obj, class_str, teacher_str, start_time_obj, end_time_obj)

def find_conflict(lessons_list):
    lessons_by_key = defaultdict(list)
    for lesson in lessons_list:
        key = (lesson.date, lesson.class_name)
        lessons_by_key[key].append(lesson)
    conflicting_groups = []
    for key, lesson_group in lessons_by_key.items():
        if len(lesson_group) < 2:
            continue
        for lesson1, lesson2 in combinations(lesson_group, 2):
            times_overlap = (lesson1.start_time < lesson2.end_time and
                                lesson1.end_time > lesson2.start_time)
            if times_overlap:
                conflicting_groups.append(lesson_group)
                break

    return conflicting_groups


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

conflicts = find_conflicts(lessons)
if conflicts:
    for i, group in enumerate(conflicts, 1):
        date_str = group[0].date.strftime('%d.%m.%Y')
        class_name = group[0].class_name
        print(f"\nКонфликт №{i}: Аудитория '{class_name}' на {date_str}")

        sorted_group = sorted(group, key=lambda x: x.start_time)
        for lesson in sorted_group:
            print("-" * 20)
            print(str(lesson))
else:
    print("\nПересечений в расписании не найдено.")

print("\n" + "-" * 25)
unique_classrooms = sorted(list({lesson.class_name for lesson in lessons}))
print("Доступные аудитории:", ", ".join(unique_classrooms))

auditory = input("Введите название аудитории для вывода расписания: ")
filtered_lessons = []
for lesson in lessons:
    if lesson.class_name == auditory:
        filtered_lessons.append(lesson)

filtered_lessons.sort(key=lambda x: (x.date, x.start_time))

print(f"\n--- Расписание для аудитории '{auditory}' ---")
if filtered_lessons:
    for lesson in filtered_lessons:
        print(lesson)
        print("-" * 20)
else:
    print("Нет занятий в этой аудитории или аудитория указана неверно.")