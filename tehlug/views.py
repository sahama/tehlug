# Sayyid Hamid Mahdavi
# GPL v3 ; later may be change

from pyramid.response import Response
from pyramid.view import (
    view_config,
    forbidden_view_config,
)

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPForbidden,
    HTTPNotFound,
)

from pyramid.security import (
remember,
forget,
)

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    User,
    )


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(User).filter(User.name == 'root').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'tehlug'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_tehlug_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

@view_config(route_name='signin', renderer='templates/signin.pt')
def signin(request):
    login_url = request.route_url('signin')
    referrer = request.url
    if referrer == login_url:
        referrer = request.route_url('home')

    message = ''
    try:
        import hashlib
        user = DBSession.query(User).filter_by(name=request.authenticated_userid).one()
    except:
        user = None

    if 'submit' in request.POST:
        name = request.POST.get('login_name', '')
        password = request.POST.get('password', '')

        try:
            import hashlib
            user = DBSession.query(User).filter_by(name=name,password=hashlib.md5(password.encode()).hexdigest()).one()
            headers = remember(request, user.name)
            message = 'user logged in:{0}'.format(name)
            return HTTPFound(location=referrer, headers=headers)
        # try:
        #     user = DBSession.query(User).filter_by(login_name=login_name,password=password).one()
        #     print(user)
        #     headers = remember(request, login_name)
        #     message = 'user logged in:{0}'.format(user.first_name)
        #     return HTTPFound(location=referrer, headers=headers)
        except:
            message = 'کاربر پیدا نشد'

    return {'user':user, 'message':message}


@view_config(route_name='signout', renderer='templates/signout.pt')
def signout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)

@view_config(route_name='signup', renderer='templates/signup.pt')
def signup(request):
    message = ''
    if 'submit' in request.POST:
        same_users=DBSession.query(User).filter_by(name=request.POST.get('login_name', '')).all()
        if not same_users:
            import hashlib
            user = User(name=request.POST.get('login_name', ''),
                        password=hashlib.md5(request.POST.get('password', '').encode()).hexdigest(),
                        email=request.POST.get('email', ''),
                        display_name=request.POST.get('display_name', ''),
                        mobile = request.POST.get('mobile', ''),)

            DBSession.add(user)
            message ='کاربر ثبت شد'
        else:
            message ='امکان ثبت کاربر وجود ندارد'

    return {'message':message}



