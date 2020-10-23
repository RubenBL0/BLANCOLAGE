import var, sys

class Eventos():

    def Saludo(self):
        try:
            var.ui.lblSaludo.setText("Has pulsado el botón")
        except Exception as error:
            print("Error: %s " % str(error))

    def Salir(self):
        try:
            sys.exit()
        except Exception as error:
            print("Error %s " % str(error))