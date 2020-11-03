from ventana import *
from warning import *
from vencalendar import *
from datetime import datetime

import sys
import var, events, clients

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
        var.ui.btnAceptar.clicked.connect(events.Eventos.validarDNI)
        var.rbtSex = (var.ui.rbtFem, var.ui.rbtMasc)
        for i in var.rbtSex:
            i.toggled.connect(events.Eventos.selSexo)

        var.chkpago = (var.ui.chkEfect, var.ui.chkTarj, var.ui.chkTrans)
        for i in var.chkpago:
            i.stateChanged.connect(events.Eventos.selPago)

        clients.Clientes.cargarProv()
        var.ui.cmbProv.activated[str].connect(clients.Clientes.selProv)
        #var.ui.entDNI.editingFinished.connect(events.Eventos.validarDNI)
        '''
        Controles del menubar
        '''
        QtWidgets.QAction(self).triggered.connect(self.close)
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)

class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.avisoSalir = Ui_Dialog()
        var.avisoSalir.setupUi(self)
        var.avisoSalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.Salir)
        var.avisoSalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.No).clicked.connect(events.Eventos.Salir)

class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        var.dlgCalendar = Ui_calendar()
        var.dlgCalendar.setupUi(self)
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgCalendar.Calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, 1)))
        var.dlgCalendar.Calendar.clicked.connect(clients.Clientes.cargarFecha)
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)


def closeEvent(self, event):
    event.Eventos.Salir()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())