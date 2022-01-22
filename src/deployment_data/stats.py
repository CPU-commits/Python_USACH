from functools import reduce
from os import truncate


from deployment_data import payroll


def __average(data):
    return round((reduce(lambda a, b: a+b, data) / len(data)), 1)


def __median(data):
    if len(data) < 2:
        return data[0]
    mid_position = len(data) / 2
    if type(mid_position):
        return round(
            (data[int(mid_position)] + data[int(mid_position)+1]) / 2,
            1,
        )
    else:
        return data[mid_position]


def __standard_deviation(data):
    average = __average(data)
    sum = 0
    for n in data:
        sum += ((n) - average)**2
    o = (sum/len(data))**0.5
    return round(o, 1)


def __repeat(data):
    repeticiones = 0
    for i in data:
        n = data.count(i)
        if n > repeticiones:
            repeticiones = n
    moda = []
    for i in data:
        n = data.count(i)
        if n == repeticiones and i not in moda:
            moda.append(i)
    return moda


def __generate_stats(data):
    print(f'Media: {__average(data)}')
    print(f'Mediana: {__median(data)}')
    print(f'Desviación estandar: {__standard_deviation(data)}')
    print(f'Moda {__repeat(data)}')


def __grades_group(data):
    grades = []
    for student in data:
        for grade in student['Calificaciones']:
            grades.append(float(grade))
    grades.sort()
    __generate_stats(grades)


def __grades_group_general(data):
    grades = []
    for group in data:
        grades.append(float(group['Promedio']))
    grades.sort()
    __generate_stats(grades)


def __form(data):
    form = []
    for question in data[1]:
        for answer in data[1][question]:
            form.append(float(answer['Respuesta']))
    form.sort()
    __generate_stats(form)


def stats():
    menu_open = True
    while menu_open:
        print('1) Calificaciones por grupo')
        print('2) Calificaciones generales (Promedios)')
        print('3) Encuestas por grupo')
        print('4) Encuestas generales')
        print('5) Retroceder')
        option = input('Escoga una opción: ')
        if option == '1':
            success, data, _ = payroll.grades_group()
            if success:
                __grades_group(data)
            else:
                print(data)
        elif option == '2':
            data = payroll.grades_general()
            __grades_group_general(data)
        elif option == '3':
            success, data, _ = payroll.forms_group()
            if success:
                __form(data)
            else:
                print(data)
        elif option == '4':
            success, data = payroll.forms_general()
            if success:
                __form(data)
            else:
                print(data)
        elif option == '5':
            menu_open = False
        else:
            print('Escoga una opción válida')
