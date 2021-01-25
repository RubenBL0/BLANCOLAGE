import var, conexion
from ventana import *

class Facturas():

    def abrirCalendar():
        '''
        Abrir la ventana calendario específica para el módulo de facturas (no el de clientes)
        '''
        try:
            var.dlgcalendarfact.show()
        except Exception as error:
            print('Error al mostrar el calendario: %s ' % str(error))

    def cargarFecha(qDate):
        ''''
        Carga la fecha cuando clickamos en la ventana del calendario
        '''
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.editFechaFact.setText(str(data))
            var.dlgcalendarfact.hide()
        except Exception as error:
            print('Error al cargar la fecha: %s ' % str(error))

    def limpiarFactura():
        '''
        Limpia los datos del formulario
        '''
        fields = [var.ui.lblCodFact, var.ui.editFechaFact, var.ui.editDniFact,var.ui.editApelFact]

        for i in range(len(fields)):
            fields[i].setText('')

    def altaFactura():
        '''
        Da de alta una factura vacía, utilizando el nombre, apellidos y la fecha introducidos
        '''
        try:
            factura = [var.ui.editDniFact, var.ui.editApelFact, var.ui.editFechaFact]
            newfact = []

            for i in factura:
                newfact.append(i.text())

            print(newfact)
            conexion.Conexion.altaFact(newfact)
            conexion.Conexion.mostrarFacturas()
        except Exception as error:
            print("Error %s: " % str(error))

    def cargarFactura():
        '''
        Carga los datos seleccionados en la tabla en el formulario de facturas
        '''
        try:
            fila = var.ui.tabFacturas.selectedItems()
            var.ui.lblCodFact.setText(fila[0].text())
            conexion.Conexion.cargarFactura()
        except Exception as error:
            print('Error al cargar factura %s' % str(error))

    def borrarFactura():
        try:
            codfact = var.ui.lblCodFact.text()
            conexion.Conexion.bajaFactura(codfact)
            Facturas.limpiarFactura()
            conexion.Conexion.mostrarFacturas(None)

        except Exception as error:
            print('Error al eliminar la factura: %s' % str(error))

    def buscarFactura():
        try:
            dni = var.ui.editDniFact.text()
            conexion.Conexion.buscarFactura(dni)

        except Exception as error:
            print('Error al buscar el cliente: %s' % str(error))