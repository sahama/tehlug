from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    Table,
    ForeignKey,
    Boolean,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


def striper(str):
    # TODO: do some thing to strip str
    # may be BBCOCE is good
    return str

def is_strip(str):
    if str == is_strip(str):
        return True
    else:
        return False




user_2_group_map = Table('user_2_group_map', Base.metadata,
                       Column('user_id', Integer, ForeignKey('users.id')),
                       Column('group_id', Integer, ForeignKey('groups.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50),nullable=False)
    password = Column(String(50),nullable=False) #md5
    email = Column(String(50),nullable=False)
    display_name = Column(String(50),nullable=True) # comma separated for first and last name
    mobile = Column(String(50),nullable=True)
    block = Column(Boolean) # user is blocked until email activation

    groups = relationship('Group',
                          secondary=user_2_group_map,
                          backref='users'
                          )

    def __init__(self, name, password, email, display_name=None, mobile=None):
        from email.utils import parseaddr
        if is_strip(name) and parseaddr(email)[1] and is_strip(display_name) and str(mobile).isalnum():
            self.name = name
            self.password = password
            self.email = email
            self.display_name = display_name
            self.mobile = mobile
            self.block = True



    def __repr__(self):
        return "<User('{0}','{1}')>".format(self.name, self.display_name)

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return "<Group('{0}')>".format(self.name)


# Index('my_index', MyModel.name, unique=True, mysql_length=255)
