import os
import sys
import datetime
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Base,
    Note,
    User,
    Label,
    Identity,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        u1 = User('User One')
        u2 = User('User Two')
        DBSession.add_all([u1, u2])
        i1 = Identity(identifier='identity1', user=u1)
        i2 = Identity(identifier='identity2', user=u1)
        i3 = Identity(identifier='identity3', user=u2)
        DBSession.add_all([i1, i2, i3])
        l1 = Label('first label')
        l2 = Label('second label')
        l3 = Label('third label')
        l4 = Label('fourth label')
        DBSession.add_all([l1, l2, l3, l4])
        n1 = Note(title='First note', content='First note content\nsecond line')
        n1.created_by = u1
        n1.created_on -= datetime.timedelta(days=5, hours=1, minutes=9)
        n1.labels = [l1, l3]
        n2 = Note(title='Second note', content='Second note content\nsecond line')
        n2.created_by = u2
        n2.created_on -= datetime.timedelta(days=4, hours=20, minutes=14)
        n2.labels = [l2, l3]
        n3 = Note(title='Third note', content='Third note content\nsecond line')
        n3.created_by = u1
        n3.created_on -= datetime.timedelta(days=4, hours=2, minutes=2)
        n3.labels = [l1]
        n4 = Note(title='Fourth note', content='Fourth note content\nsecond line')
        n4.created_by = u1
        n4.created_on -= datetime.timedelta(days=3, hours=18, minutes=41)
        n4.labels = [l1, l3, l4]
        n5 = Note(title='Fifth note', content='Fifth note content\nsecond line')
        n5.created_by = u2
        n5.created_on -= datetime.timedelta(days=1, hours=3, minutes=19)
        n5.labels = [l3, l4]
        n6 = Note(title='Sixth note', content='Sixth note content\nsecond line')
        n6.created_by = u1
        n6.created_on -= datetime.timedelta(days=0, hours=1, minutes=39)
        n6.labels = [l4]
        DBSession.add_all([n1, n2, n3, n4, n5, n6])
