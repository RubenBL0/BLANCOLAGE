from ventana import *
from about import *
from warning import *
from vencalendar import *
from ventanaborrar import *
from datetime import datetime, date
import sys, var, events, clients, conexion, products, printer, facturas
import locale
from PyQt5.QtPrintSupport import QPrintDialog


locale.setlocale(locale.LC_ALL, 'es-ES')

class DialogAbout(QtWidgets.QDialog):
    def __init__(self):
        super(DialogAbout, self).__init__()
        var.dlgabout = Ui_dialogAbout()
        var.dlgabout.setupUi(self)

# Ventana de imprimir
class PrintDialogAbrir(QPrintDialog):
    def __init__(self):
        super(PrintDialogAbrir, self).__init__()
        self.setModal(True)


# Ventana modal de salir de la aplicación
class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.dlgsalir = Ui_Dialog()
        var.dlgsalir.setupUi(self)
        var.dlgsalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.Salir)
        self.setModal(True)


# Ventana del widget calendar para clientes
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

# Ventana del widget calendar para facturas
class DialogCalendarFactura(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendarFactura, self).__init__()
        var.dlgcalendar = Ui_dlgCalendar()
        var.dlgcalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgcalendar.Calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        var.dlgcalendar.Calendar.clicked.connect(facturas.Facturas.cargarFecha)
        self.setModal(True)

class CmbVenta(QtWidgets.QComboBox):
    def __init__(self):
        super(CmbVenta, self).__init__()
        var.cmbventa = QtWidgets.QComboBox()

# Ventana modal para pedir confirmación al borrar un elemento de la base de datos
class DialogBorrar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogBorrar, self).__init__()
        var.dlgborrar = Ui_DialogBorrar()
        var.dlgborrar.setupUi(self)
        var.dlgborrar.btnBoxBorrar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(clients.Clientes.bajaCliente)
        self.setModal(True)

# Ventana para abrir un archivo
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
        var.dlgabout = DialogAbout()
        var.dlgcalendarfact = DialogCalendarFactura()
        var.cmbVenta = QtWidgets.QComboBox()

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
        var.ui.actionAbout.triggered.connect(events.Eventos.About)
        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
        var.ui.editDni.editingFinished.connect(lambda: clients.Clientes.validoDni())
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)
        var.ui.btnAltaCli.clicked.connect(clients.Clientes.altaCliente)
        var.ui.btnLimpiarCli.clicked.connect(clients.Clientes.limpiarCli)
        var.ui.btnBajaCli.clicked.connect(events.Eventos.Borrar)
        var.ui.btnModifCli.clicked.connect(clients.Clientes.modifCliente)
        var.ui.btnReloadCli.clicked.connect(clients.Clientes.reloadCli)
        var.ui.btnBuscarCli.clicked.connect(clients.Clientes.buscarCli)
        var.ui.statusbar.addPermanentWidget(var.ui.lblStatus, 1)
        var.ui.lblStatus.setText("Bienvenido a 2º DAM")
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
        funciones de productos
        '''
        var.ui.btnGrabarProd.clicked.connect(products.Productos.altaProd)
        var.ui.tableProd.clicked.connect(products.Productos.cargarProd)
        var.ui.tableProd.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.btnLimpProd.clicked.connect(products.Productos.limpiarProd)
        var.ui.btnElimProd.clicked.connect(products.Productos.bajaProd)
        var.ui.btnModProd.clicked.connect(products.Productos.modifProd)
        var.ui.btnSalirProd.clicked.connect(events.Eventos.Salir)

        '''
        funciones de facturas
        '''
        var.ui.btnFechaFact.clicked.connect(facturas.Facturas.abrirCalendar)
        var.ui.btnReloadFact.clicked.connect(conexion.Conexion.mostrarFacturas)
        var.ui.btnFactura.clicked.connect(facturas.Facturas.altaFactura)
        var.ui.tabFacturas.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tabVentas.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tabFacturas.clicked.connect(facturas.Facturas.cargarFactura)
        var.ui.btnAnular.clicked.connect(facturas.Facturas.borrarFactura)
        var.ui.bntBuscarFact.clicked.connect(facturas.Facturas.buscarFactura)
        var.ui.btnCheckFact.clicked.connect(facturas.Facturas.altaVenta)
        var.ui.btnElimFact.clicked.connect(facturas.Facturas.anularVenta)


        '''
        módulos conexion base datos
        '''
        conexion.Conexion.db_connect(var.filebd)
        conexion.Conexion.mostrarClientes(self)
        conexion.Conexion.mostrarProductos(self)
        conexion.Conexion.mostrarFacturas(self)
        conexion.Conexion.cargarCmbventa(var.cmbVenta)

        '''
        módulos para informes
        '''
        var.ui.actionInformeClientes.triggered.connect(printer.Printer.reportCli)
        var.ui.actionInformeProductos.triggered.connect(printer.Printer.reportProductos)
        var.ui.actionFacturas.triggered.connect(printer.Printer.reportFact)
        var.ui.actionFacturasCliente.triggered.connect(printer.Printer.reportFacCli)

        '''
        módulos de supuestos prácticos
        '''
        var.ui.toolbarBackup.triggered.connect(events.Eventos.Backup)
        var.ui.actionBackup.triggered.connect(events.Eventos.Backup)
        var.ui.actionRestaurarBackup.triggered.connect(events.Eventos.cargarBackup)
        var.ui.actionImportarProd.triggered.connect(events.Eventos.cargarDesdeExcel)

    def closeEvent(self, event):
        if event:
            events.Eventos.Salir(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized() # PONER SHOWMAXIMIZED()
    window.setWindowIcon(QtGui.QIcon("img/logo.ico"))
    sys.exit(app.exec())