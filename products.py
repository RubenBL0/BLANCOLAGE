import var, conexion
from ventana import *

class Productos():
    '''
    Eventos de la clase Productos
    '''
    def altaProd():
        '''
        Módulo que recoge los datos del formulario de productos para darlo de alta
        :return: None

        '''
        try:
            prod = [var.ui.editNomeProd, var.ui.editPrezoProd, var.ui.editStockProd]
            newprod = []

            for i in prod:
                newprod.append(i.text())

            if (newprod[0] == "" or newprod[1] == "" or newprod[2] == ""):
                print("Faltan datos")

            else:
                print(newprod)

                conexion.Conexion.altaProd(newprod)
                conexion.Conexion.mostrarProductos(None)

        except Exception as error:
            print("Error al dar de alta un producto: %s" % str(error))

    def cargarProd():
        '''
        Módulo que carga en el formulario los datos del producto seleccionado
        :return: None

        '''
        try:
            fila = var.ui.tableProd.selectedItems()
            prod = [var.ui.lblCodProd, var.ui.editPrezoProd, var.ui.editPrezoProd, var.ui.editStockProd]
            if fila:
                fila = [dato.text() for dato in fila]
            i = 0
            for i, dato in enumerate(prod):
                dato.setText(fila[i])
            conexion.Conexion.cargarProducto()
        except Exception as error:
            print('Error al cargar producto %s ' % str(error))

    def limpiarProd():
        '''
        Módulo que limpia los datos del formulario de productos
        :return: None

        '''
        try:
            prod = [var.ui.lblCodProd, var.ui.editNomeProd, var.ui.editPrezoProd, var.ui.editStockProd]
            for i in range(len(prod)):
                prod[i].setText('')
            var.ui.lblStatus.setText("Bienvenido a 2º DAM")
        except Exception as error:
            print('Error al limpiar producto %s ' % str(error))

    def bajaProd(self):
        '''
        Módulo que recoge el código del producto seleccionado para darlo de baja
        :return: None

        '''
        try:
            codigo = var.ui.lblCodProd.text()
            conexion.Conexion.bajaProd(codigo)
            Productos.limpiarProd()
            conexion.Conexion.mostrarProductos(None)
            var.ui.lblStatus.setText("Producto con código " + codigo + " eliminado")

        except Exception as error:
            print("Error baja producto: %s " % str(error))

    def modifProd(self):
        '''
        Módulo que recoge el código de un producto y los nuevos datos, para modificarlo
        :return: None

        '''
        try:
            newdata = []
            prod = [var.ui.editNomeProd, var.ui.editPrezoProd, var.ui.editStockProd]
            for i in prod:
                newdata.append(i.text())
            cod = var.ui.lblCodProd.text()
            conexion.Conexion.modifProd(cod, newdata)
            conexion.Conexion.mostrarProductos(self)

        except Exception as error:
            print("Error cargar productos: %s" % str(error))