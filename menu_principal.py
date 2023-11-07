import os
from rich import print
import time
import notas
import clientes
import servicios

class Menu_principal:
    def __init__(self) -> None:

        while True:
            self.mostrar_menu()

            match self.eleccion_del_menu:
                case 1:
                    self.notas()
                case 2:
                    self.clientes()
                case 3:
                    self.servicios()
                case 4:
                    if self.salir_del_sistema():
                        break

    def mostrar_menu(self):

        os.system('cls')

        print(f'''
[#9999FF]REGISTRO Y MANIPULACIÓN DE NOTAS[/#9999FF]

[#7AFFFF]--Menú Principal--[/#7AFFFF]
              
1 - Notas
2 - Clientes
3 - Servicios
4 - Salir del Sistema
              
''')

        while True:
            try:
                self.eleccion_del_menu = int(input('Elija una opción (indicando su respectivo número): '))
            except ValueError:
                print('Opción no válida. Intente de nuevo')
            else:
                if self.eleccion_del_menu > 0 and self.eleccion_del_menu <= 5:
                    break
                else:
                    print('Opción no válida. Intente de nuevo')

    def notas(self):
        notas.Menu()

    def clientes(self):
        clientes.Menu()

    def servicios(self):
        servicios.Menu()


    def salir_del_sistema(self):
        while True:
            salir = input("¿Desea salir definitivamente del programa?\n| s - Sí | n - No |\n")

            if salir.upper() in ('S', 'SI', 'SÍ'):
                print("\nGracias por su visita, vuelva pronto")
                return True
            
            elif salir.upper() in ('N', 'NO'):
                print("\nVolviendo al Menú Principal")
                for i in range(3):
                    print('.', end=' ')
                    time.sleep(.3)
                time.sleep(.3)
                return False
                
            else:
                print('Opción no válida. Intente de nuevo\n')

Menu_principal() 