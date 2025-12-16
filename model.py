import re
from datetime import datetime, time, date
from collections import defaultdict
from itertools import combinations
from typing import List, Dict, Tuple
from exceptions import ParseError, ValidationError

class Lesson:

    DATE_PATTERN = r"(19|20)\d{2}\.(0[1-9]|1[0-2])\.(0[1-9]|[12][0-9]|3[01])"
    CLASS_PATTERN = r'"(\d{1,2}-\d{2})"'
    TEACHER_PATTERN = r'"([а-яА-ЯёЁa-zA-Z\s\.]{2,})"'
    TIME_PATTERN = r'"(\d{2}:\d{2}-\d{2}:\d{2})"'

    def __init__(
            self,
            lesson_date: date,
            classroom: str,
            teacher: str,
            start_time: time,
            end_time: time,
    ):
        self.lesson_date = lesson_date
        self.classroom = classroom
        self.teacher = teacher
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self) -> str:
        return (
            f"Дата: {self.lesson_date.strftime('%Y.%m.%d')} | "
            f"Ауд: {self.classroom} | "
            f"Преп: {self.teacher} | "
            f"Время: {self.start_time.strftime('%H:%M')}-"
            f"{self.end_time.strftime('%H:%M')}"
        )

    @classmethod
    def create_from_string(cls, line: str) -> "Lesson":
        if not line or not line.strip():
            raise ParseError("Пустая строка")

        lesson_date = cls._parse_date(line)
        classroom = cls._parse_classroom(line)
        teacher = cls._parse_teacher(line)
        start_time, end_time = cls._parse_time(line)

        return cls(lesson_date, classroom, teacher, start_time, end_time)

    @staticmethod
    def _parse_date(line: str) -> date:
        match = re.search(Lesson.DATE_PATTERN, line)
        if not match:
            raise ParseError("Некорректная дата")
        return datetime.strptime(match.group(), "%Y.%m.%d").date()

    @staticmethod
    def _parse_classroom(line: str) -> str:
        match = re.search(Lesson.CLASS_PATTERN, line)
        if not match:
            raise ParseError("Некорректная аудитория")

        building, room = map(int, match.group(1).split("-"))
        if not (1 <= building <= 5 and 1 <= room <= 99):
            raise ValidationError("Недопустимый номер аудитории")

        return match.group(1)

    @staticmethod
    def _parse_teacher(line: str) -> str:
        match = re.search(Lesson.TEACHER_PATTERN, line)
        if not match:
            raise ParseError("Не найдено имя преподавателя")
        return match.group(1)

    @staticmethod
    def _parse_time(line: str) -> tuple[time, time]:
        match = re.search(Lesson.TIME_PATTERN, line)
        if not match:
            raise ParseError("Не найдено время")

        start_str, end_str = match.group(1).split("-")
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()

        if start_time >= end_time:
            raise ValidationError("Начало занятия позже окончания")

        return start_time, end_time

class Schedule:

    def __init__(self):
        self._lessons: List[Lesson] = []

    def load_data(self, filename: str) -> str:
        self._lessons.clear()
        success, errors = 0, 0

        try:
            with open(filename, encoding="utf-8") as file:
                for line in file:
                    try:
                        lesson = Lesson.create_from_string(line)
                        self._lessons.append(lesson)
                        success += 1
                    except (ParseError, ValidationError):
                        errors += 1
        except FileNotFoundError:
            return "Файл не найден."

        return f"Загружено: {success}, Ошибок: {errors}"

    def get_all_lessons(self) -> List[Lesson]:
        return sorted(self._lessons, key=lambda l: (l.lesson_date, l.start_time))

    def get_lessons_by_classroom(self, classroom: str) -> List[Lesson]:
        return sorted(
            [l for l in self._lessons if l.classroom == classroom],
            key=lambda l: (l.lesson_date, l.start_time),
        )

    def get_unique_classrooms(self) -> List[str]:
        return sorted({l.classroom for l in self._lessons})

    def find_conflicts(self) -> Dict[str, List[Lesson]]:
        grouped = defaultdict(list)
        for lesson in self._lessons:
            key = (lesson.lesson_date, lesson.classroom)
            grouped[key].append(lesson)

        conflicts = {}
        for (lesson_date, classroom), lessons in grouped.items():
            if len(lessons) < 2:
                continue

            conflict_set = set()
            for first, second in combinations(lessons, 2):
                if (
                        first.start_time < second.end_time
                        and first.end_time > second.start_time
                ):
                    conflict_set.update({first, second})

            if conflict_set:
                key_str = f"{classroom} ({lesson_date.strftime('%d.%m.%Y')})"
                conflicts[key_str] = sorted(
                    conflict_set, key=lambda l: l.start_time
                )

        return conflicts