import os
from flask_script import Server, Manager
from app import create_app

app = create_app()
manager = Manager(app)
manager.add_command("runserver", Server(host=os.environ['DB_HOST']))

if __name__ == "__main__":
    manager.run()
