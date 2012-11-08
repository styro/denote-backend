import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest

from cornice.resource import resource, view

from denote import models
from denote.models import DBSession

log = logging.getLogger(__name__)

@resource(collection_path='/users', path='/users/{id}')
class User(object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):
        users = DBSession.query(models.User).all()
        user_list = [{'id': u.id, 'name': u.name} for u in users]
        return {'users': user_list}

    def get(self):
        user_id = int(self.request.matchdict['id'])
        user = DBSession.query(models.User).get(user_id)
        if user:
            return dict(user)
        else:
            raise HTTPNotFound

    def collection_post(self):
        # Note: needs sending with 'Content-Type: application/json'
        body = self.request.json_body
        user = models.User(body['name'])
        DBSession.add(user)

    def put(self):
        # Note: needs sending with 'Content-Type: application/json'
        user_id = int(self.request.matchdict['id'])
        user = DBSession.query(models.User).get(user_id)
        if not user:
            raise HTTPNotFound
        body = self.request.json_body
        if 'name' in body:
            user.name = body['name']
        if 'notes' in body:
            user.notes = []
            for note_dict in body['notes']:
                note = DBSession.query(models.Note).get(note_dict['id'])
                if not note:
                    raise HTTPBadRequest('Request body contains an invalid note id')
                user.notes.append(note)
        if 'identities' in body:
            user.identities = []
            for ident_id in body['identities']:
                identity = DBSession.query(models.Identity).get(ident_id)
                if not identity:
                    raise HTTPBadRequest('Request body contains an invalid identity id')
                user.identities.append(identity)


    def delete(self):
        user_id = int(self.request.matchdict['id'])
        DBSession.query(models.User).filter(models.User.id==user_id).delete()