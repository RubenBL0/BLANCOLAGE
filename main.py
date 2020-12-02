from ventana import *
from warning import *
from vencalendar import *
from ventanaborrar import *
from datetime import datetime, date
import sys, var, events, clients, conexion
import locale
from PyQt5.QtPrintSupport import QPrintDialog


locale.setlocale(locale.LC_ALL, 'es-ES')

class PrintDialogAbrir(QPrintDialog):
    def __init__(self):
        super(PrintDialogAbrir, self).__init__()
        self.setModal(True)


class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.dlgsalir = Ui_Dialog()
        var.dlgsalir.setupUi(self)
        var.dlgsalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.Salir)
        self.setModal(True)

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
        self.setModal(True)

class DialogBorrar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogBorrar, self).__init__()
        var.dlgborrar = Ui_DialogBorrar()
        var.dlgborrar.setupUi(self)
        var.dlgborrar.btnBoxBorrar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(clients.Clientes.bajaCliente)
        self.setModal(True)

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()
        self.setModal(True)

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_VenPrincipal()
        var.ui.setupUi(self)
        var.dlgsalir = DialogSalir()
        var.dlgcalendar = DialogCalendar()
        var.filedlgabrir = FileDialogAbrir()
        var.dlgimprimir = PrintDialogAbrir()
        var.dlgborrar = DialogBorrar()
        '''
        poner la fecha actual
        '''
        var.ui.lblFecha.setText(str(date.today().strftime("%A, %d de %B de %Y")))

        '''
        colección de datos
        '''
        var.rbtsex = (var.ui.rbtFem, var.ui.rbtMasc)
        var.chkpago = (var.ui.chkEfec, var.ui.chkTar, var.ui.chkTrans)

        '''
        conexion de eventos con los objetos
        estamos conectando el código con la interfaz gráfico
        botones formulario cliente
        '''
        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
        var.ui.editDni.editingFinished.connect(lambda: clients.Clientes.validoDni())
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)
        var.ui.btnAltaCli.clicked.connect(clients.Clientes.altaCliente)
        var.ui.btnLimpiarCli.clicked.connect(clients.Clientes.limpiarCli)
        var.ui.btnBajaCli.clicked.connect(events.Eventos.Borrar)
        var.ui.btnModifCli.clicked.connect(clients.Clientes.modifCliente)
        var.ui.btnReloadCli.clicked.connect(clients.Clientes.reloadCli)
        var.ui.btnBuscarCli.clicked.connect(conexion.Conexion.cargarCliente)
        var.ui.statusbar.addPermanentWidget(var.ui.lblStatus, 1)
        var.ui.lblStatus.setText("Bienvenido a 2º DAM")
        var.ui.toolbarBackup.triggered.connect(events.Eventos.Backup)
        var.ui.toolbarSalir.triggered.connect(events.Eventos.Salir)
        var.ui.toolbarAbrir.triggered.connect(events.Eventos.AbrirDir)
        var.ui.actionAbrir.triggered.connect(events.Eventos.AbrirDir)
        var.ui.toolbarImprimir.triggered.connect(events.Eventos.Imprimir)
        var.ui.spinEdad.setValue(18)
        var.ui.spinEdad.setMaximum(65)
        var.ui.spinEdad.setMinimum(16)
        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)

        var.ui.cmbProv.activated[str].connect(clients.Clientes.selProv)
        var.ui.tableCli.clicked.connect(clients.Clientes.cargarCli)
        var.ui.tableCli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        events.Eventos.cargarProv()
        '''
        módulos conexion base datos
        '''

        conexion.Conexion.db_connect(var.filebd)
        # conexion.Conexion()
        conexion.Conexion.mostrarClientes(self)

    def closeEvent(self, event):
        if event:
            events.Eventos.Salir(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())