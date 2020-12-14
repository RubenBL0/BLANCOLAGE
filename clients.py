import var, conexion
from ventana import *

class Clientes():
    '''
    Eventos necesarios para el formulario clientes
    '''
    def validarDni(dni):
        '''
        Código que controla si el dni o nie es correcto
        :return:
        '''
        try:
            tabla = 'TRWAGMYFPDXBNJZSQVHLCKE'
            dig_ext = 'XYZ'
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = '0123456789'
            dni = dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control
        except Exception as error:
            print('Error en el algoritmo de validación del DNI: %s' % str(error))
            return None

    def validoDni():
        '''
        Muestra si el DNI es válido con un V verde, y si es
        incorrecto con una X roja, en la etiqueta lblValidar
        '''
        try:
            dni = var.ui.editDni.text()
            if Clientes.validarDni(dni):
                var.ui.lblValidar.setStyleSheet('QLabel {color: green;}')
                var.ui.lblValidar.setText('V')
                var.ui.editDni.setText(dni.upper())
                return True
            else:
                var.ui.lblValidar.setStyleSheet('QLabel {color: red;}')
                var.ui.lblValidar.setText('X')
                var.ui.editDni.setText(dni.upper())
                return False

        except Exception as error:
            print('Error al intentar validar el DNI: %s' % str(error))
            return None

    def selSexo():      # Carga el valor del sexo seleccionado
        try:
            if var.ui.rbtFem.isChecked():
                var.sex = 'Mujer'
            if var.ui.rbtMasc.isChecked():
                var.sex = 'Hombre'
        except Exception as error:
            print('Error al seleccionar el sexo: %s' % str(error))

    def selPago():      # Recoge y devuelve todos los datos marcados relacionados con el pago
        try:
            var.pay = []
            for i, data in enumerate(var.ui.grpbtnPay.buttons()):
                if data.isChecked() and i == 0:
                    var.pay.append('Efectivo')
                if data.isChecked() and i == 1:
                    var.pay.append('Tarjeta')
                if data.isChecked() and i == 2:
                    var.pay.append('Transferencia')
            print(var.pay)      # Lo imprime en consola para verificar que funciona correctamente
            return var.pay
        except Exception as error:
            print('Error: %s' % str(error))


    def selProv(prov):          # Guarda el valor seleccionado en la provincia en una variable global
        try:
            global vpro         # Definimos la variable global que contendrá la provincia
            vpro = prov
        except Exception as error:
            print('Error en la selección de provincia: %s' % str(error))


    def abrirCalendar():
        '''
        Abrir la ventana calendario
        '''
        try:
            var.dlgcalendar.show()      # Muestra la ventana del calendario
        except Exception as error:
            print('Error al mostrar el calendario: %s ' % str(error))

    def cargarFecha(qDate):
        ''''
        Este módulo se ejecuta cuando clicamos en un día del calendar, es decir, clicked.connect de calendar
        '''
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.editClialta.setText(str(data))       # Establecemos como texo la fecha seleccionada
            var.dlgcalendar.hide()                      # Ocultamos la ventana tras seleccionar la fecha deseada
        except Exception as error:
            print('Error al cargar la fecha: %s ' % str(error))

    def altaCliente():  # Se ejecuta cuando el usuario pulsa el botón Grabar
        '''
        Carga los datos que introduzcamos en la base de datos y en la tabla
        :return: none
        '''
        # Preparamos los datos
        try:
            newcli = []     # Todos los datos del cliente
            clitab = []     # Los 3 datos que se visualizarán en la tabla
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome, var.ui.editClialta, var.ui.editDir]
            k = 0
            for i in client:
                newcli.append(i.text())     # Así cargamos los editLine
                if k < 3:                   # Bucle que solo garga los 3 datos que visualizaremos en la tabla
                    clitab.append(i.text())
                    k += 1

            print(clitab)
            newcli.append(vpro)
            newcli.append(var.sex)
            var.pay2 = Clientes.selPago()
            newcli.append(var.pay2)
            newcli.append(var.ui.spinEdad.value())      # Así cargamos el spinner
            if client:  # Comprobar que no está vacío
                if(Clientes.validarDni(var.ui.editDni.text) == False):
                    print("No se puede añadir")
                else:
                    row = 0
                    column = 0
                    var.ui.tableCli.insertRow(row)
                    for registro in clitab:
                        cell = QtWidgets.QTableWidgetItem(registro)
                        var.ui.tableCli.setItem(row, column, cell)
                        column +=1
                    conexion.Conexion.altaCli(newcli)
                    print("añadido")
            else:
                print('Faltan Datos')
        except Exception as error:
            print('Error al dar de alta al cliente: %s ' % str(error))

    def limpiarCli():
        '''
        limpia los datos del formulario cliente
        :return: none
        '''
        try:
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome, var.ui.editClialta, var.ui.editDir]
            for i in range(len(client)):
                client[i].setText('')
            var.ui.grpbtnSex.setExclusive(False)  # Para que solo se pueda añadir un valor en los Radio Buttons
            for dato in var.rbtsex:
                dato.setChecked(False)
            for data in var.chkpago:
                data.setChecked(False)
            var.ui.cmbProv.setCurrentIndex(0)
            var.ui.lblValidar.setText('')
            var.ui.lblCodcli.setText('')
            var.ui.spinEdad.setValue(18)
            var.ui.lblStatus.setText("Bienvenido a 2º DAM")
        except Exception as error:
            print('Error limpiar widgets: %s ' % str(error))

    def cargarCli():
        '''
        carga en widgets formulario cliente los datos
        elegidos en la tabla
        :return: none
        '''
        try:
            fila = var.ui.tableCli.selectedItems()
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome]
            if fila:
                fila = [dato.text() for dato in fila]
            i = 0
            for i, dato in enumerate(client):
                dato.setText(fila[i])
            conexion.Conexion.cargarCliente()
        except Exception as error:
            print(':Error cargar clientes 1 %s ' % str(error))

    def bajaCliente(self):
        '''
        módulos para dar de baja un cliente
        :return:
        '''
        try:
            dni = var.ui.editDni.text()
            conexion.Conexion.bajaCli(dni)
            Clientes.limpiarCli()
            conexion.Conexion.mostrarClientes(None)
            var.ui.lblStatus.setText("Cliente con DNI " + dni + " dado de baja")

        except Exception as error:
            print("Error cargar clientes 2: %s " % str(error))

    def modifCliente(self):
        '''
        módulo para modificar datos de un cliente
        :return:
        '''
        try:
            newdata = []
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome, var.ui.editClialta, var.ui.editDir]
            for i in client:
                newdata.append(i.text())
            newdata.append(var.ui.cmbProv.currentText())
            newdata.append(var.sex)
            var.pay = Clientes.selPago()
            newdata.append(var.pay)
            newdata.append(var.ui.spinEdad.value())
            cod = var.ui.lblCodcli.text()
            conexion.Conexion.modifCli(cod, newdata)
            conexion.Conexion.mostrarClientes(self)

        except Exception as error:
            print("Error cargar clientes 3: %s" % str(error))


    def reloadCli(self):
        try:
            Clientes.limpiarCli()
        except Exception as error:
            print("Error recargar clientes: %s" % str(error))

    def buscarCli(self):
        '''
        Busca un Cliente a partir de un DNI que escribe el usuario
        :return: mensaje
        '''

        try:
            dni = var.ui.editDni.text()
            conexion.Conexion.buscaCli(dni)
        except Exception as error:
            print("Error recargar clientes: %s" % str(error))










