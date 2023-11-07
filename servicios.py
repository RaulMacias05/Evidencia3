import sqlite3
from sqlite3 import Error
from rich import print
from rich.table import Table
import os
from time import sleep
import pandas as pd
import datetime


def comprobar_nombre():
    while True:
        nombre_del_servicio = input('\nNombre del servicio: ')
        if nombre_del_servicio.strip():
            break
        else:
            print('El nombre del servicio no debe quedar vacío. Intente de nuevo')

    return nombre_del_servicio

def comprobar_costo():
    while True:
        costo_servicio = float(input("Costo del servicio: "))
        if costo_servicio > 0.00:
            break
        else:
            print('El costo debe ser superior a 0.00. Intente de nuevo')
    return costo_servicio

def listado():

    os.system('cls')

    try:
            with sqlite3.connect("taller_mecanico_DB.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT * FROM servicios")
                registros = mi_cursor.fetchall()

                #Procedemos a evaluar si hay registros en la respuesta
                if registros:
                    print("Claves\tNombre")
                    print("*" * 30)
                    for clave, nombre, costo in registros:
                        print(f"{clave:^6}\t{nombre}")
                #Si no hay registros en la respuesta
                else:
                    print("No se encontraron registros en la respuesta")

    except sqlite3.Error as e:
            print(f'[red]{e}[/red]')
            input("Enter")

    except Exception as e:
            print(f'[red]{e}[/red]')
            input("Enter")

    finally:
            if conn:
                conn.close()


