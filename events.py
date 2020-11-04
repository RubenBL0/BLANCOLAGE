import var, sys


class Eventos():

    #Eventos Generales

    def Salir(event):
        try:
            var.dlgsalir.show()
            if var.dlgsalir.exec_():
                sys.exit()
            else:
                var.dlgsalir.hide()
                event.ignore()
        except Exception as error:
            print("Error %s " % str(error))


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