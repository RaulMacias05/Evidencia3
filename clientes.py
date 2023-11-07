import sqlite3
from rich.table import Table
from rich import print
import datetime
from email_validator import validate_email, EmailNotValidError
import os
from time import sleep
import pandas as pd

def comprobar_correo():
    while True:
        correo = input('\nCorreo electrónico del cliente: ')
        try:
            v = validate_email(correo)
            return correo
        
        except EmailNotValidError as e:
            print(f'Ocurrió un problema: {e}')
        
        except Exception as e:
            print(f'Ocurrió un problema: {e}')


def comprobar_RFC():
    RFC = input('\nRFC del Cliente: ')
    
    if len(RFC) == 12:
        if not RFC[:3].isalpha():
            print(f'Los primeros 3 caracteres del RFC deben ser letras para personas morales')
            return False
        else:
            digitos_fecha = [RFC[digito:digito+2] for digito in range(3,9,2)]
        
        

    elif len(RFC) == 13:
        if not (RFC[:4].isalpha() and RFC[1].upper() in ('AEIOU')):
            print(f'Los primeros 4 caracteres del RFC deben ser letras y el segundo una vocal para personas físicas')
            return False
        else:
            digitos_fecha = [RFC[digito:digito+2] for digito in range(4,10,2)]
        
    else:
        print('La longitud del RFC debe ser de 13 caracteres para personas físicas o 12 para personas morales')
        return False
    
    fecha = '/'.join(digitos_fecha)

    try:
        fecha_correcta = datetime.datetime.strptime(fecha,"%y/%m/%d").date()
        return RFC
    
    except ValueError:
        print('Fecha en RFC no válida')
        return False

    except Exception as exc:
        print(f'Ocurrió un error: {exc}')
        return False
    
    
def comprobar_nombre():
    while True:
        nombre_del_cliente = input('\nNombre del cliente: ')
        if nombre_del_cliente.strip():
            break
        else:
            print('El nombre del cliente no debe quedar vacío. Intente de nuevo')

    return nombre_del_cliente



