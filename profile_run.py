import cProfile
from controller import AppController

def main():
    app = AppController()
    app.run()

if __name__ == "__main__":
    cProfile.run("main()", sort="cumulative")