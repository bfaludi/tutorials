import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Article(Base):
    __tablename__ = 't_article'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('t_user.id', ondelete = 'CASCADE'))
    content = Column(UnicodeText)
    created = Column(DateTime)
    updated = Column(DateTime)
    
    def __init__( self, user, content ):
        self.user_id = user.id
        self.content = content
        self.created = datetime.datetime.now()
        self.updated = datetime.datetime.now()

class User(Base):
    __tablename__ = 't_user'

    id = Column(Integer, primary_key = True )
    username = Column(Unicode(255), index = True)
    password = Column(Unicode(255))
    name = Column(Unicode(255))
    age = Column(Integer)
    created = Column(DateTime)
    updated = Column(DateTime)
