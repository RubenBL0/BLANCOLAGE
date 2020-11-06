from ventana import *
from warning import *
from vencalendar import *
from datetime import datetime

import sys, var, events, clients


class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.dlgsalir = Ui_Dialog()
        var.dlgsalir.setupUi(self)
        var.dlgsalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.Salir)
        var.dlgsalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.No).clicked.connect(events.Eventos.Salir)

class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        var.dlgcalendar = Ui_dlgCalendar()
        var.dlgcalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgcalendar.Calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        var.dlgcalendar.Calendar.clicked.connect(clients.Clientes.cargarFecha)


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_VenPrincipal()
        var.ui.setupUi(self)
        var.dlgsalir = DialogSalir()
        var.dlgcalendar = DialogCalendar()

        #Código de conexión de los eventos

        '''
        Botones
        '''
        #var.ui.btnAceptar.clicked.connect(events.Eventos.Saludo)
        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)
        var.ui.entDNI.editingFinished.connect(clients.Clientes.validoDni)
        var.rbtSex = (var.ui.rbtFem, var.ui.rbtMasc)
        for i in var.rbtSex:
            i.toggled.connect(clients.Clientes.selSexo)

        var.chkpago = (var.ui.chkEfect, var.ui.chkTarj, var.ui.chkTrans)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)

        clients.Clientes.cargarProv()
        var.ui.cmbProv.activated[str].connect(clients.Clientes.selProv)
        #var.ui.entDNI.editingFinished.connect(events.Eventos.validarDNI)
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)
        var.ui.btnAceptar.clicked.connect(clients.Clientes.showClientes)
        '''
        Controles del menubar
        '''
        QtWidgets.QAction(self).triggered.connect(self.close)
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)

def closeEvent(self, event):
    event.Eventos.Salir(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())