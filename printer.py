from reportlab.pdfgen import canvas
import os, var
from datetime import *
from PyQt5 import QtSql

class Printer():

    def cabecera(self):
        logo = '.\\img\logo.png'
        var.rep.setTitle("INFORMES")
        var.rep.setAuthor("Rubén Blanco Lage")
        var.rep.setFont("Helvetica", size = 10)
        var.rep.line(45, 820, 525, 820)
        var.rep.line(45, 745, 525, 745)
        textcif = "A0000000H"
        textnom = "SUPERMERCADO RUBÉN BLANCO, S.L."
        textdir = "Avenida Galicia, 101 - Vigo"
        texttlfo = "886 12 04 64"
        var.rep.drawString(50, 805, textcif)
        var.rep.drawString(50, 790, textnom)
        var.rep.drawString(50, 775, textdir)
        var.rep.drawString(50, 760, texttlfo)
        var.rep.drawImage(logo, 450, 752)

    def pie(textlistado):
        try:
            var.rep.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d.%m.%Y   %H:%M:%S')
            var.rep.setFont("Helvetica-Oblique", size = 7)
            var.rep.drawString(460, 40, str(fecha))
            var.rep.drawString(275, 40, str("Página %s" % var.rep.getPageNumber()))
            var.rep.drawString(50, 40, str(textlistado))
        except Exception as error:
            print("Error en el pie de informe: %s" % str(error))

    def reportCli(self):
        try:
            textlistado = "LISTADO DE CLIENTES"
            var.rep = canvas.Canvas('informes/listadoclientes.pdf')
            Printer.cabecera(self)
            Printer.cabeceraCli(self)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, dni, apellidos, nombre, fechalta from clientes order by apellidos, nombre')
            if query.exec_():
                i = 50
                j = 690
            Printer.pie(textlistado)
            while query.next():
                if j <= 80:
                    var.rep.showPage()
                    Printer.cabecera(self)
                    Printer.pie(textlistado)
                    Printer.cabeceraCli(self)
                    i = 50
                    j = 690
                var.rep.setFont('Helvetica', size=10)
                var.rep.drawString(i, j, str(query.value(0)))
                var.rep.drawString(i + 30, j, str(query.value(1)))
                var.rep.drawString(i + 130, j, str(query.value(2)))
                var.rep.drawString(i + 280, j, str(query.value(3)))
                var.rep.drawRightString(i + 470, j, str(query.value(4)))
                j = j - 25

            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('listadoclientes.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1

        except Exception as error:
            print("Error reportcli %s" % str(error))


    #Cabecera única para el listado de clientes
    def cabeceraCli(self):
        try:
            var.rep.setFont("Helvetica-Bold", size=9)
            textlistado = "LISTADO DE CLIENTES"
            var.rep.drawString(255, 735, textlistado)
            var.rep.line(45, 730, 525, 730)
            itemCli = ["Cod", "DNI", "APELLIDOS", "NOMBRE", "FECHA ALTA"]
            var.rep.drawString(45, 710, itemCli[0])
            var.rep.drawString(90, 710, itemCli[1])
            var.rep.drawString(180, 710, itemCli[2])
            var.rep.drawString(325, 710, itemCli[3])
            var.rep.drawString(465, 710, itemCli[4])
            var.rep.line(45, 703, 525, 703)
        except Exception as error:
            print("Error en la cabecera de clientes: " % str(error))

    def reportProductos(self):
        try:
            textlistado = "LISTADO DE PRODUCTOS"
            var.rep = canvas.Canvas('informes/listadoproductos.pdf')
            Printer.cabecera(self)
            Printer.cabeceraProd(self)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nome, prezo, stock from articulos order by codigo')
            if query.exec_():
                i = 50
                j = 690
            Printer.pie(textlistado)
            while query.next():
                if j <= 80:
                    var.rep.showPage()
                    Printer.cabecera(self)
                    Printer.pie(textlistado)
                    Printer.cabeceraCli(self)
                    i = 50
                    j = 690
                var.rep.setFont('Helvetica', size=10)
                var.rep.drawString(i, j, str(query.value(0)))
                var.rep.drawString(i + 125, j, str(query.value(1)))
                var.rep.drawRightString(i + 315, j, str(query.value(2)))
                var.rep.drawRightString(i + 450, j, str(query.value(3)))
                j = j - 25

            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('listadoproductos.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1

        except Exception as error:
            print("Error reportprod %s" % str(error))

    # Cabecera única para el listado de productos
    def cabeceraProd(self):
        try:
            var.rep.setFont("Helvetica-Bold", size=9)
            textlistado = "LISTADO DE PRODUCTOS"
            var.rep.drawString(255, 735, textlistado)
            var.rep.line(45, 730, 525, 730)
            itemCli = ["Código", "NOMBRE", "PRECIO", "STOCK"]
            var.rep.drawString(45, 710, itemCli[0])
            var.rep.drawString(175, 710, itemCli[1])
            var.rep.drawString(330, 710, itemCli[2])
            var.rep.drawString(470, 710, itemCli[3])
            var.rep.line(45, 703, 525, 703)
        except Exception as error:
            print("Error en la cabecera de productos: " % str(error))


    def reportFact(self):
        try:
            textlistado = "FACTURA"
            var.rep = canvas.Canvas("informes/factura.pdf")
            Printer.cabecera(self)
            Printer.pie(textlistado)
            codfac = var.ui.lblCodFact.text()
            Printer.cabeceraFact(codfac)
            query = QtSql.QSqlQuery()
            query.prepare("select codventa, codarticventa, cantidad, precio from ventas where codfacventa = :cod")
            query.bindValue(":cod", int(codfac))
            if query.exec_():
                i = 55
                j = 600
                while query.next():
                    if j <= 100:
                        var.rep.drawString(440, 110, "Página siguiente...")
                        var.rep.showPage()
                        Printer.cabecera(self)
                        Printer.pie(textlistado)
                        Printer.cabeceraFact(self)
                        i = 50
                        j = 600
                    var.rep.setFont("Helvetica", size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    query2 = QtSql.QSqlQuery()
                    query2.prepare("select nome, prezo from articulos where codigo = :codigo")
                    query2.bindValue(":codigo", str(query.value(1)))
                    if query2.exec_():
                        while query2.next():
                            articulo = query2.value(0)
                            precio = query2.value(1)
                    var.rep.drawString(i + 85, j, str(articulo))
                    var.rep.drawRightString(i + 260, j, str(query.value(2)))
                    var.rep.drawRightString(i + 375, j, "{0:.2f}".format(float(precio)))
                    subt = round(float(query.value(2)) * float(precio), 2)
                    var.rep.drawRightString(i + 460, j, "{0:.2f}".format(float(subt)) + " €")
                    j -= 20

            var.rep.save()
            path = ".\\informes"
            cont = 0
            for file in os.listdir(path):
                if file.endswith("factura.pdf"):
                    os.startfile("%s/%s" % (path, file))
                cont += 1

        except Exception as error:
            print("Error en el informe de factura: %s" % str(error))




    def cabeceraFact(codfac):
        try:
            var.rep.setFont("Helvetica-Bold", size=9)
            var.rep.drawString(55, 725, "Cliente: ")
            var.rep.drawString(50, 650, "Factura nº: %s" % str(codfac))
            var.rep.line(45, 665, 525, 665)
            var.rep.line(45, 640, 525, 640)

            query = QtSql.QSqlQuery()
            query.prepare("select dni, fecha from facturas where codfactura = :codfac")
            query.bindValue(":codfac", int(codfac))
            if query.exec_():
                while query.next():
                    dni = str(query.value(0))
                    var.rep.drawString(55, 710, "DNI: %s" % dni)
                    var.rep.drawString(420, 650, "Fecha: %s" % str(query.value(1)))

            query2 = QtSql.QSqlQuery()
            query2.prepare("select apellidos, nombre, direccion, provincia, formapago from clientes where dni = :dni")
            query2.bindValue(":dni", dni)
            if query2.exec_():
                while query2.next():
                    var.rep.drawString(55, 695, str(query2.value(0)) + ", " + str(query2.value(1)))
                    var.rep.drawString(300, 695, "Formas de pago: ")
                    var.rep.drawString(55, 680, str(query2.value(2)) + " - " + str(query2.value(3)))
                    var.rep.drawString(300, 680, str(query2.value(4).strip("[]").replace("'", "").replace(","," -")))
                var.rep.line(45, 625, 525, 625)
                datos = ["Código de venta", "Artículo", "Cantidad", "Precio/Unidad(€)", "Subtotal(€)"]
                var.rep.drawString(50, 630, datos[0])
                var.rep.drawString(140, 630, datos[1])
                var.rep.drawString(275, 630, datos[2])
                var.rep.drawString(360, 630, datos[3])
                var.rep.drawString(470, 630, datos[4])
                var.rep.drawRightString(500, 160, "Subtotal:    " + "{0:.2f}".format(float(var.ui.lblSubtotal.text())) + " €")
                var.rep.drawRightString(500, 140, "IVA:     " + "{0:.2f}".format(float(var.ui.lblIVA.text())) + " €")
                var.rep.drawRightString(500, 115, "Total:   " + "{0:.2f}".format(float(var.ui.lblTotal.text())) + " €")
        except Exception as error:
            print("Error en la cabecera de factura: %s" % str(error))

    def reportFacCli(self):
        try:
            dni = var.ui.editDniFact.text()
            textlistado = "FACTURAS DEL CLIENTE"
            var.rep = canvas.Canvas("informes/facturascliente.pdf")
            Printer.cabecera(self)
            Printer.pie(textlistado)
            query = QtSql.QSqlQuery()
            query.prepare("select nombre, apellidos from clientes where dni = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec_():
                while query.next():
                    nombre = str(query.value(0))
                    apell = str(query.value(1))
                    var.rep.drawString(230, 720, textlistado)
                    var.rep.line(45, 710, 525, 710)
                    var.rep.drawString(45, 730, "Cliente: %s" % (str(nombre) + " " + str(apell)) + "  DNI: %s" % str(dni))
                    datos = ["Nº Factura", "Fecha", "Total (€)"]
                    var.rep.line(45, 680, 525, 680)
                    var.rep.drawString(45, 690, datos[0])
                    var.rep.drawString(245, 690, datos[1])
                    var.rep.drawString(470, 690, datos[2])
                    query2 = QtSql.QSqlQuery()
                    query2.prepare("select codfactura, fecha from facturas where dni = :dni")
                    query2.bindValue(":dni", dni)
                    i = 55
                    j = 650
                    total = 0.00
                    if query2.exec_():
                        while query2.next():
                            if j <= 100:
                                var.rep.showPage()
                                Printer.cabecera(self)
                                Printer.pie(textlistado)
                                i = 55
                                j = 650
                            var.rep.setFont("Helvetica", size=10)
                            var.rep.drawString(i, j, str(query2.value(0)))
                            var.rep.drawRightString(i + 240, j, str(query2.value(1)))

                            query3 = QtSql.QSqlQuery()
                            query3.prepare("select precio from ventas where codfacventa = :codfacventa")
                            query3.bindValue(":codfacventa", int(query2.value(0)))
                            subtotal = 0.00
                            if query3.exec_():
                                while query3.next():
                                    subtotal += float(query3.value(0))
                                var.rep.drawRightString(i + 440, j, "{0:.2f}".format(float(subtotal)) + " €")
                                total += subtotal

                            j -= 20

                    var.rep.drawRightString(i + 430, 140, "IVA: " + "{0:.2f}".format(float(total) * 0.21) + " €")
                    var.rep.drawRightString(i + 430, 120, "Total: " + "{0:.2f}".format(float(total) * 1.21) + " €")

            var.rep.save()
            path = ".\\informes"
            for file in os.listdir(path):
                if file.endswith("facturascliente.pdf"):
                    os.startfile("%s/%s" % (path, file))
        except Exception as error:
            print("Error en el informe de facturas del cliente: %s" % str(error))