from model import Schedule
from view import ConsoleView

class AppController:
    def __init__(self):
        self.oModel = Schedule()
        self.oView = ConsoleView()
        self.sFilename = "input.txt"

    def run(self):
        sStatus = self.oModel.load_data(self.sFilename)
        self.oView.show_message(f"Старт программы. {sStatus}")

        while True:
            sChoice = self.oView.show_menu()

            if sChoice == '1':
                self._handle_show_all()
            elif sChoice == '2':
                self._handle_conflicts()
            elif sChoice == '3':
                self._handle_filter()
            elif sChoice == '0':
                self.oView.show_message("Выход.")
                break
            else:
                self.oView.show_error("Неверная команда.")

    def _handle_show_all(self):
        lstLessons = self.oModel.get_all_lessons()
        self.oView.show_list(lstLessons, "Все занятия")

    def _handle_conflicts(self):
        dctConfl = self.oModel.find_conflicts()
        self.oView.show_conflicts(dctConfl)

    def _handle_filter(self):
        lstRooms = self.oModel.get_unique_classrooms()
        sTarget = self.oView.get_classroom_input(lstRooms)
        lstFiltered = self.oModel.get_lessons_by_classroom(sTarget)
        self.oView.show_list(lstFiltered, f"Расписание: {sTarget}")