class Menu:
    def __init__(self) -> None:
        while True:

            self.mostrar_menu()
            
            match self.eleccion_del_menu:
                case 1:
                    self.agregarCliente()
                case 2:
                    self.consultasyReportes()
                case 3:
                    break
    
    def mostrar_menu(self):

        os.system('cls')

        print(f'''
[#9999FF]CLIENTES[/#9999FF]

[#7AFFFF]--Menú clientes--[/#7AFFFF]
              
1 - Agregar un cliente
2 - Consultas y Reportes
3 - Volver al Menú Principal
              
''')
        while True:
            try:
                self.eleccion_del_menu = int(input('Elija una opción (indicando su respectivo número): '))
            except ValueError:
                print('Opción no válida. Intente de nuevo')
            else:
                if self.eleccion_del_menu > 0 and self.eleccion_del_menu <= 3:
                    break
                else:
                    print('Opción no válida. Intente de nuevo')

    def agregarCliente(self):
        
        os.system('cls')

        nombre = comprobar_nombre()
        while True:
            rfc = comprobar_RFC()
            if rfc:
                break

        correo = comprobar_correo()

        try:
            with sqlite3.connect("taller_mecanico_DB.db") as conn:
                mi_cursor = conn.cursor()

                valores = {"nombre": nombre, "rfc": rfc, "correo": correo}

                mi_cursor.execute("INSERT INTO clientes (nombre, rfc, correo) \
                                  VALUES (:nombre, :rfc, :correo)", valores)
                
                print()
                for i in range(3):
                    print("[green].[/green]", end = ' ')
                    sleep(.3)
                print("[green]Cliente agregado[/green]")

        except sqlite3.Error as e:
            print(f'[red]{e}[/red]')
            input("Enter")

        except Exception as e:
            print(f'[red]{e}[/red]')
            input("Enter")

        finally:
            if conn:
                conn.close()

    def consultasyReportes(self):

        while True:
            os.system('cls')
            print('''
[#9999FF]CONSULTAS Y REPORTES DE CLIENTES[/#9999FF]
            
[#7AFFFF]--Menú Consultas de Clientes--[/#7AFFFF]

1 - Ordenados por clave
2 - Ordenados por nombre
3 - Regresar al menú anterior

''')
            t_clientes = Table(title='[#7AFFFF]--Clientes ordenados por su clave--[/#7AFFFF]')
            t_clientes.add_column("Clave", justify="left", style="#9999FF")
            t_clientes.add_column("Nombre", justify="left", style="#9999FF")
            t_clientes.add_column("RFC", justify="left", style="#9999FF")
            t_clientes.add_column("Correo", justify="left", style="#9999FF")

            try: 
                with sqlite3.connect("taller_mecanico_DB.db") as conn:
                    mi_cursor = conn.cursor()
                    
                    seleccion_consulta = input("Seleccione el tipo de orden del listado que desea: ")
                    
                    if seleccion_consulta == '1':
                        mi_cursor.execute("SELECT * FROM clientes ORDER BY clave")
                        registros = mi_cursor.fetchall()
                        listaclientes = []
                        listaclaves = []

                        if registros:
                            for clave, nombre, rfc, correo in registros: 
                                t_clientes.add_row(str(clave), nombre, rfc, correo)
                                listaclaves.append(clave)
                                listaclientes.append([nombre, rfc, correo])
                            os.system('cls')
                            print(t_clientes)
                            
                            self.menu_exportacion('Clave', listaclientes, listaclaves)

                        else: 
                            print('No se encontraron registros') 
                            input('Presione Enter para continuar')

                    elif seleccion_consulta == '2': 

                        mi_cursor.execute("SELECT * FROM clientes ORDER BY nombre")
                        registros = mi_cursor.fetchall()
                        listaclientes = []
                        listaclaves = []

                        if registros: 

                            for clave, nombre, rfc, correo in registros: 
                                t_clientes.add_row(str(clave), nombre, rfc, correo)
                                listaclaves.append(clave)
                                listaclientes.append([nombre, rfc, correo])
                            os.system('cls')
                            print(t_clientes)
                            
                            self.menu_exportacion('Nombre', listaclientes, listaclaves)
                        else: 
                            print('No se encontraron registros') 
                            input('Presione Enter para continuar')

                    elif seleccion_consulta == '3':
                        break
                    
                    else: 
                        print('No es una opción válida.')
                        input('Presione Enter para continuar')


            except sqlite3.Error as e:
                print(e)
                input('Presione Enter para continuar')

            except Exception as e: 
                print(f'Se produjo el siguiente error: {e}') 
                input('Presione Enter para continuar')

            finally: 
                if conn:
                    conn.close()

    def menu_exportacion(self, orden, listaclientes, listaclaves):
        print('''
[#9999FF]EXPORTACION DE RESULTADO[/#9999FF]
            
[#7AFFFF]--Menú Exportacion de Resultado--[/#7AFFFF]

1 - Exportar hacia CSV
2 - Exportar a EXCEL
3 - Regresar al menú de reportes

''')        
        seleccion_exportacion = input('Seleccione el tipo de exportación deseada: ')

        Fecha_de_reporte =  datetime.date.today()
        Fecha_de_reporte = datetime.date.today().strftime('%m-%d-%Y')
        
        df_listaclientes = pd.DataFrame(listaclientes)
        df_listaclientes.columns = ["Nombre", "RFC", "Correo"]
        df_listaclientes.index = listaclaves

        if seleccion_exportacion == '1':
            df_listaclientes.to_csv(f'ReporteClientesActivosPor{orden}_{Fecha_de_reporte}.csv')

        elif seleccion_exportacion == '2': 
            df_listaclientes.to_excel((f'ReporteClientesActivosPor{orden}_{Fecha_de_reporte}.xlsx'))

        elif seleccion_exportacion == '3': 
            return
        else:
            print('No es una opción válida.')
            input('Presione Enter para continuar') 