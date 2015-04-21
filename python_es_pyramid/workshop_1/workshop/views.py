from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from .models import *

@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):

    return {
        'users': DBSession.query(User).all(), 
        'project': 'workshop'
    }

@view_config(route_name='ketto', renderer='json')
def ketto(request):

    return {'one': 'ketto', 'project': 'workshop'}

