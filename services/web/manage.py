from flask.cli import FlaskGroup

from project import app, db #, User
from project.models import User, City
import click

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
@click.argument("mail")
def seed_db(mail):
    db.session.add(User(email=mail))
    db.session.commit()


if __name__ == "__main__":
    cli()