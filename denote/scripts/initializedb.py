import os
import sys
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
        i1 = Identity(name='identity1', user=u1)
        i2 = Identity(name='identity2', user=u1)
        i3 = Identity(name='identity3', user=u2)
        DBSession.add_all([i1, i2, i3])
        l1 = Label('first label')
        l2 = Label('second label')
        l3 = Label('third label')
        DBSession.add_all([l1, l2, l3])
        n1 = Note(title='First note', content='First note content\nsecond line')
        n1.created_by = u1
        n1.labels = [l1, l3]
        n2 = Note(title='Second note', content='Second note content\nsecond line')
        n2.created_by = u2
        n2.labels = [l2, l3]
        n3 = Note(title='Third note', content='Third note content\nsecond line')
        n3.created_by = u1
        n3.labels = [l1]
        DBSession.add_all([n1, n2, n3])
