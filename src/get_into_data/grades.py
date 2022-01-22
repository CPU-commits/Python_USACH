import pandas as pd
import json


from get_into_data import groups
from historical import historical
from files_data import files


def __open_grades(mode):
    return open('src/db/grades.json', mode)


def get_data():
    file = __open_grades('r')
    data = json.load(file)
    file.close()
    return data


def __get_data_groups():
    return groups.get_data()


def __select_student(students_data):
    menu_open = True
    while menu_open:
        selected_student = input('Seleccione un estudiante (Posición): ')
        if 0 <= int(selected_student) < len(students_data):
            menu_open = False
        else:
            print('Seleccione un estudiante válido')
    return int(selected_student)


def __validate_keys_existence(key_group, key_student, grades_data):
    # Validar llaves
    if key_group in grades_data:
        if key_student not in grades_data[key_group]['students_grades']:
            grades_data[key_group]['students_grades'][key_student] = []
    else:
        grades_data[key_group] = {
            "students_grades": {
                key_student: []
            }
        }
    return grades_data


def validate_grade(grade):
    valid = True
    if len(grade) != 3:
        return False
    i = 0
    for c in grade:
        if i == 0 or i == 2:
            if c not in "0123456789":
                valid = False
        elif i == 1:
            if c != ".":
                valid = False
        i += 1
    return valid


def __select_grade():
    # Seleccionar nota
    menu_open = True
    while menu_open:
        grade = input('Calificación/nota (En formato "Entero.Decimas"): ')
        if validate_grade(grade):
            menu_open = False
        else:
            print('Ingrese una calificación/nota válida')
    return float(grade)


def __enter_students_grades(groups_data, grades_data):
    # Función para ver estudiantes
    students_data, sg = groups.get_students(groups_data)
    if len(students_data) > 0:
        grades_file = __open_grades('w')
        print(f"Estudiantes:\n {pd.DataFrame(students_data)}\n")
        selected_student = __select_student(students_data)
        grade = __select_grade()
        key_group = groups_data[sg]['id']
        key_student = groups_data[sg]['students'][selected_student]['id']
        grades_data = __validate_keys_existence(
            key_group,
            key_student,
            grades_data
        )
        grades_data[key_group]['students_grades'][key_student].append(grade)
        json.dump(grades_data, grades_file)
        historical.historical(
            'Insertar',
            'Se insertan calificaciones de alumnos manualmente'
        )
        grades_file.close()
    else:
        print('No existen estudiantes en este grupo. Cree nuevos estudiantes.')


def __read_excel():
    # Obtener datos del Excel y validarlos
    data = files.read_excel_file()
    # Si hay éxito, empezar a añadir los datos
    if data['success']:
        grades_data = get_data()
        grades_file = __open_grades('w')
        for group in data['data']:
            students = data['data'][group].keys()
            for student in students:
                grades = data['data'][group][student]
                grades_data = __validate_keys_existence(
                    group,
                    student,
                    grades_data
                )
                for grade in grades:
                    grades_data[group]['students_grades'][student].append(
                        float(grade)
                    )
        json.dump(grades_data, grades_file)
        grades_file.close()
        historical.historical(
            'Insertar',
            'Se insertan respuestas de alumnos con Excel'
        )
        print('Se han añadido las calificaciones con éxito')


def __print_instructions():
    print("\n Instrucciones: \n")
    print('1. Seleccionar la opción "1)" en el menú de Excel')
    print(
        '2. Se va a generar un archivo pre-construido con las '
        'columnas a rellenar en la carpeta output dentro de "src"'
    )
    print(
        '3. Al abrirlo, habrán 3 columnas: \n A) Curso (id)\n '
        'B) Alumno (id)\n C) Calificación/Nota -> Formato "Entero.Decimal"'
    )
    print(
        'Si necesita saber estos valores, consultelo dentro de la opción'
        ' "3) Grupos" del menú para Ingresar datos'
    )
    print(
        '4. Rellene tantas filas como necesite. Para posteriormente, '
        'guardar el archivo con el '
        'nombre de "grades.xlsx". Siendo este, '
        'el único nombre que puede tener el archivo'
    )
    print(
        'Trabaje siempre desde la hoja "Grades", de lo contrario, '
        'tampoco se podrá leer el archivo Excel'
    )
    print(
        '5. Colocar este archivo dentro de la carpeta "input". '
        'Si esta no está generada, puede crearla manualmente dentro de "src"'
    )
    print(
        '6. Finalmente, seleccionar la opción "2)"'
        ' en el menú de Excel, '
        'para su lectura y posterior escritura. '
        '(Cualquier error, será notificado para su corrección)\n'
    )


def __generate_excel():
    files.create_excel_file()


def __excel_menu():
    menu_open = True
    while menu_open:
        print('1) Obtener archivo excel tipo')
        print('2) Leer archivo excel desde la carpeta "input"')
        print('3) Instrucciones cómo ingresar archivo excel para leer')
        print('4) Retroceder')
        option = input('Seleccione una opción: ')
        if option == '1':
            __generate_excel()
        elif option == '2':
            __read_excel()
        elif option == '3':
            __print_instructions()
        elif option == '4':
            menu_open = False
        else:
            print('Escoga una opción válida')


def grades():
    menu_open = True
    while menu_open:
        print('1) Ingresar nota manualmente')
        print('2) Ingresar notas por Excel')
        print('3) Retroceder')
        option = input('Seleccione una opción: ')
        if option == '1':
            groups_data = __get_data_groups()
            grades_data = get_data()
            if len(groups_data) > 0:
                __enter_students_grades(groups_data, grades_data)
            else:
                print(
                    'No existen grupos a los cuales agregan notas. '
                    'Cree nuevos grupos.'
                )
        elif option == '2':
            __excel_menu()
        elif option == '3':
            menu_open = False
        else:
            print('Escoga una opción válida')
