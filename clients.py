import var

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

    def cargarProv():
        try:
            prov = ["","A Coruña","Lugo","Ourense","Pontevedra"]
            for i in prov:
                var.ui.cmbProv.addItem(i)
        except Exception as error:
            print("Error: %s " % str(error))


    def selProv(prov):
        try:
            print("Has seleccionado la provincia de ", prov)
            return prov
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