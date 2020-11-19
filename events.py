import sys, var, warning

class Eventos():

    def Salir(event):
        '''
        Módulo para cerrar el programa
        :return:
        '''
        try:
            var.dlgsalir.show()
            if var.dlgsalir.exec_():
                #print(event)
                sys.exit()
            else:
                var.dlgsalir.hide()
                event.ignore()

        except Exception as error:
            print('Error %s' % str(error))

    def closeSalir(event):
        try:
            if var.dlgsalir.exec_():
                print(event)
                var.dlgsalir.hide()
               #necesario para que ignore X de la ventana
        except Exception as error:
            print('Error %s' % str(error))

    def cargarProv():
        """
        carga las provincias al iniciar el programa
        :return:
        """
        try:
            prov = ['','A Coruña', 'Lugo', 'Ourense', 'Pontevedra', 'Vigo']
            for i in prov:
                var.ui.cmbProv.addItem(i)

        except Exception as error:
            print('Error: %s' % str(error))
