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
        items = [None, 1, u'hello']
        for item in items:
            with self.subTest(val=item):
                xval = value(item)
                with self.assertRaises(TypeError):
                    bval = bytes(xval)
                continue
        item = b'hello, world'
        xval = value(item)
        self.assertEqual(bytes(xval), bytes(item))
        pass

    def test_12len(self):
        items = [[], {}, [3, 4], {'5': 5, '6': 6}]
        for item in items:
            with self.subTest(val=item):
                xval = value(item)
                self.assertEqual(len(xval), len(item))
                continue

        items = [None, False, True, 0, 1, 2.0, u'3', b'4', ]
        for item in items:
            with self.subTest(val=item):
                with self.assertRaises(AttributeError):
                    xval = value(item)
                    xval.length()
                    continue
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

    def test_14getitem(self):
        items = ['[3,4,5]', '{"five": 5, "seven": 7}']
        with self.subTest(val=items[0]):
            xval = value.parse(items[0])

            self.assertEqual(xval[0], value(3))
            self.assertEqual(xval[1], value(4))
            self.assertEqual(xval[-1],value(5))

            with self.assertRaises(IndexError):
                r = xval[20]

            with self.assertRaises(TypeError):
                r = xval['key']

        with self.subTest(val=items[1]):
            xval = value.parse(items[1])

            self.assertEqual(xval['five'], value(5))

            with self.assertRaises(KeyError):
                r = xval['not exist']
        pass

    def test_16setitem(self):
        xval = value([1, 2, 3])
        xval[0] = 7
        xval[-1] = 7
        self.assertEqual(xval, value([7, 2, 7]))

        xval = value({'0': 0})
        xval['0'] = 'zero'
        xval['7'] = 7
        self.assertEqual(xval['0'], value('zero'))
        self.assertEqual(xval['7'], value(7))

        # undefined -> array
        xval = value([])
        self.assertEqual(xval.get_type(), VALUE_TYPE.T_ARRAY)

        xval = value()
        xval[0] = 7
        self.assertEqual(xval.get_type(), VALUE_TYPE.T_ARRAY)
        self.assertEqual(xval[0], value(7))

        with self.assertRaises(KeyError):
            xval = value([])  # array
            xval['key'] = 'value'

        # undefined -> map
        xval = value({})
        self.assertEqual(xval.get_type(), VALUE_TYPE.T_MAP)

        xval = value()
        xval['0'] = 7
        self.assertEqual(xval.get_type(), VALUE_TYPE.T_MAP)
        self.assertEqual(xval['0'], value(7))
        pass

    @unittest.skip("__delitem__ is not supported")
    def test_17delitem(self):
        items = [i for i in range(5)]
        item = dict(zip(map(lambda x: str(x), items), items))
        xval = value(item)
        del xval['2']  # middle
        del xval['0']  # first
        del xval['4']  # last
        self.assertEqual(xval, value({1: 1, 3: 3}))
        pass

    def test_18contains(self):
        xval = value({'0': 0, '7': 7})
        self.assertIn('0', xval)
        self.assertIn('7', xval)
        self.assertNotIn('8', xval)
        pass

    def test_19explicit(self):
        # null
        xval = value.null()
        self.assertTrue(xval.is_null())
        self.assertFalse(xval)

        # #symbol
        xval = value.symbol('hello')
        self.assertTrue(xval.is_symbol())
        self.assertTrue(xval.is_string())   # string is a generic type for error, symbol and string itself
        self.assertEqual(xval.get_value(), 'hello')

        # secure string
        xval = value.secure_string('secure')
        self.assertTrue(xval.is_string())
        self.assertEqual(xval.get_type(with_unit=True), (VALUE_TYPE.T_STRING, 2))  # VALUE_UNIT_TYPE_STRING.UT_STRING_SECURE
        self.assertEqual(xval.get_value(), 'secure')

        # error
        xval = value(ValueError('error'))
        self.assertTrue(xval.is_error_string())
        self.assertEqual(xval.get_value(), 'error')  # doesn't raise exception.

        pass

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
