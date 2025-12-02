from controller import AppController
import os

if not os.path.exists("input.txt"):
    with open("input.txt", "w", encoding="utf-8") as f:
        f.write('"1-01" "Иванов" "2023.09.01" "10:00-11:30"\n')
        f.write('"1-01" "Петров" "2023.09.01" "11:00-12:30"\n')
        f.write('"2-05" "Сидоров" "2023.09.01" "09:00-10:00"\n')

if __name__ == "__main__":
    app = AppController()
    app.run()