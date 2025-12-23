import pytest
from datetime import date, time
from model import Schedule, Lesson
from exceptions import ValidationError


class TestFatModel:

    def test_create_lesson(self):
        sLine = '"1-01" "Иванов" "2023.09.01" "10:00-11:00"'
        oLesson = Lesson.create_from_string(sLine)
        assert oLesson.classroom == "1-01"
        assert oLesson.start_time == time(10, 0)

    def test_validation_error(self):
        sLine = '"1-01" "Test" "2023.09.01" "12:00-10:00"'
        with pytest.raises(ValidationError):
            Lesson.create_from_string(sLine)

    def test_conflict_logic(self):
        oSchedule = Schedule()
        l1 = Lesson(date(2023, 9, 1), "1-01", "T1", time(10, 0), time(11, 30))
        l2 = Lesson(date(2023, 9, 1), "1-01", "T2", time(11, 0), time(12, 30))  # Пересечение
        oSchedule._lessons = [l1, l2]

        dctConflicts = oSchedule.find_conflicts()
        assert len(dctConflicts) == 1
        assert "1-01" in list(dctConflicts.keys())[0]
        assert len(list(dctConflicts.values())[0]) == 2

    def test_filter_logic(self):
        oSchedule = Schedule()
        l1 = Lesson(date(2023, 9, 1), "1-01", "T1", time(10, 0), time(11, 0))
        l2 = Lesson(date(2023, 9, 1), "2-05", "T2", time(10, 0), time(11, 0))
        oSchedule._lessons = [l1, l2]

        lstRes = oSchedule.get_lessons_by_classroom("1-01")
        assert len(lstRes) == 1
        assert lstRes[0].teacher == "T1"