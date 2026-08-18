import unittest

from src.main import Calculadora

class TestMathOperations(unittest.TestCase):

    def setUp(self):
        self.objCalculadora = Calculadora()

    def test_add(self):
        self.assertEqual(self.objCalculadora.suma(1, 2), 3)
        self.assertEqual(self.objCalculadora.suma(-1, 1), 0)
        self.assertEqual(self.objCalculadora.suma(-1, -1), -2)

    def test_subtract(self):
        self.assertEqual(self.objCalculadora.resta(2, 1), 1)
        self.assertEqual(self.objCalculadora.resta(1, 1), 0)
        self.assertEqual(self.objCalculadora.resta(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(self.objCalculadora.multiplicacion(2, 3), 6)
        self.assertEqual(self.objCalculadora.multiplicacion(-1, 1), -1)
        self.assertEqual(self.objCalculadora.multiplicacion(-1, -1), 1)

    def test_divide(self):
        self.assertEqual(self.objCalculadora.division(6, 3), 2)
        self.assertRaises(ZeroDivisionError, self.objCalculadora.division, 1, 0)