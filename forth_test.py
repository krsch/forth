import forth
import unittest

class TestForth(unittest.TestCase):
    def testParseSum(self):
        self.assertEqual(forth.parse('1 2 +'), [1,2,'+'])
    def testParseNumber(self):
        self.assertEqual(forth.parse('1'), [1])
    def testParseLargeNumber(self):
        self.assertEqual(forth.parse('1234567890'), [1234567890])
    def testParseFunc(self):
        self.assertEqual(
            forth.parse('1 2 DROP'),
            [1, 2, 'DROP']
        )
    def testExecNumber(self):
        self.assertAlmostEqual(
            forth.execute([123]),
            [123]
        )
    def testExecSum(self):
        self.assertAlmostEqual(
            forth.execute([13, 12, '+']),
            [12+13]
        )
    def testExecDrop(self):
        self.assertAlmostEqual(
            forth.execute([1, 2, 'DROP']),
            [1]
        )
    def testAll(self):
        self.assertEqual(
            forth.execute(forth.parse('1 2 3 * +'))[0],
            1+2*3
        )
    def testSub(self):
        self.assertEqual(
            forth.execute(forth.parse('''
            : TRIPLE DUP DUP ; 3 TRIPLE * +
            '''))[0], 3*3+3
        )