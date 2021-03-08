import unittest, clients, conexion, var
from PyQt5 import QtSql


class MyTestCase(unittest.TestCase):

    def test_dni(self):
        '''
        Módulo que testea que la función de validar el DNI funciona correctamente
        :return: None

        '''
        dni = "00000000T"
        mes = "DNI incorrecto"
        res = clients.Clientes.validarDni
        self.assertTrue(res, mes)

    def test_conexion(self):
        '''
        Módulo que testea que la conexión con la base de datos se establece correctamente
        :return: None

        '''
        res = conexion.Conexion.db_connect(var.filebd)
        mes = "Error en la conexión"
        self.assertTrue(res, mes)

    def test_codigoPrecio(self):
        '''
        Módulo que testea que la función de obtener el código y precio de un artículo devuelve los valores acertados
        :return: None

        '''
        conexion.Conexion.db_connect(var.filebd)

        articulo = "Champiñones"
        cp = conexion.Conexion.obtenerCodPrec(articulo)

        self.assertEqual(int(cp[0]), 7, "El código es incorrecto")
        self.assertEqual(float(cp[1]), 0.60, "El precio es incorrecto")

if __name__ == '__main__':
    unittest.main()
