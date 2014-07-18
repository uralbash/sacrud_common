#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Common tools for fixtures
"""
import os
from random import randint

import transaction
from sacrud.action import CRUD


class Fixture(object):
    def __init__(self, DBSession):
        self.DBSession = DBSession

    def add(self, model, fixtures, delete=True):
        """
        Add fixtures to database.

        Example::

        hashes = ({'foo': "{'foo': 'bar', '1': '2'}}", {'foo': "{'test': 'data'}"})
        add_fixture(TestHSTORE, hashes)
        """
        if delete:
            model.__table__.create(checkfirst=True, bind=self.DBSession.bind.engine)
            self.DBSession.query(model).delete()
            transaction.commit()
        for fixture in fixtures:
            CRUD(self.DBSession, model, request=fixture).add()

    def rand_id(self, model):
        qty = len(self.DBSession.query(model).all())
        return randint(1, qty)


def add_extension(engine, *args):
    """
    Add extension to PostgreSQL database.
    """
    conn = engine.connect()
    for ext in args:
        conn.execute('CREATE EXTENSION IF NOT EXISTS "%s"' % ext)
    conn.execute('COMMIT')
    conn.close()


def add_triggers(engine, SQL_path, *args):
    """
    Add triggers from files
    """
    conn = engine.connect()
    for trigger in args:
        path_to_trigger = os.path.join(SQL_path, trigger)
        # only nobomb files
        conn.execute(open(path_to_trigger, 'r').read().decode('utf-8'))
    conn.execute('COMMIT')
    conn.close()