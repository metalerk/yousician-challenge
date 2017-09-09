from flask_script import Server, Manager, Command
from app import start_app

manager = Manager(start_app)
manager.add_command("runserver", Server())

if __name__ == "__main__":
    manager.run()
