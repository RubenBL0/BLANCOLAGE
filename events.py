import sys, var, clients, products, conexion, zipfile, os, shutil, xlrd
from datetime import datetime
from PyQt5 import QtWidgets, QtSql


class Eventos():

    def About(event):
        var.dlgabout.show()

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
            fechahoy = datetime.today().strftime("%Y.%m.%d.%H.%M.%S")
            backup = ("backup_" + fechahoy + ".zip")
            option = QtWidgets.QFileDialog.Options()
            directorio, file = var.filedlgabrir.getSaveFileName(None, "Guardar backup", backup, ".zip", options=option)
            if var.filedlgabrir.Accepted and file != "":
                zip = zipfile.ZipFile(backup, "w")
                zip.write(var.filebd, os.path.basename(var.filebd), zipfile.ZIP_DEFLATED)
                zip.close()
                var.ui.lblStatus("Backup realizado con éxito")
                shutil.move(str(backup), str(directorio))
        except Exception as error:
            print("Error al crear el backup: %s" % str(error))

    def cargarBackup(self):

        try:
            option = QtWidgets.QFileDialog.Options()
            nombre = var.filedlgabrir.getOpenFileName(None, "Restaurar backup", "", "*.zip;;All Files", options=option)
            if var.filedlgabrir.Accepted and nombre != "":
                file = nombre[0]
                with zipfile.ZipFile(str(file), "r") as backup:
                    backup.extractall(pwd=None)
                backup.close()
            conexion.Conexion.db_connect(var.filebd)
            conexion.Conexion.mostrarClientes(self)
            conexion.Conexion.mostrarProductos(self)
            conexion.Conexion.mostrarFacturas(self)
            var.ui.lblStatus.setText("Backup restaurado exitosamente")
        except Exception as error:
            print("Error al restaura el backup: %s" % str(error))

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

    def cargarDesdeExcel(self):
        try:
            doc = xlrd.open_workbook("MercaEstadisticas.xls")
            productos = doc.sheet_by_index(0)

            for i in range(0, productos.nrows):
                nombre = str(productos.cell_value(i, 0))
                precio = str(productos.cell_value(i, 1))
                cantidad = str(productos.cell(i, 2))

                query = QtSql.QSqlQuery()
                query.prepare("select codigo, prezo, stock from articulos where nome = :nombre")
                query.bindValue(":nombre", nombre)

                existe = False
                if query.exec_():
                    while query.next():
                        query2 = QtSql.QSqlQuery()
                        query2.prepare("update articulos set prezo = :prezo, stock = :stock where nome = :nombre")
                        query2.bindValue(":prezo", float(precio))
                        query2.bindValue(":stock", int(cantidad))
                        query2.bindValue(":nombre", nombre)

                        if query2.exec_():
                            existe = True
                            print("Actualizado producto %s" % nombre)

                    if not existe:
                        query3 = QtSql.QSqlQuery()
                        query3.prepare("insert into articulos (nome, prezo, stock) values (:nome, :prezo, :stock)")
                        query3.bindValue(":nome", nombre)
                        query3.bindValue(":prezo", float(precio))
                        query3.bindValue(":stock", int(cantidad))

                        if query3.exec_():
                            print("Añadido producto %s" % nombre)
        except Exception as error:
            print("Error al cargar el xml: %s" % str(error))