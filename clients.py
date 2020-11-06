import var
from PyQt5 import QtWidgets

class Clientes():
    #Clase gestión Clientes
    def validarDNI(dni):
        try:
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {"X": "0", "Y": "1", "Z": "2"}
            numeros = "1234567890"
            dni = dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control
            return False
        except Exception as error:
            print("Error en el módulo de validación del DNI. ", str(error))
            return None

    def validoDni():
        try:
            dni = var.ui.entDNI.text()
            if Clientes.validarDNI(dni):
                var.ui.lblValido.setStyleSheet("QLabel {color: green;}")
                var.ui.lblValido.setText("V")
                var.ui.entDNI.setText(dni.upper())
            else:
                var.ui.lblValido.setStyleSheet("QLabel {color: red;}")
                var.ui.lblValido.setText("X")
                var.ui.entDNI.setText(dni.upper())

        except Exception as error:
            print("Error: %s " % str(error))
            return None

    def selSexo(self):
        try:
            if var.ui.rbtFem.isChecked():
                var.sex = "femenino"
            if var.ui.rbtMasc.isChecked():
                var.sex = "masculino"
        except Exception as error:
            print("Error: %s" % str(error))

    def selPago(self):
        try:
            if var.ui.chkEfect.isChecked():
                var.pay.append("Efectivo")
            if var.ui.chkTarj.isChecked():
                var.pay.append("Tarjeta")
            if var.ui.chkTrans.isChecked():
                var.pay.append("Transferencia")
        except Exception as error:
            print("Error: %s " % str(error))

    def cargarProv():
        try:
            prov = ["","A Coruña","Lugo","Ourense","Pontevedra"]
            for i in prov:
                var.ui.cmbProv.addItem(i)
        except Exception as error:
            print("Error: %s " % str(error))

    def selProv(prov):
        try:
            global vpro
            vpro = prov
        except Exception as error:
            print("Error: %s" % str(error))

    def abrirCalendar(self):
        try:
            var.dlgcalendar.show()
        except Exception as error:
            print("Error: %s" % str(error))

    def cargarFecha(qDate):
        try:
            data = ("{0}/{1}/{2}".format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.editCliAlta.setText(str(data))
            var.dlgcalendar.hide()
        except Exception as error:
            print("Error: %s" % str(error))


    def showClientes(self):
        '''
        Cargará los clientes en la tabla
        :return: none
        '''
        # preparamos el registro
        try:
            newcli = []
            clitab = []  # será lo que carguemos en la tabla
            client = [var.ui.entDNI, var.ui.entApelidos, var.ui.entNome, var.ui.entDireccion, var.ui.editCliAlta]
            k = 0
            for i in client:
                newcli.append(i.text())  # cargamos los valores que hay en las editline
                if k < 3:
                    clitab.append(i.text())
                    k += 1
            newcli.append(vpro)
            # elimina duplicados
            var.pay = set(var.pay)

            for j in var.pay:
                newcli.append(j)
            newcli.append(var.sex)
            print(newcli)
            print(clitab)
            # aquí empieza como trabajar con la TableWidget
            row = 0
            column = 0
            var.ui.tablaCli.insertRow(row)
            for registro in clitab:
                cell = QtWidgets.QTableWidgetItem(registro)
                var.ui.tablaCli.setItem(row, column, cell)
                column += 1

        except Exception as error:
            print("Error: %s" % str(error))
