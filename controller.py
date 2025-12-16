from model import Schedule
from view import ConsoleView

class AppController:
    def __init__(self):
        self.model = Schedule()
        self.view = ConsoleView()
        self.filename = "input.txt"

    def run(self):
        status = self.model.load_data(self.filename)
        self.view.show_message(f"Старт программы. {status}")

        while True:
            choice = self.view.show_menu()

            if choice == "1":
                self.view.show_list(
                    self.model.get_all_lessons(), "Все занятия"
                )
            elif choice == "2":
                self.view.show_conflicts(self.model.find_conflicts())
            elif choice == "3":
                rooms = self.model.get_unique_classrooms()
                target = self.view.get_classroom_input(rooms)
                lessons = self.model.get_lessons_by_classroom(target)
                self.view.show_list(lessons, f"Расписание: {target}")
            elif choice == "0":
                self.view.show_message("Выход.")
                break
            else:
                self.view.show_error("Неверная команда.")

    def _handle_show_all(self):
        lstLessons = self.model.get_all_lessons()
        self.view.show_list(lstLessons, "Все занятия")

    def _handle_conflicts(self):
        dctConfl = self.model.find_conflicts()
        self.view.show_conflicts(dctConfl)

    def _handle_filter(self):
        lstRooms = self.model.get_unique_classrooms()
        sTarget = self.view.get_classroom_input(lstRooms)
        lstFiltered = self.model.get_lessons_by_classroom(sTarget)
        self.view.show_list(lstFiltered, f"Расписание: {sTarget}")