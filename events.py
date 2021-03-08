import sys, var, clients, products, conexion, zipfile, os, shutil, xlrd
from datetime import datetime
from PyQt5 import QtWidgets, QtSql


class Eventos():

    def About(event):
        '''
        Módulo para abrir la ventana de Acerca de
        :return: None

        '''

        var.dlgabout.show()

    def Salir(event):
        '''
        Módulo para cerrar el programa
        :return: None

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
        '''
        Módulo para abrir la ventana de diálogo que pide conformidad para salir del programa
        :return: None

        '''
        try:
            if var.dlgsalir.exec_():
                print(event)
                var.dlgsalir.hide()  # Necesario para que ignore X de la ventana
        except Exception as error:
            print('Error %s' % str(error))

    def cargarProv():
        """
        Módulo que carga los valores de las provincias en su combobox
        :return:None

        """
        try:
            prov = ['', 'A Coruña', 'Lugo', 'Ourense', 'Pontevedra', 'Vigo']
            for i in prov:
                var.ui.cmbProv.addItem(i)

        except Exception as error:
            print('Error: %s' % str(error))

    def Backup(self):
        '''
        Módulo que crea el backup en la localización deseada por el usuario
        :return: None

        '''
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
        '''
        Módulo que solicita un archivo backup al usuario y restaurará la base de datos según el archivo
        :return: None

        '''
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
        '''
        Módulo que abre la ventana de diálogo de Abrir
        :return: None

        '''
        try:
            var.filedlgabrir.show()

        except Exception as error:
            print("Error: %s" % str(error))

    def Imprimir(self):
        '''
        Módulo que abre la ventana de diálogo de Imprimir
        :return: None

        '''
        try:
            var.dlgimprimir.show()

        except Exception as error:
            print("Error: %s" % str(error))

    def Borrar(self):
        '''
        Módulo que abre la ventana de diálogo que pide conformidad para borrar a un cliente
        :return: None

        '''
        try:
            var.dlgborrar.show()
            if var.dlgborrar.exec_():
                clients.Clientes.bajaCliente
            else:
                var.dlgborrar.hide()

        except Exception as error:
            print("Error: %s" % str(error))

    def cargarDesdeExcel(self):
        '''
        Módulo que solicita un archivo excel y carga los datos de productos contenidos en él:
        los lee y crea productos o actualiza los existentes con esos datos
        :return: None

        '''
        try:
            option = QtWidgets.QFileDialog.Options()
            nombre = var.filedlgabrir.getOpenFileName(None, "Importar datos", "", "*.xls;;All Files", options=option)
            if var.filedlgabrir.Accepted and nombre != "":
                file = nombre[0]
            doc = xlrd.open_workbook(file)
            productos = doc.sheet_by_index(0)

            for i in range(0, productos.nrows):
                nombre = str(productos.cell_value(i, 0))
                precio = ("{0:.2f}").format(float(productos.cell_value(i, 1)))
                cantidad = int(productos.cell_value(i, 2))

                query = QtSql.QSqlQuery()
                query.prepare("select codigo, prezo, stock from articulos where nome = :nombre")
                query.bindValue(":nombre", nombre)

                existe = False
                if query.exec_():
                    while query.next():
                        query2 = QtSql.QSqlQuery()
                        query2.prepare("update articulos set prezo = :prezo, stock = :stock where nome = :nombre")
                        query2.bindValue(":prezo", precio)
                        query2.bindValue(":stock", cantidad)
                        query2.bindValue(":nombre", nombre)

                        if query2.exec_():
                            existe = True
                            print("Actualizado producto %s" % nombre)

                    if not existe:
                        query3 = QtSql.QSqlQuery()
                        query3.prepare("insert into articulos (nome, prezo, stock) values (:nome, :prezo, :stock)")
                        query3.bindValue(":nome", nombre)
                        query3.bindValue(":prezo", precio)
                        query3.bindValue(":stock", cantidad)

                        if query3.exec_():
                            print("Añadido producto %s" % nombre)

            conexion.Conexion.mostrarProductos(self)

        except Exception as error:
            print("Error al cargar el xml: %s" % str(error))