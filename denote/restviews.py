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
        # We flush the session to generate an id that we can add to the response
        DBSession.flush()
        return dict(user)

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
            note_ids = [n['id'] for n in body['notes']]
            note_query = DBSession.query(models.Note).filter(models.Note.id.in_(note_ids))
            user.notes = note_query.all()
        if 'identities' in body:
            id_query = DBSession.query(models.Identity)
            id_query.filter(models.Identity.id.in_(body['identities']))
            user.identities = id_query.all()

    def delete(self):
        user_id = int(self.request.matchdict['id'])
        DBSession.query(models.User).filter(models.User.id==user_id).delete()

@resource(collection_path='/notes', path='/notes/{id}')
class Note(object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):
        notes = DBSession.query(models.Note).all()
        note_list = [{'id': n.id, 'title': n.title} for n in notes]
        return {'notes': note_list}

    def get(self):
        note_id = int(self.request.matchdict['id'])
        note = DBSession.query(models.Note).get(note_id)
        if note:
            return dict(note)
        else:
            raise HTTPNotFound

    def collection_post(self):
        # Note: needs sending with 'Content-Type: application/json'
        body = self.request.json_body
        note = models.Note(body['title'])
        if 'content' in body:
            note.content = body['content']
        if 'creator_id' in body:
            # The id takes preference
            note.creator_id = body['creator_id']
        elif 'created_by' in body:
            name = body['created_by']
            user = DBSession.query(models.User).filter_by(name=name).first()
            if user:
                note.creator_id = user.id
        if 'labels' in body and len(body['labels']) > 0:
            lids = [x['id'] for x in body['labels']]
            label_query = DBSession.query(models.Label).filter(models.Label.id.in_(lids))
            note.labels = label_query.all()
        DBSession.add(note)
        # We flush the session to generate an id that we can add to the response
        DBSession.flush()
        return dict(note)

    def put(self):
        # Note: needs sending with 'Content-Type: application/json'
        note_id = int(self.request.matchdict['id'])
        note = DBSession.query(models.Note).get(note_id)
        if not note:
            raise HTTPNotFound
        body = self.request.json_body
        if 'title' in body:
            note.title = body['title']
        if 'content' in body:
            note.content = body['content']
        # We ignore created_on, created_by, creator_id as they are 'immutable'
        if 'labels' in body:
            lids = [l['id'] for l in body['labels']]
            label_query = DBSession.query(models.Label).filter(models.Label.id.in_(lids))
            note.labels = label_query.all()

    def delete(self):
        note_id = int(self.request.matchdict['id'])
        DBSession.query(models.Note).filter(models.Note.id==note_id).delete()

@resource(collection_path='/labels', path='/labels/{id}')
class Label(object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):
        labels = DBSession.query(models.Label).all()
        label_list = [{'id': l.id, 'name': l.name, 'note_count': len(l.notes)} for l in labels]
        return {'labels': label_list}

    def get(self):
        label_id = int(self.request.matchdict['id'])
        label = DBSession.query(models.Label).get(label_id)
        if label:
            return dict(label)
        else:
            raise HTTPNotFound

    def collection_post(self):
        # Note: needs sending with 'Content-Type: application/json'
        body = self.request.json_body
        label = models.Label(body['name'])
        DBSession.add(label)
        # We flush the session to generate an id that we can add to the response
        DBSession.flush()
        return dict(label)

    def put(self):
        # Note: needs sending with 'Content-Type: application/json'
        label_id = int(self.request.matchdict['id'])
        label = DBSession.query(models.Label).get(label_id)
        if not label:
            raise HTTPNotFound
        body = self.request.json_body
        if 'name' in body:
            label.name = body['name']
        if 'notes' in body:
            note_ids = [n['id'] for n in body['notes']]
            note_query = DBSession.query(models.Note).filter(models.Note.id.in_(note_ids))
            label.notes = note_query.all()

    def delete(self):
        label_id = int(self.request.matchdict['id'])
        DBSession.query(models.Label).filter(models.Label.id==label_id).delete()

@resource(collection_path='/identities', path='/identities/{id}')
class Identity(object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):
        identities = DBSession.query(models.Identity).all()
        identity_list = [{'id': i.id, 'identifier': i.identifier, 'user_id': i.user_id} for i in identities]
        return {'identities': identity_list}

    def get(self):
        identity_id = int(self.request.matchdict['id'])
        identity = DBSession.query(models.Identity).get(identity_id)
        if identity:
            return dict(identity)
        else:
            raise HTTPNotFound

    def collection_post(self):
        # Note: needs sending with 'Content-Type: application/json'
        body = self.request.json_body
        identity = models.Label(body['identifier'], body['user_id'])
        DBSession.add(identifier)
        # Check for valid user_id
        # We flush the session to generate an id that we can add to the response
        DBSession.flush()
        return dict(identifier)

    def put(self):
        # Note: needs sending with 'Content-Type: application/json'
        identity_id = int(self.request.matchdict['id'])
        identity = DBSession.query(models.Identity).get(identity_id)
        if not identity:
            raise HTTPNotFound
        body = self.request.json_body
        if 'identifier' in body:
            identity.identifier = body['identifier']
        if 'user_id' in body:
            user = DBSession.query(models.User).get(body['user_id'])
            if user:
                identity.user = user
            else:
                raise HTTPBadRequest('Request body contains an invalid user id')

    def delete(self):
        label_id = int(self.request.matchdict['id'])
        DBSession.query(models.Label).filter(models.Label.id==label_id).delete()