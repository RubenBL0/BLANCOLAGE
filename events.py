import var, sys, clients


class Eventos():

    #Eventos Generales

    def Salir(self):
        try:
            sys.exit()
        except Exception as error:
            print("Error %s " % str(error))


    def validarDNI(self):
        try:
            dni = var.ui.entDNI.text()
            if clients.Clientes.validarDNI(dni):
                var.ui.lblValido.setStyleSheet("QLabel {color: green;}")
                var.ui.lblValido.setText("V")
                var.ui.entDNI.setText(dni.upper())
            else:
                var.ui.lblValido.setStyleSheet("QLabel {color: red;}")
                var.ui.lblValido.setText("X")
                var.ui.entDNI.setText(dni.upper())

        except Exception as error:
            print("Error: %s " % str(error))


    def selSexo(self):
        try:
            if var.ui.rbtFem.isChecked():
                var.ui.lblPrueba.setText("femenino")
            if var.ui.rbtMasc.isChecked():
                var.ui.lblPrueba.setText("masculino")
        except Exception as error:
            print("Error: %s" % str(error))

    def selPago(self):
        try:
            if var.ui.chkEfect.isChecked():
                print("pagas con efectivo")
            if var.ui.chkTarj.isChecked():
                print("pagas con tarjeta")
            if var.ui.chkTrans.isChecked():
                print("pagas con transferencia")
        except Exception as error:
            print("Error: %s " % str(error))