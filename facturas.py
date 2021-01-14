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