# Obtener datos
from get_into_data import grades
from get_into_data import groups
from get_into_data import forms

# Recordatorios
from get_into_data import reminders
from reminders import reminders as reminders_init

# Archivos
from files_data import files

# Despliegue de datos
from deployment_data import payroll
from deployment_data import pdf
from deployment_data import graphs
from deployment_data import stats

# Mapa conceptual
from conceptual_map import conceptual_map

# Calculadora
from calculator import calculator

# Historial
from historical import historical


def deployment_data_menu():
    menu_open = True
    while menu_open:
        print('1) Planillas')
        print('2) Exportar datos a PDF')
        print('3) Gráficos')
        print('4) Estadísticas')
        print('5) Retroceder')
        option = input('Seleccione una opción: ')
        if option == '1':
            payroll.payroll()
        elif option == '2':
            pdf.pdf()
        elif option == '3':
            graphs.graphs()
        elif option == '4':
            stats.stats()
        elif option == '5':
            menu_open = False
        else:
            print('Escoga una opción válida')


def data_menu():
    menu_open = True
    while menu_open:
        print('1) Notas')
        print('2) Encuestas')
        print('3) Grupos')
        print('4) Recordatorios')
        print('5) Retroceder')
        option = input('Seleccione una opción: ')
        if option == '1':
            grades.grades()
        elif option == '2':
            forms.forms()
        elif option == '3':
            groups.groups()
        elif option == '4':
            reminders.reminders()
        elif option == '5':
            menu_open = False


def main():
    menu_open = True
    while menu_open:
        print('1) Ingresar datos')
        print('2) Ver o exportar datos')
        print('3) Mapa conceptual')
        print('4) Calculadora')
        print('5) Historial datos agregados')
        print('6) Salir del programa')
        option = input('Ingrese una opción: ')
        if option == '1':
            data_menu()
        elif option == '2':
            deployment_data_menu()
        elif option == '3':
            conceptual_map.conceptual_map()
        elif option == '4':
            calculator.calculator()
        elif option == '5':
            historical.get_historical()
        elif option == '6':
            menu_open = False
        else:
            print('Escoga una opción válida')

if __name__ == '__main__':
    # Inicializar base de datos
    files.set_db()
    # Imprimir por consola los recordatorios
    reminders_init.print_reminders()
    # Menú principal
    main()
