import sys, var, clients


class Eventos():

    def Salir(event):
        '''
        Módulo para cerrar el programa
        :return:
        '''
        try:
            var.dlgsalir.show()
            if var.dlgsalir.exec_():
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
                var.dlgsalir.hide()  # Necesario para que ignore X de la ventana
        except Exception as error:
            print('Error %s' % str(error))

    def cargarProv():
        """
        carga las provincias al iniciar el programa
        :return:
        """
        try:
            prov = ['', 'A Coruña', 'Lugo', 'Ourense', 'Pontevedra', 'Vigo']
            for i in prov:
                var.ui.cmbProv.addItem(i)

        except Exception as error:
            print('Error: %s' % str(error))

    def Backup(self):
        try:
            print("Aquí hace el backup")

        except Exception as error:
            print("Error: %s" % str(error))

    def AbrirDir(self):
        try:
            var.filedlgabrir.show()

        except Exception as error:
            print("Error: %s" % str(error))

    def Imprimir(self):
        try:
            var.dlgimprimir.show()

        except Exception as error:
            print("Error: %s" % str(error))

    def Borrar(self):
        try:
            var.dlgborrar.show()
            if var.dlgborrar.exec_():
                clients.Clientes.bajaCliente
            else:
                var.dlgborrar.hide()

        except Exception as error:
            print("Error: %s" % str(error))
