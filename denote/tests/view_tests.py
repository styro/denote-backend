import unittest
import transaction

from pyramid import testing

from ..models import DBSession

class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from ..models import (
            Base,
            User,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = User(name=u'one')
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_it(self):
        from ..views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['user'].name, 'one')
        self.assertEqual(info['project'], 'pyramid-alchemy')
