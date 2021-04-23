import os
from flask_script import Server, Manager
from app import create_app

app = create_app()

manager = Manager(app)
manager.add_command("runserver", Server(
    host='0.0.0.0', port=os.environ.get('PORT')))

if __name__ == "__main__":
    manager.run()
