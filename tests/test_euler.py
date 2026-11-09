"""Pruebas automáticas para la aproximación de Euler."""
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import comparar, metodo_euler, solucion_exacta


class TestEuler(unittest.TestCase):
    def test_numero_de_puntos_y_intervalo(self):
        puntos = metodo_euler(0, 1, 1, 0.2)
        self.assertEqual(len(puntos), 6)
        self.assertAlmostEqual(puntos[0][0], 0)
        self.assertAlmostEqual(puntos[-1][0], 1)

    def test_aproximacion_final(self):
        self.assertAlmostEqual(metodo_euler(0, 1, 1, 0.2)[-1][1], 2.48832)

    def test_solucion_exacta(self):
        self.assertAlmostEqual(solucion_exacta(1), math.e)

    def test_error(self):
        filas = comparar(metodo_euler(0, 1, 1, 0.2))
        self.assertAlmostEqual(filas[-1][3], math.e - 2.48832)

    def test_paso_invalido(self):
        with self.assertRaises(ValueError):
            metodo_euler(0, 1, 1, 0.3)


if __name__ == "__main__":
    unittest.main()
