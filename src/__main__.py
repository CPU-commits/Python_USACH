from get_into_data import grades
from get_into_data import groups
from get_into_data import forms
from get_into_data import reminders
from files_data import files
from reminders import reminders as reminders_init
from deployment_data import payroll
from historical import historical

def deployment_data_menu():
    menu_open = True
    while menu_open:
        print('1) Planillas')
        print('2) Exportar')
        print('3) Retroceder')
        option = input('Seleccione una opción: ')
        if option == '1':
            payroll.payroll()
        elif option == '2':
            pass
        elif option == '3':
            menu_open = False

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
        print('3) Eliminar datos')
        print('4) Historial datos agregados')
        print('5) Salir del programa')
        option = input('Ingrese una opción: ')
        if option == '1':
            data_menu()
        elif option == '2':
            deployment_data_menu()
        elif option == '3':
            pass
        elif option == '4':
            historical.get_historical()
        elif option == '5':
            menu_open = False
        else:
            print('Escoga una opción válida')

if __name__ == '__main__':
    files.set_db()
    reminders_init.print_reminders()
    main()