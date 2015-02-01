__author__ = 'hamid'
from .models import (
    DBSession,
    Group,
    User,
)

from pyramid.security import (
    Allow,
    Everyone,
)


def groupfinder(userid, request):

    user = DBSession.query(User).filter_by(name=userid).one()
    return [group.title for group in user.groups]


# TODO: try to add Group object to RootFactory
# print(DBSession.query(Group).filter_by(id=4).one())

class RootFactory(object):
    __acl__ = [(Allow, Everyone, 'view')]

    def __init__(self, request):
        pass
