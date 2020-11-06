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