import var, sys

class Eventos():

    #Eventos Generales

    def Salir(self):
        try:
            sys.exit()
        except Exception as error:
            print("Error %s " % str(error))