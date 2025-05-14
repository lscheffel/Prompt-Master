from app import app, db
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)

if __name__ == '__main__':
    from flask.cli import FlaskGroup
    cli = FlaskGroup(app)
    cli()