import unittest

import sciter
from sciter.value import value, VALUE_TYPE


class TestSciterValue(unittest.TestCase):

    def test_01empty(self):
        v = value()
        self.assertIsNotNone(v)
        self.assertIsNotNone(v.data)
        self.assertIsNotNone(v.ptr)
        self.assertEqual(v.data.t, VALUE_TYPE.T_UNDEFINED)
        self.assertEqual(v.data.u, 0)
        self.assertEqual(v.data.d, 0)
        pass

    def test_02empty_eq(self):
        x, y = value(), value()
        self.assertEqual(x, y)
        self.assertIsNot(x, y)
        pass

    def test_03ctor(self):
        val = 7
        v = value(val)
        self.assertEqual(v.data.t, VALUE_TYPE.T_INT)
        self.assertEqual(v.data.u, 0)
        self.assertEqual(v.data.d, val)
        pass

    def test_04ctor_unsupported(self):
        with self.assertRaises(TypeError):
            s = set((1, 2, 3))
            x = value(s)
            x = x
        pass

    def test_05type(self):
        x, y = value(), value(7)
        self.assertEqual(x.get_type(), VALUE_TYPE.T_UNDEFINED)
        self.assertEqual(y.get_type(), VALUE_TYPE.T_INT)
        self.assertIs(x.get_type(py=True), type(None))
        self.assertIsNot(x.get_type(py=True), int)
        self.assertIs(y.get_type(py=True), int)
        self.assertIsNot(y.get_type(py=True), type(None))
        pass

    def test_06ctor_types(self):
        items = [None, False, True, 0, 1, 2.0, u'3', b'4', [3, 4], {'5': 5, '6': 6}]
        for item in items:
            with self.subTest(val=item):
                xval = value(item)
                self.assertIs(xval.get_type(py=True), type(item))
        # case for tuple
        item = (1, 2)
        xval = value(item)
        self.assertIs(xval.get_type(py=True), list)
        pass

    def test_07get_value(self):
        items = [None, False, True, 0, 1, 2.0, u'3', b'4', [3, 4], {'5': 5, '6': 6}]
        for item in items:
            with self.subTest(val=item):
                xval = value(item)
                val = xval.get_value()
                self.assertEqual(item, val)
        # case for tuple
        item = (1, 2)
        xval = value(item)
        val = xval.get_value()
        self.assertEqual(list(item), val)
        pass

    def test_08eq(self):
        x, y, z = value(), value(7), value(7)
        self.assertNotEqual(x, y)
        self.assertNotEqual(x, z)
        self.assertEqual(y, z)
        pass

    def test_09bool(self):
        items = [None, False, True, 0, 1, 0.0, 1.0, u'', u'3', (), (1, 2), [], [3, 4], {}, {'5': 5, '6': 6}]
        for item in items:
            with self.subTest(val=item):
                xval = value(item)
                if item:
                    self.assertTrue(xval)
                else:
                    self.assertFalse(xval)
        pass

    def test_10str(self):
        items = [None, False, True, 0, 1, 2.0, u'3', b'4', [3, 4], {'5': 5, '6': 6}]
        ritems = []
        sitems = []
        for item in items:
            with self.subTest(val=item):
                xval = value(item)
                rval = repr(xval)
                sval = str(xval)
                ritems.append(rval)
                sitems.append(sval)
                continue
                pass
        pass

    def test_11bytes(self):
        pass

    def test_12len(self):
        pass

    def test_13parse(self):
        items = ["", 'null', '1', '"2"', '2.0', 'true', '[3, 4]', '{"5": 5, "6": 6, seven: "seven"}']
        for item in items:
            with self.subTest(val=item):
                xval = value.parse(item)
                if xval:
                    self.assertTrue(xval)
                else:
                    self.assertFalse(xval)
        with self.assertRaises(sciter.ValueError):
            item = '{item: '
            xval = value.parse(item)
        pass
    
    # __getitem__ __setitem__ __delitem__ __contains__
    # Sequence operations
    # Mapping sequence operations


if __name__ == '__main__':
    import sys
    try:
        re = unittest.main(exit=False, failfast=True, verbosity=2)
    except:
        et, ev, eb = sys.exc_info()
        print(sys.exc_info())
    sys.exit(0)
