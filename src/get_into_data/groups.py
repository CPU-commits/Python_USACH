import pandas as pd
import uuid
import json

from historical import historical

def __open_groups(mode):
    return open('src/db/groups.json', mode)

def get_data():
    file = __open_groups('r')
    data = json.load(file)
    file.close()
    return data

def __format_group(groups_data):
    format_group = []
    for group in groups_data:
        format_group.append({
            "id": group['id'],
            "name": group['name']
        })
    return format_group

def select_group(groups_data):
    format_group = __format_group(groups_data)
    print(pd.DataFrame(format_group))
    menu_open = True
    while menu_open:
        selected_group = input('Seleccione un grupo (Posición): ')
        if 0 <= int(selected_group) < len(format_group):
            menu_open = False
        else:
            print('Seleccione un grupo válido')
    return int(selected_group)

def get_students(groups_data):
    selected_group = select_group(groups_data)
    students_data = groups_data[selected_group]['students']
    return (students_data, selected_group)

def __create_groups(groups_data, groups):
    course_name = input('Escriba el nombre del grupo: ')
    groups_data.append({
        'id': str(uuid.uuid4()),
        'name': course_name,
        'students': []
    })
    json.dump(groups_data, groups)
    historical.historical('Insertar', 'Se inserta grupo')
    groups.close()

def __create_student(groups_data, groups):
    selected_group = select_group(groups_data)
    student_name = input('Escriba el nombre del estudiante: ')
    groups_data[selected_group]['students'].append({
        'id': str(uuid.uuid4()),
        'name': student_name,
    })
    json.dump(groups_data, groups)
    historical.historical('Insertar', 'Se inserta estudiante a grupo')
    groups.close()

def groups():
    menu_open = True
    while menu_open:
        print('1) Ver grupos creados')
        print('2) Crear grupo')
        print('3) Crear estudiantes')
        print('4) Ver estudiantes grupos')
        print('5) Retroceder')
        option = input('Seleccionar opción: ')
        if option == '1':
            groups = get_data()
            groups = __format_group(groups)
            if len(groups) == 0:
                print('Datos: No hay datos. Cree nuevos grupos.')
            else:
                sr = pd.DataFrame(groups)
                print(f"Datos:\n {sr} \n")
        elif option == '2':
            groups_data = get_data()
            groups = __open_groups('w')
            __create_groups(groups_data, groups)
        elif option == '3':
            groups_data = get_data()
            if len(groups_data) > 0:
                groups = __open_groups('w')
                __create_student(groups_data, groups)
            else:
                print('Debe existir al menos un grupo, para asignar un alumno')
        elif option == '4':
            groups = get_data()
            if len(groups) > 0:
                students_data, _ = get_students(groups)
                if len(students_data) > 0:
                    print(pd.DataFrame(students_data))
                else:
                    print('No existen alumnos en este grupo. Agregue alumnos')
            else:
                print('No existen grupos. Cree nuevos grupos')
        elif option == '5':
            menu_open = False
        else:
            print('Escoga una opción válida')