class Menu:
    def __init__(self) -> None:

        while True:

            self.mostrar_menu()
            
            match self.eleccion_del_menu:
                case 1:
                    self.agregar_servicio()
                case 2:
                    self.consultasyReportes()
                case 3:
                    break
    
    def mostrar_menu(self):

        os.system('cls')

        print(f'''
[#9999FF]CLIENTES[/#9999FF]

[#7AFFFF]--Menú Servicios--[/#7AFFFF]
              
1 - Agregar un Servicio
2 - Consultas y Reportes de Servicios
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


    def agregar_servicio(self):

        os.system('cls')

        nombre = comprobar_nombre()

        costo = comprobar_costo()

        try:
            with sqlite3.connect("taller_mecanico_DB.db") as conn:

                mi_cursor = conn.cursor()

                valores = {"nombre": nombre, "costo": costo}

                mi_cursor.execute("INSERT INTO servicios (nombre, costo) \
                                VALUES (:nombre, :costo)", valores)
                
                print()
                for i in range(3):
                    print("[green].[/green]", end = ' ')
                    sleep(.3)
                print("[green]Servicio agregado[/green]")

        except sqlite3.Error as e:
            print(f'[red]{e}[/red]')
            input("Enter")

        except Exception as e:
            print(f'[red]{e}[/red]')
            input("Enter")

        finally:
            if conn:
                conn.close()
                print("\n[#9999FF]Se ha cerrado la conexión[/#9999FF]")
                sleep(1)

    def consultasyReportes(self):
        while True:
            os.system('cls')

            print(f'''
[#9999FF]SERVICIOS[/#9999FF]

[#7AFFFF]--Menú Consultas--[/#7AFFFF]
            
1 - Búsqueda por clave de servicio
2 - Búsqueda por nombre de servicio
3 - Listado de servicios
4 - Volver al menú de servicios
            
''')
            while True:
                try:
                    self.eleccion_del_menu = int(input('Elija una opción (indicando su respectivo número): '))
                except ValueError:
                    print('Opción no válida. Intente de nuevo')
                else:
                    if self.eleccion_del_menu > 0 and self.eleccion_del_menu <= 4:
                        break
                    else:
                        print('Opción no válida. Intente de nuevo') 

            if self.eleccion_del_menu == 1:

                listado()

                valor_clave = int(input("\nIngrese la clave del servicio para conocer su detalle: "))

                os.system('cls')
                
                while True:
                    try:
                        with sqlite3.connect("taller_mecanico_DB.db") as conn:
                            mi_cursor = conn.cursor()
                            valores = {"clave":valor_clave}
                            mi_cursor.execute("SELECT * FROM servicios WHERE clave = :clave", valores)
                            registros = mi_cursor.fetchall()

                            #Procedemos a evaluar si hay registros en la respuesta
                            if registros:
                                print("Clave\tNombre\t\t\tCosto")
                                print("*" * 60)
                                for clave, nombre, costo in registros:
                                    print(f"{clave:^6}\t{nombre}\t\t\t{costo}")
                            #Si no hay registros en la respuesta
                            else:
                                print("No se encontraron registros en la respuesta")

                    except sqlite3.Error as e:
                        print(f'[red]{e}[/red]')
                        input("Enter")

                    except Exception as e:
                        print(f'[red]{e}[/red]')
                        input("Enter")

                    finally:
                        if conn:
                            conn.close()

                    salir = input("\nPresione ENTER para volver al menú ")
                    if salir == "":     
                        break

            elif self.eleccion_del_menu == 2:

                nombre_servicio = input("Ingrese el nombre del servicio a buscar: ")

                os.system('cls') 

                while True:
                    try:
                        with sqlite3.connect("taller_mecanico_DB.db") as conn:
                            mi_cursor = conn.cursor()
                            valor = {"nombre":nombre_servicio}
                            mi_cursor.execute("SELECT * FROM servicios WHERE UPPER(nombre) = UPPER(:nombre)", valor)
                            registro = mi_cursor.fetchall()

                            if registro:
                                print("Clave\tNombre\t\t\tCosto")
                                print("*" * 60)
                                for clave, nombre, costo in registro:
                                    print(f"{clave:^6}\t{nombre}\t\t\t{costo}")
                            #Si no hay registros en la respuesta
                            else:
                                print("No se encontraron registros en la respuesta")

                    except sqlite3.Error as e:
                        print(f'[red]{e}[/red]')
                        input("Enter")

                    except Exception as e:
                        print(f'[red]{e}[/red]')
                        input("Enter")

                    finally:
                        if conn:
                            conn.close()

                    salir = input("\nPresione ENTER para volver al menú ")
                    if salir == "":     
                        break
            
            elif self.eleccion_del_menu == 3:
                self.listado_de_servicios()

            elif self.eleccion_del_menu == 4:
                break

            else:
                print('Opción no válida. Intente de nuevo')   


    def listado_de_servicios(self):
        while True:
            os.system('cls')
            print('''
[#9999FF]CONSULTAS Y REPORTES DE Servicios[/#9999FF]
            
[#7AFFFF]--Menú Consultas de Servicios--[/#7AFFFF]

1 - Ordenados por clave
2 - Ordenados por nombre
3 - Regresar al menú anterior
            
''')
            tabla_servicios = Table(title='[#7AFFFF]--Servicios ordenados por su clave--[/#7AFFFF]')
            tabla_servicios.add_column("Clave", justify="left", style="#9999FF")
            tabla_servicios.add_column("Nombre", justify="left", style="#9999FF")
            tabla_servicios.add_column("Costo", justify="left", style="#9999FF")


            try:
                with sqlite3.connect("taller_mecanico_DB.db") as conn:
                    mi_cursor = conn.cursor()
                    tipo_consulta = input("Seleccione el tipo de orden del listado que desea: ")
                    if tipo_consulta == "1":
                        mi_cursor.execute("SELECT * FROM servicios ORDER BY clave")
                        registros = mi_cursor.fetchall()
                        listaservicios=[]
                        listaclaves=[]
                        if registros: 
                            for clave, nombre, costo in registros:
                                tabla_servicios.add_row(str(clave), nombre, str(costo))
                                listaclaves.append(clave)
                                listaservicios.append([nombre, costo])
                                os.system('cls')
                            print(tabla_servicios) 
                            print('''
[#9999FF]EXPORTACION DE RESULTADO[/#9999FF]
            
[#7AFFFF]--Menú Exportacion de Resultado--[/#7AFFFF]

1 - Exportar hacia CSV
2 - Exportar a EXCEL
3 - Regresar al menú de reportes
            
''')
                            while True:
                                tipo_exportacion = input('Seleccione el tipo de exportación deseada: ')
                                df_listaservicios = pd.DataFrame(listaservicios)
                                df_listaservicios.columns = ["Nombre", "Costo"]
                                df_listaservicios.index = listaclaves
                                Fecha_de_reporte =  datetime.date.today()
                                Fecha_de_reporte = datetime.date.today().strftime('%m-%d-%Y')

                                if tipo_exportacion == "1":
                                    df_listaservicios.to_csv(f"ReporteServiciosPorClave_{Fecha_de_reporte}.csv")
                                    break
                                elif tipo_exportacion == "2":
                                    df_listaservicios.to_excel(f"ReporteServiciosPorClave_{Fecha_de_reporte}.xlsx")
                                    break
                                elif tipo_exportacion == '3': 
                                    break
                                else: 
                                    print('Opcion no existente.')
                                    input('Presione Enter para continuar')
                            
                        else: 
                            print('No se encontraron registros')
                            input('Presione Enter para continuar')

                    elif tipo_consulta == "2":
                        mi_cursor.execute("SELECT * FROM servicios ORDER BY nombre")
                        registros = mi_cursor.fetchall()
                        listaservicios=[]
                        listaclaves=[]
                        if registros: 
                            for clave, nombre,costo in registros:
                                tabla_servicios.add_row(str(clave), nombre, str(costo))
                                listaclaves.append(clave)
                                listaservicios.append([nombre, costo])
                            os.system('cls')
                            print(tabla_servicios) 
                            print('''
[#9999FF]EXPORTACION DE RESULTADO[/#9999FF]
        
[#7AFFFF]--Menú Exportacion de Resultado--[/#7AFFFF]

1 - Exportar hacia CSV
2 - Exportar a EXCEL
3 - Regresar al menú de reportes
        
''')
                            while True:
                                tipo_exportacion = input('Seleccione el tipo de exportación deseada: ')
                                df_listaservicios =pd.DataFrame(listaservicios)
                                df_listaservicios.columns = ["Nombre", "Costo"]
                                df_listaservicios.index = listaclaves
                                Fecha_de_reporte =  datetime.date.today()
                                Fecha_de_reporte = datetime.date.today().strftime('%m-%d-%Y')

                                if tipo_exportacion == "1":
                                    df_listaservicios.to_csv(f"ReporteServiciosPorClave_{Fecha_de_reporte}.csv")
                                    break
                                elif tipo_exportacion == "2":
                                    df_listaservicios.to_excel(f"ReporteServiciosPorClave_{Fecha_de_reporte}.xlsx")
                                    break
                                elif tipo_exportacion == '3':
                                    break  
                                        
                                else: 
                                    print('Opcion no existente.')
                                    input('Presione Enter para continuar')

                        else: 
                            print('No se encontraron registros')
                            input('Presione Enter para continuar')

                    elif tipo_consulta == "3":
                        break
                            
                    else:
                        print('None es una opción válida.')
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