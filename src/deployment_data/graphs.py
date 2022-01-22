import pandas as pd
import matplotlib.pyplot as plt


from deployment_data import payroll


def __generate_plot(x, y, file_name):
    _, ax = plt.subplots()
    ax.plot(x, y)
    plt.savefig(f'src/output/plot-{file_name}.png')
    plt.show()


def __generate_bar(y, x, file_name):
    _, ax = plt.subplots()
    ax.bar(y, x)
    plt.savefig(f'src/output/bar-{file_name}.png')
    plt.show()


def __generate_pie(x, labels, file_name):
    _, ax = plt.subplots()
    ax.pie(x, labels=labels, shadow=True)
    plt.savefig(f'src/output/pie-grupo_{file_name}.png')


def __graph_grades_group(data, group_name):
    grades = {}
    for student in data:
        for grade in student['Calificaciones']:
            if grade not in grades:
                grades[grade] = 1
            else:
                grades[grade] += 1
    grades_keys = list(grades.keys())
    grades_count = list(grades[k] for k in grades)
    __generate_bar(grades_keys, grades_count, f'grupo_{group_name}')
    __generate_pie(grades_count, grades_keys, f'grupo_{group_name}')
    print('Se han generado los gráficos en output')


def __select_student(students):
    menu_open = True
    while menu_open:
        print(f"\nDatos: {pd.DataFrame(students)}\n")
        option = int(input('Selecciona un estudiante: '))
        if 0 > option >= len(students):
            print('Seleccione un alumno válido')
        else:
            menu_open = False
    return option


def __graph_grades_student(student):
    grades = {}
    for grade in student['Calificaciones']:
        if grade not in grades:
            grades[grade] = 1
        else:
            grades[grade] += 1
    grades_keys = list(grades.keys())
    grades_count = []
    i = 0
    while i < len(grades_keys):
        grades_count.append(i+1)
        i += 1
    __generate_plot(
        grades_count,
        grades_keys,
        f'estudiante-{student["Estudiante"]}'
    )
    print('Se ha generado el gráfico en output')


def __graph_forms_group(data, group):
    forms = {}
    for form in data[1]:
        for answer in data[1][form]:
            if answer['Respuesta'] not in forms:
                forms[answer['Respuesta']] = 1
            else:
                forms[answer['Respuesta']] += 1
    forms_keys = list(forms.keys())
    forms_count = list(forms[k] for k in forms)
    __generate_bar(forms_keys, forms_count, f'formulario_grupo_{group}')
    __generate_pie(forms_count, forms_keys, f'formulario_grupo_{group}')
    print('Se han generado los gráficos en output')


def graphs():
    menu_open = True
    while menu_open:
        print('1) Calificaciones por grupo')
        print('2) Calificaciones alumno')
        print('3) Encuestas por grupo')
        print('4) Encuestas generales')
        print('5) Retroceder')
        option = input('Escoga una opción: ')
        if option == '1':
            success, data, group_name = payroll.grades_group()
            if success:
                __graph_grades_group(data, group_name)
            else:
                print(data)
        elif option == '2':
            success, data, _ = payroll.grades_group()
            if success:
                student = __select_student(data)
                __graph_grades_student(data[student])
            else:
                print(data)
        elif option == '3':
            success, data, group = payroll.forms_group()
            if success:
                __graph_forms_group(data, group)
            else:
                print(data)
        elif option == '4':
            success, data = payroll.forms_general()
            if success:
                __graph_forms_group(data, f"encuesta_{data[0]['name']}")
            else:
                print(data)
        elif option == '5':
            menu_open = False
        else:
            print('Escoga una opción válida')
