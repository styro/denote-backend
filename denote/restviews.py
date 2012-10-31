from cornice.resource import resource, view

from denote import models
from denote.models import DBSession

@resource(collection_path='/users', path='/users/{id}')
class User(object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):
        users = DBSession.query(models.User).all()
        user_ids = [u.id for u in users]
        return {'users': user_ids}

    @view(renderer='json')
    def get(self):
        user_id = int(self.request.matchdict['id'])
        user = DBSession.query(models.User).get(user_id)
        return dict(user)
