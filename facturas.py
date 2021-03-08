import var, conexion
from ventana import *


class Facturas():

    def abrirCalendar():
        '''
        Módulo que  la ventana calendario específica para el módulo de facturas
        :return: None

        '''
        try:
            var.dlgcalendarfact.show()
        except Exception as error:
            print('Error al mostrar el calendario: %s ' % str(error))

    def cargarFecha(qDate):
        ''''
        Módulo que carga la fecha seleccionada en el formulario
        :return: None

        '''
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.editFechaFact.setText(str(data))
            var.dlgcalendarfact.hide()
        except Exception as error:
            print('Error al cargar la fecha: %s ' % str(error))

    def limpiarFactura():
        '''
        Módulo que limpia los datos del formulario
        :return: None

        '''
        fields = [var.ui.lblCodFact, var.ui.editFechaFact, var.ui.editDniFact, var.ui.editApelFact]

        for i in range(len(fields)):
            fields[i].setText('')

    def altaFactura(self):
        '''
        Módulo que da de alta una factura nueva, utilizando el nombre, apellidos y la fecha introducidos
        :return: None

        '''
        try:
            dni = var.ui.editDniFact.text()
            apel = var.ui.editApelFact.text()
            fecha = var.ui.editFechaFact.text()
            if dni != '' and apel != '' and fecha != '':
                conexion.Conexion.altaFact(dni, apel, fecha)
            else:
                print('Faltan datos')
            conexion.Conexion.mostrarFacturas(self)
            conexion.Conexion.cargarFac2(self)
            Facturas.prepararTablaventas(0)
        except Exception as error:
            print("Error %s: " % str(error))

    def cargarFactura(self):
        '''
        Módulo que carga los datos de la factura seleccionada en el formulario
        :return: None

        '''
        try:
            var.subtotal = 0.00
            var.iva = 0.00
            var.total = 0.00
            fila = var.ui.tabFacturas.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            var.ui.lblCodFact.setText(str(fila[0]))
            var.ui.editFechaFact.setText(str(fila[1]))
            conexion.Conexion.cargarFactura(str(fila[0]))
            conexion.Conexion.mostrarVentas(str(fila[0]))
        except Exception as error:
            print('Error al cargar factura %s' % str(error))

    def borrarFactura():
        '''
        Módulo que elimina la factura seleccionada de la base de datos
        :return: None

        '''
        try:
            codfact = var.ui.lblCodFact.text()
            conexion.Conexion.bajaFactura(codfact)
            Facturas.limpiarFactura()
            conexion.Conexion.mostrarFacturas(None)
            Facturas.prepararTablaventas(0)

        except Exception as error:
            print('Error al eliminar la factura: %s' % str(error))

    def buscarFactura():
        '''
        Módulo que recoge el DNI del formulario para buscar las facturas asociadas al cliente
        :return: None

        '''
        try:
            dni = var.ui.editDniFact.text()
            print(dni)
            conexion.Conexion.buscarFactura(dni)

        except Exception as error:
            print('Error al buscar el cliente: %s' % str(error))

    def prepararTablaventas(index):
        '''
        Módulo que prepara tabla Ventas, carga un combo en la tabla
        y carga dicho combo con los datos del producto
        :param index: La fila de la tabla en la que se insertará
        :type index: int
        :return: None

        '''
        try:
            var.cmbVenta = QtWidgets.QComboBox()
            conexion.Conexion.cargarCmbventa(var.cmbVenta)
            var.ui.tabVentas.setRowCount(index + 1)
            var.ui.tabVentas.setItem(index, 0, QtWidgets.QTableWidgetItem())
            var.ui.tabVentas.setCellWidget(index, 1, var.cmbVenta)
            var.ui.tabVentas.setItem(index, 2, QtWidgets.QTableWidgetItem())
            var.ui.tabVentas.setItem(index, 3, QtWidgets.QTableWidgetItem())
            var.ui.tabVentas.setItem(index, 4, QtWidgets.QTableWidgetItem())
        except Exception as error:
            print('Error Preparar tabla de ventas: %s ' % str(error))

    def altaVenta(self):
        '''
        Módulo que da de alta la venta de un producto en la factura
        :return: None

        '''
        try:
            var.subtot = 0.00
            venta = []
            codigo = var.ui.lblCodFact.text()
            venta.append(int(codigo))
            articulo = var.cmbVenta.currentText()
            dato = conexion.Conexion.obtenerCodPrec(articulo)
            venta.append(int(dato[0]))
            venta.append(articulo)
            fila = var.ui.tabVentas.currentRow()
            cantidad = var.ui.tabVentas.item(fila, 2).text()
            cantidad = cantidad.replace(',', '.')
            venta.append(int(cantidad))
            precio = dato[1].replace(',', '.')
            venta.append(round(float(precio), 2))
            subtotal = round(float(cantidad) * float(dato[1]), 2)  # probar precio
            print(subtotal)
            venta.append(subtotal)
            venta.append(fila)
            print(venta)
            if codigo != '' and articulo != '' and cantidad != '':
                conexion.Conexion.altaVenta(venta)
                Facturas.mostrarVentas()
            else:
                var.ui.lblStatus.setText('Faltan datos')

        except Exception as error:
            print("Error al dar de alta una venta: " % str(error))

    def mostrarVentas():
        '''
        Módulo que llama a la conexión con la base de datos para mostrar todas las ventas en la tabla de ventas
        :return: None

        '''
        try:
            var.cmbVenta = QtWidgets.QComboBox()
            conexion.Conexion.cargarCmbventa(var.cmbVenta)
            codigo = var.ui.lblCodFact.text()
            conexion.Conexion.mostrarVentas(codigo)

        except Exception as error:
            print("Error al mostrar las ventas de la factura: " % str(error))

    def anularVenta(self):
        '''
        Módulo que anula una venta hecha en una factura
        :return: None

        '''
        try:
            fila = var.ui.tabVentas.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            codigo = int(fila[0])
            conexion.Conexion.anulaVenta(codigo)
            Facturas.mostrarVentas()

        except Exception as error:
            print("Error al borrar la factura: " % str(error))
