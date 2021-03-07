from PyQt5 import QtWidgets, QtSql
import var, facturas
from ventana import *

class Conexion():
    def db_connect(filename):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filename)
        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos','No se puede establecer conexion.\n'
                                            'Haz Click para Cancelar.', QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexión Establecida')
        return True

    def mostrarVentas(codigo):
        try:
            var.ui.tabVentas.clearContents()
            var.subfac = Conexion.precioFac(codigo)
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad from ventas where codfacventa = :codigo')
            query.bindValue(':codigo', int(codigo))
            if query.exec_():
                index = 0
                while query.next():
                    codventa = query.value(0)
                    codartic = query.value(1)
                    cantidad = query.value(2)
                    var.ui.tabVentas.setRowCount(index + 1)
                    var.ui.tabVentas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codventa)))
                    query1.prepare('select nome, prezo from articulos where codigo = :codartic')
                    query1.bindValue(':codartic', int(codartic))
                    if query1.exec_():
                        while query1.next():
                            articulo = query1.value(0)
                            print(codventa, articulo)
                            precio = query1.value(1)
                            var.ui.tabVentas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(articulo)))
                            var.ui.tabVentas.setItem(index, 2, QtWidgets.QTableWidgetItem(str(cantidad)))
                            subtotal = round(float(cantidad) * float(precio), 2)
                            var.ui.tabVentas.setItem(index, 3, QtWidgets.QTableWidgetItem("{0:.2f}".format(float(precio)) + ' €'))
                            var.ui.tabVentas.setItem(index, 4, QtWidgets.QTableWidgetItem("{0:.2f}".format(float(subtotal)) + ' €'))
                            var.ui.tabVentas.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                            var.ui.tabVentas.item(index, 2).setTextAlignment(QtCore.Qt.AlignCenter)
                            var.ui.tabVentas.item(index, 3).setTextAlignment(QtCore.Qt.AlignCenter)
                            var.ui.tabVentas.item(index, 4).setTextAlignment(QtCore.Qt.AlignCenter)

                            index += 1

                if int(index) > 0:
                    facturas.Facturas.prepararTablaventas(index)
                else:
                    var.ui.tabVentas.setRowCount(0)
                    facturas.Facturas.prepararTablaventas(0)

                #ES AQUI: HACER UN MODULO QUE CALCULE EL SUBTOTAL, IVA Y TOTAL DE CADA FACTURA Y LO CARGUE EN CADA CAMBIO EN VEZ DE CAMBIAR LOS DATOS EN EL ALTA DE FACTURA
                #Y EN CONEXION
                Conexion.calcularPrecios(var.subfac)
        except Exception as error:
            print("Error en la conexión de mostrar ventas: %s" % str(error))

    def precioFac(codigo):
        total = 0.00
        query = QtSql.QSqlQuery()
        query.prepare('select precio from ventas where codfacventa = :codigo')
        query.bindValue(':codigo', codigo)
        if query.exec_():
            while query.next():
                total += float(query.value(0))

        print("Total", total)
        return total


    def calcularPrecios(subtot):
        var.ui.lblSubtotal.setText("{0:.2f}".format((float(subtot))))
        iva = round(float(subtot) * 0.21, 2)
        var.ui.lblIVA.setText("{0:.2f}".format((float(iva))))
        total = round(float(subtot) + float(iva), 2)
        print(total)
        var.ui.lblTotal.setText("{0:.2f}".format((float(total))))



    def altaVenta(venta):
        query = QtSql.QSqlQuery()
        query.prepare('insert into ventas (codfacventa, codarticventa, cantidad, precio) VALUES (:codfacventa, :codarticventa, :cantidad, :precio)')
        query.bindValue(':codfacventa', int(venta[0]))
        query.bindValue(':codarticventa', int(venta[1]))
        query.bindValue(':cantidad', int(venta[3]))
        query.bindValue(':precio', float(venta[5]))
        fila = var.ui.tabVentas.currentRow()
        if query.exec_():
            var.ui.lblStatus.setText('Venta dade de alta satisfactoriamente')
            var.ui.tabVentas.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(venta[1])))
            var.ui.tabVentas.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(venta[2])))
            var.ui.tabVentas.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(venta[3])))
            var.ui.tabVentas.setItem(fila, 4, QtWidgets.QTableWidgetItem(str(venta[4])))
            var.ui.tabVentas.setItem(fila, 5, QtWidgets.QTableWidgetItem(str(venta[5])))
            fila += 1
            var.ui.tabVentas.insertRow(fila)
            var.ui.tabVentas.setCellWidget(fila, 1, var.cmbVenta)
            var.ui.tabVentas.scrollToBottom()
            Conexion.cargarCmbventa(var.cmbVenta)

    def anulaVenta(codigo):
        query = QtSql.QSqlQuery()
        query.prepare('delete from ventas where codventa = :codventa')
        query.bindValue(':codventa', codigo)
        if query.exec_():
            var.ui.lblStatus.setText("Venta anulada con éxito")
        else:
            print("Error al dar de baja la venta: ", query.lastError().text())

    def altaFact(dni, apel, fecha):
        query = QtSql.QSqlQuery()
        query.prepare('insert into facturas (dni, fecha, apellidos)'
                       'VALUES(:dni, :fecha, :apellidos)')
        query.bindValue(':dni', dni)
        query.bindValue(':fecha', fecha)
        query.bindValue(':apellidos', apel)
        if query.exec_():
            print("Factura dada de alta satisfactoriamente")
            Conexion.mostrarFacturas(None)

    def altaProd(producto):
        query = QtSql.QSqlQuery()
        query.prepare('insert into articulos (nome, prezo, stock)'
                      'VALUES(:nome, :prezo, :stock)')
        query.bindValue(':nome', str(producto[0]))
        query.bindValue(':prezo', str(producto[1]))
        query.bindValue(':stock', str(producto[2]))
        if query.exec_():
            print("Producto dado de alta satisfactoriamente")
            var.ui.lblStatus.setText("Producto " + str(producto[0]) + " dado de alta")

    def mostrarFacturas(self):
        while var.ui.tabFacturas.rowCount() > 0:
            var.ui.tabFacturas.removeRow(0)
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codfactura, fecha from facturas order by codfactura asc')
        if query.exec_():
            while query.next():
                cod = str(query.value(0))
                fecha = query.value(1)
                var.ui.tabFacturas.setRowCount(index + 1)
                var.ui.tabFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(cod))
                var.ui.tabFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(fecha))
                index += 1
            facturas.Facturas.limpiarFactura()
        else:
            print("Error mostrar facturas")

    def cargarVentasFactura(codigo):
        try:
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad, precio from ventas where codfacventa = :codigo')
            query.bindValue(':codigo', codigo)
            query2 = QtSql.QSqlQuery()
            query2.prepare('select nome, prezo from articulos where codigo = :codigo')
            if query.exec_():
                while query.next():
                    codventa = query.value(0)
                    artic = query.value(1)
                    cantidad = query.value(2)
                    precio = query.value(3)
                    query2.bindValue(':codigo', artic)
                    if query2.exec_():
                        while query2.next():
                            nome = query2.value(0)
                            unidad = query2.value(1)

                            var.ui.tabVentas.setRowCount(index + 1)
                            var.ui.tabVentas.setItem(index, 0, QtWidgets.QTableWidgetItem(codventa))
                            var.ui.tabVentas.setItem(index, 1, QtWidgets.QTableWidgetItem(nome))
                            var.ui.tabVentas.setItem(index, 2, QtWidgets.QTableWidgetItem(cantidad))
                            var.ui.tabVentas.setItem(index, 3, QtWidgets.QTableWidgetItem(unidad))
                            var.ui.tabVentas.setItem(index, 4, QtWidgets.QTableWidgetItem(precio))
                            index += 1

            facturas.Facturas.prepararTablaventas(index)
        except Exception as error:
            print("ERROR: %s" % str(error))


    def cargarFactura(codigo):
        query = QtSql.QSqlQuery()
        query.prepare('select dni, fecha, apellidos from facturas where codfactura = :codfactura')
        query.bindValue(':codfactura', codigo)
        if query.exec_():
            while(query.next()):
                var.ui.editDniFact.setText(str(query.value(0)))
                var.ui.editFechaFact.setText(str(query.value(1)))
                var.ui.editApelFact.setText(str(query.value(2)))

    def cargarFac2(self):
        query = QtSql.QSqlQuery()
        query.prepare('select codfactura, dni, fecha, apellidos from facturas order by codfactura desc limit 1')
        if query.exec_():
            while query.next():
                var.ui.lblCodFact.setText(str(query.value(0)))
                var.ui.editDni.setText(str(query.value(1)))
                var.ui.editFechaFact.setText(str(query.value(2)))
                var.ui.editApelFact.setText(str(query.value(3)))


    def bajaFactura(codfact):
        query = QtSql.QSqlQuery()
        query.prepare('delete from facturas where codfactura = :codfactura')
        query.bindValue(':codfactura', codfact)
        if query.exec_():
            print('Factura eliminada satisfactoriamente')

    def buscarFactura(dni):
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codfactura, fecha from facturas where dni = :dni order by codfactura desc')
        query.bindValue(':dni', str(dni))
        if query.exec_():
            while query.next():
                print("a")
                codfac = query.value(0)
                print(codfac)
                fecha = query.value(1)

                var.ui.tabFacturas.setRowCount(index + 1)

                var.ui.tabFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codfac)))
                var.ui.tabFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(fecha)))
                index += 1

    def cargarProducto():
        codigo = var.ui.lblCodProd.text()
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, nome, prezo, stock from articulos where codigo = :codigo')
        query.bindValue(':codigo', codigo)
        if query.exec_():
            while query.next():
                print(str(query.value(0)))
                var.ui.lblCodProd.setText(str(query.value(0)))
                var.ui.editNomeProd.setText(str(query.value(1)))
                var.ui.editPrezoProd.setText(str(query.value(2)))
                var.ui.editStockProd.setText(str(query.value(3)))

    def mostrarProductos(self):
        while var.ui.tableProd.rowCount() > 0:   # Fundamental para que no quede el valor mal borrado de la tabla
            var.ui.tableProd.removeRow(0)
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, nome, prezo, stock from articulos')
        if query.exec_():
            while query.next():
                codigo = str(query.value(0))
                nome = query.value(1)
                prezo = query.value(2)
                stock = query.value(3)
                var.ui.tableProd.setRowCount(index+1)
                var.ui.tableProd.setItem(index, 0, QtWidgets.QTableWidgetItem(codigo))
                var.ui.tableProd.setItem(index, 1, QtWidgets.QTableWidgetItem(nome))
                var.ui.tableProd.setItem(index, 2, QtWidgets.QTableWidgetItem(prezo))
                var.ui.tableProd.setItem(index, 3, QtWidgets.QTableWidgetItem(stock))
                index += 1
        else:
            print("Error mostrar clientes: ", query.lastError().text())

    def bajaProd(codigo):

        query = QtSql.QSqlQuery()
        query.prepare('delete from articulos where codigo = :codigo')
        query.bindValue(":codigo", codigo)
        if query.exec_():
            print("Baja producto")
            var.ui.lblStatus.setText("Producto con código " + str(codigo) + " dado de baja")
        else:
            print("Error al dar de baja el producto: ", query.lastError().text())

    def modifProd(codigo, newdata):
        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        query.prepare('update articulos set nome=:nome, prezo=:prezo, stock=:stock where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':nome', str(newdata[0]))
        query.bindValue(':prezo', str(newdata[1]))
        query.bindValue(':stock', str(newdata[2]))
        if query.exec_():
            print('Producto modificado')
            var.ui.lblStatus.setText('Producto con código ' + str(codigo) + ' modificado')
        else:
            print("Error modificar productos: ", query.lastError().text())

    def altaCli(cliente):
        query = QtSql.QSqlQuery()
        query.prepare('insert into clientes (dni, apellidos, nombre, fechalta, direccion, provincia, sexo, formapago, edad)'
                    'VALUES (:dni, :apellidos, :nombre, :fechalta, :direccion, :provincia, :sexo, :formapago, :edad)')
        query.bindValue(':dni', str(cliente[0]))
        query.bindValue(':apellidos', str(cliente[1]))
        query.bindValue(':nombre', str(cliente[2]))
        query.bindValue(':fechalta', str(cliente[3]))
        query.bindValue(':direccion', str(cliente[4]))
        query.bindValue(':provincia', str(cliente[5]))
        query.bindValue(':sexo', str(cliente[6]))
        query.bindValue(':formapago', str(cliente[7]))
        query.bindValue(':edad', int(cliente[8]))
        if query.exec_():
            print("Inserción Correcta")
            var.ui.lblStatus.setText("Alta cliente con DNI " + str(cliente[0]))
            Conexion.mostrarClientes(None)
        else:
            print("Error: ", query.lastError().text())

    def cargarCliente():
        dni = var.ui.editDni.text()
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.lblCodcli.setText(str(query.value(0)))
                var.ui.editDniFact.setText(str(query.value(1)))
                var.ui.editDni.setText(str(query.value(1)))
                var.ui.editApelFact.setText(str(query.value(2)))
                var.ui.editApel.setText(str(query.value(2)))
                var.ui.editNome.setText(str(query.value(3)))
                var.ui.editClialta.setText(str(query.value(4)))
                var.ui.editDir.setText(str(query.value(5)))
                var.ui.cmbProv.setCurrentText(str(query.value(6)))
                var.ui.spinEdad.setValue(int(query.value(9)))
                if str(query.value(7)) == 'Mujer':
                    var.ui.rbtFem.setChecked(True)
                    var.ui.rbtMasc.setChecked(False)
                else:
                    var.ui.rbtMasc.setChecked(True)
                    var.ui.rbtFem.setChecked(False)
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    var.chkpago[2].setChecked(True)

    def mostrarClientes(self):
        while var.ui.tableCli.rowCount() > 0:   # Fundamental para que no quede el valor mal borrado de la tabla
            var.ui.tableCli.removeRow(0)
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select dni, apellidos, nombre from clientes')
        if query.exec_():
            while query.next():
                dni = query.value(0)
                apellidos = query.value(1)
                nombre = query.value(2)
                var.ui.tableCli.setRowCount(index+1)
                var.ui.tableCli.setItem(index,0, QtWidgets.QTableWidgetItem(dni))
                var.ui.tableCli.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                var.ui.tableCli.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                index += 1
        else:
            print("Error mostrar clientes: ", query.lastError().text())


    def bajaCli(dni):
        '''
        módulo para eliminar cliente. Se llama desde fichero clientes.py
        :return:
        '''

        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(":dni", dni)
        if query.exec_():
            print("Baja cliente")

        else:
            print("Error al dar de baja el clientes: ", query.lastError().text())

    def modifCli(codigo, newdata):
        ''''
        modulo para modificar cliente. se llama desde fichero clientes.py
        :return None
        '''
        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        query.prepare('update clientes set dni=:dni, apellidos=:apellidos, nombre=:nombre, fechalta=:fechalta, '
                      'direccion=:direccion, provincia=:provincia, sexo=:sexo, formapago=:formapago, edad=:edad where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':dni', str(newdata[0]))
        query.bindValue(':apellidos', str(newdata[1]))
        query.bindValue(':nombre', str(newdata[2]))
        query.bindValue(':fechalta', str(newdata[3]))
        query.bindValue(':direccion', str(newdata[4]))
        query.bindValue(':provincia', str(newdata[5]))
        query.bindValue(':sexo', str(newdata[6]))
        query.bindValue(':formapago', str(newdata[7]))
        query.bindValue(':edad', str(newdata[8]))
        if query.exec_():
            print('Cliente modificado')
            var.ui.lblStatus.setText('Cliente con dni ' + str(newdata[0]) + ' modificado')
        else:
            print("Error modificar cliente: ", query.lastError().text())


    def buscaCli(dni):
        '''
        select un cliente a partir de su dni
        :return:
        '''
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.lblCodcli.setText(str(query.value(0)))
                var.ui.editApel.setText(str(query.value(2)))
                var.ui.editNome.setText(str(query.value(3)))
                var.ui.editClialta.setText(str(query.value(4)))
                var.ui.editDir.setText(str(query.value(5)))
                var.ui.cmbProv.setCurrentText(str(query.value(6)))
                var.ui.spinEdad.setValue(int(query.value(9)))
                if str(query.value(7)) == 'Mujer':
                    var.ui.rbtFem.setChecked(True)
                    var.ui.rbtMasc.setChecked(False)
                else:
                    var.ui.rbtMasc.setChecked(True)
                    var.ui.rbtFem.setChecked(False)
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    var.chkpago[2].setChecked(True)

    def cargarCmbventa(cmbVenta):
        var.cmbVenta.clear()
        query = QtSql.QSqlQuery()
        var.cmbVenta.addItem('')
        query.prepare('select codigo, nome from articulos order by nome')
        if query.exec_():
            while query.next():
                var.cmbVenta.addItem(str(query.value(1)))


    def obtenerCodPrec(articulo):
        cp = []
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, prezo from articulos where nome = :articulo')
        query.bindValue(':articulo', str(articulo))
        if query.exec_():
            while query.next():
                cp = [str(query.value(0)), str(query.value(1))]
        return cp
