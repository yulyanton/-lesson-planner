from typing import List, Dict, Any

class ConsoleView:
    def show_message(self, sMsg: str):
        print(f"\n>> {sMsg}")

    def show_error(self, sError: str):
        print(f"\nОШИБКА {sError}")

    def show_menu(self) -> str:
        print("\n" + "="*30)
        print("1. Показать все занятия")
        print("2. Проверить конфликты")
        print("3. Расписание по аудитории")
        print("0. Выход")
        print("="*30)
        return input("Ваш выбор: ").strip()

    def get_classroom_input(self, lstAvailable: List[str]) -> str:
        print(f"Доступные аудитории: {', '.join(lstAvailable)}")
        return input("Введите номер аудитории: ").strip()

    def show_list(self, lstData: List[Any], sHeader: str):
        print(f"\n{sHeader}")
        if not lstData:
            print("Список пуст.")
        else:
            for item in lstData:
                print(str(item))

    def show_conflicts(self, dctConflicts: Dict[str, List[Any]]):
        if not dctConflicts:
            self.show_message("Конфликтов не найдено.")
            return

        print("\nНАЙДЕНЫ КОНФЛИКТЫ")
        for sPlace, lstLessons in dctConflicts.items():
            print(f"\nМесто: {sPlace}")
            for l in lstLessons:
                print(f"  -> {l}")