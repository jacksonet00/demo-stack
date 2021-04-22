# Generate some dummy data in the db

from .engine import db_session, engine
from .model import User, Animal, Zoo
from passlib.hash import pbkdf2_sha256
from sqlalchemy import text


def drop_table(tablename):
    engine.execute(text(f'DROP TABLE IF EXISTS {tablename};'))


def drop_tables(tablenames=[]):
    for tablename in tablenames:
        engine.execute(text(f'DROP TABLE IF EXISTS {tablename};'))


def gen_data():
    db_session.add(
        User(username='jackson', password=pbkdf2_sha256.hash('password')))
    db_session.add(
        User(username='john', password=pbkdf2_sha256.hash('password')))
    db_session.add(
        User(username='jimothy', password=pbkdf2_sha256.hash('password')))
    db_session.commit()

    john = db_session.query(User).filter(User.username == 'john').first()
    jackson = db_session.query(User).filter(User.username == 'jackson').first()

    db_session.add(Zoo(name='manhattan zoo', owner_id=john.id))
    db_session.add(Zoo(name='san diego zoo', owner_id=john.id))
    db_session.add(Zoo(name='gulf breeze zoo', owner_id=jackson.id))
    db_session.commit()

    manhattan = db_session.query(Zoo).filter(
        Zoo.name == 'manhattan zoo').first()
    san_deigo = db_session.query(Zoo).filter(
        Zoo.name == 'san diego zoo').first()

    db_session.add(Animal(name='flying squirrel',
                   owner_id=john.id, zoo_id=manhattan.id))
    db_session.add(Animal(name='alex the lion',
                   owner_id=jackson.id, zoo_id=san_deigo.id))
    db_session.add(Animal(name='el tigre',
                   owner_id=jackson.id))
    db_session.commit()
