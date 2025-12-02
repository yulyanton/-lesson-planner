import re
from datetime import datetime, time, date
from collections import defaultdict
from itertools import combinations
from typing import List, Dict, Tuple
from exceptions import ParseError, ValidationError

class Lesson:
    def __init__(self, dDate: date, sClassName: str, sTeacherName: str, tStartTime: time, tEndTime: time):
        self.dDate = dDate
        self.sClassName = sClassName
        self.sTeacherName = sTeacherName
        self.tStartTime = tStartTime
        self.tEndTime = tEndTime

    def __str__(self):
        return (f"Дата: {self.dDate.strftime('%Y.%m.%d')} | "
                f"Ауд: {self.sClassName} | "
                f"Преп: {self.sTeacherName} | "
                f"Время: {self.tStartTime.strftime('%H:%M')}-{self.tEndTime.strftime('%H:%M')}")

    @classmethod
    def create_from_string(cls, sLine: str):
        if not sLine or not sLine.strip():
            raise ParseError("Пустая строка")

        oDateMatch = re.search(r'(19|20)\d{2}\.(0[1-9]|1[0-2])\.(0[1-9]|[12][0-9]|3[01])', sLine)
        if not oDateMatch:
            raise ParseError("Некорректная дата")
        dDateObj = datetime.strptime(oDateMatch.group(), '%Y.%m.%d').date()

        oClassMatch = re.search(r'"(\d{1,2}-\d{2})"', sLine)
        if not oClassMatch:
            raise ParseError("Некорректная аудитория")
        sClassStr = oClassMatch.group(1)
        sBuild, sRoom = sClassStr.split('-')
        if not (1 <= int(sBuild) <= 5) or not (1 <= int(sRoom) <= 99):
            raise ValidationError(f"Недопустимый номер аудитории: {sClassStr}")

        oTeacherMatch = re.search(r'"([а-яА-ЯёЁa-zA-Z\s\.]{2,})"', sLine)
        if not oTeacherMatch:
            raise ParseError("Не найдено имя преподавателя")
        sTeacherStr = oTeacherMatch.group(1)

        oTimeMatch = re.search(r'"(\d{2}:\d{2}-\d{2}:\d{2})"', sLine)
        if not oTimeMatch:
            raise ParseError("Не найдено время")
        sStart, sEnd = oTimeMatch.group(1).split('-')
        tStartObj = datetime.strptime(sStart, '%H:%M').time()
        tEndObj = datetime.strptime(sEnd, '%H:%M').time()

        if tStartObj >= tEndObj:
            raise ValidationError("Начало урока должно быть раньше конца")

        return cls(dDateObj, sClassStr, sTeacherStr, tStartObj, tEndObj)

class Schedule:
    def __init__(self):
        self._lstLessons: List[Lesson] = []

    def load_data(self, sFilename: str) -> str:
        self._lstLessons = []
        iSuccess = 0
        iErrors = 0

        try:
            with open(sFilename, 'r', encoding='utf-8') as f:
                for sLine in f:
                    sLine = sLine.strip()
                    if not sLine: continue
                    try:
                        oLesson = Lesson.create_from_string(sLine)
                        self._lstLessons.append(oLesson)
                        iSuccess += 1
                    except Exception:
                        iErrors += 1
            return f"Загружено: {iSuccess}, Ошибок: {iErrors}"
        except FileNotFoundError:
            return "Файл не найден."

    def get_all_lessons(self) -> List[Lesson]:
        return sorted(self._lstLessons, key=lambda x: (x.dDate, x.tStartTime))

    def get_lessons_by_classroom(self, sClassroom: str) -> List[Lesson]:
        lstResult = [l for l in self._lstLessons if l.sClassName == sClassroom]
        return sorted(lstResult, key=lambda x: (x.dDate, x.tStartTime))

    def get_unique_classrooms(self) -> List[str]:
        return sorted(list({l.sClassName for l in self._lstLessons}))

    def find_conflicts(self) -> Dict[str, List[Lesson]]:
        dctByKey = defaultdict(list)
        for oLesson in self._lstLessons:
            key = (oLesson.dDate, oLesson.sClassName)
            dctByKey[key].append(oLesson)

        dctConflicts = {}

        for key, lstGroup in dctByKey.items():
            if len(lstGroup) < 2: continue

            setConflicts = set()
            for l1, l2 in combinations(lstGroup, 2):
                if l1.tStartTime < l2.tEndTime and l1.tEndTime > l2.tStartTime:
                    setConflicts.add(l1)
                    setConflicts.add(l2)

            if setConflicts:
                sKeyStr = f"{key[1]} ({key[0].strftime('%d.%m.%Y')})"
                dctConflicts[sKeyStr] = sorted(list(setConflicts), key=lambda x: x.tStartTime)

        return dctConflicts