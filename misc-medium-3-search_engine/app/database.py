from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy import String, Integer, Column
from sqlalchemy.engine import create_engine
from contextlib import contextmanager

DB_URL = 'postgresql://mctf2020:mctf2020@misc-6-medium-db/mctf2020'
engine = create_engine(DB_URL, pool_size=10, max_overflow=2,pool_recycle=300,pool_pre_ping=True,pool_use_lifo=True)

Base = declarative_base()

def init_db():
    global Session
    Session = sessionmaker(bind=engine)


class Auth(Base):
    __tablename__ = 'mctf2020'
    id = Column(Integer, primary_key=True)
    level = Column('level', Integer, default=1, nullable=False)
    imgnums = Column('imgnums', String(32), nullable=False, default='0,')
    username = Column('username', String(32), unique=True, nullable=False)
    password = Column('password', String(32), nullable=False)
    timestap = Column('timestap', String(10))

    def __init__(self, username, password, timestap, level):
        self.username = username
        self.password = password
        self.timestap = timestap
        self.level = level

    def __repr__(self):
        return "<<Auth(id='{}', username='{}', password='{}')>>" \
            .format(self.id, self.username, self.password)


if not database_exists(DB_URL):
    create_database(DB_URL)
else:
    Base.metadata.create_all(engine)

@contextmanager
def session_scope():
    session: Session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
