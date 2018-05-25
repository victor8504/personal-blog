from app import create_app
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand

# Creating app instance
app = create_app('development')

manager = Manager(app)
manager.add_command('server',Server)

migrate = Migrate(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run