import datetime

from sqlalchemy import (
    Table,
    Column,
    DateTime,
    Integer,
    Unicode,
    UnicodeText,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

note_label_table = Table('notes_labels', Base.metadata,
    Column('note_id', Integer, ForeignKey('notes.id')),
    Column('label_id', Integer, ForeignKey('labels.id'))
)

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    content = Column(UnicodeText)
    created_on = Column(DateTime)
    creator_id = Column(Integer, ForeignKey('users.id'))
    labels = relationship("Label", secondary=note_label_table, backref="notes")

    def __init__(self, title, content=None, creator=None):
        self.title = title
        self.created_on = datetime.datetime.utcnow()
        if content:
            self.content = content
        if creator:
            self.created_by = creator

class Label(Base):
    __tablename__ = 'labels'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True)

    def __init__(self, name):
        self.name = name

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, unique=True)
    notes = relationship("Note", backref="created_by")
    identities = relationship("Identity", backref="user")

    def __init__(self, name):
        self.name = name

    def __iter__(self):
        yield ('id', self.id)
        yield ('name', self.name)
        yield ('notes', [n.id for n in self.notes])
        yield ('identities', [i.id for i in self.identities])

class Identity(Base):
    __tablename__ = 'identities'
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))