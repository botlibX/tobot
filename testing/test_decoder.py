# This file is placed in the Public Domain.


import unittest


from tobot.objects import Object
from tobot.serials import loads, dumps


class TestDecoder(unittest.TestCase):

    def test_loads(self):
        obj = Object()
        obj.test = "bla"
        oobj = loads(dumps(obj))
        self.assertEqual(oobj["test"], "bla")

    def test_doctest(self):
        self.assertTrue(__doc__ is None)
