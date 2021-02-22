import unittest, clients, conexion, var


class MyTestCase(unittest.TestCase):

    def test_dni(self):
        dni = "00000000T"
        mes = "DNI incorrecto"
        res = clients.Clientes.validarDni(dni)
        self.assertTrue(res, mes)

    def test_conexion(self):
        res = conexion.Conexion.db_connect(var.filebd)
        mes = "Error en la conexión"
        self.assertTrue(res, mes)


if __name__ == '__main__':
    unittest.main()
