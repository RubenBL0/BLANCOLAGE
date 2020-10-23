from ventana import *
import sys
import var, events

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_VenPrincipal()
        var.ui.setupUi(self)

        #Código de conexión de los eventos

        '''
        Botones
        '''
        #var.ui.btnAceptar.clicked.connect(events.Eventos.Saludo)
        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)

        '''
        Controles del menubar
        '''
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())