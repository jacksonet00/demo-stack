import os
from flask_script import Server, Manager
from app import create_app

port = int(os.environ.get('PORT', 5000))

app = create_app()

manager = Manager(app)
manager.add_command("runserver", Server(host='0.0.0.0', port=port))

if __name__ == "__main__":
    manager.run()
