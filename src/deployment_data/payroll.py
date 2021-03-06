import pandas as pd
import functools


from get_into_data import groups
from get_into_data import forms
from get_into_data import grades


def __print_form(forms_data, format_form):
    print(f"\nFormulario: {forms_data['name']}")
    for question in format_form:
        print(f"\n Pregunta: {question} \n")
        print(pd.DataFrame(format_form[question]))
    print('\n')


def __format_form(answers_data, forms_data, groups_data, general=True):
    format_form = {}
    for answer in answers_data:
        question = forms_data['questions'][answer['question']]
        if general:
            student = list(filter(
                lambda x: x['id'] == answer['student'],
                groups_data['students'],
            ))
        else:
            student = list(filter(
                lambda x: x['id'] == answer['student'],
                groups_data
            ))
        student_name = student[0]['name']
        format_answer = {
            'Estudiante': student_name,
            'Respuesta': answer['answer'],
        }
        if question not in format_form:
            format_form[question] = [format_answer]
        else:
            format_form[question].append(format_answer)
    return True, [
        forms_data,
        format_form,
    ]


def forms_general():
    groups_data = groups.get_data()
    forms_data = forms.get_data()
    answers_data = forms.get_data_answers()
    form = forms.select_form(forms_data)
    form_id = forms_data[form]['id']
    if form_id in answers_data:
        all_answers_data = []
        for group in answers_data[form_id]:
            for answer in answers_data[form_id][group]:
                all_answers_data.append(answer)
        students = []
        for group in groups_data:
            for student in group['students']:
                students.append(student)
        return __format_form(
            all_answers_data,
            forms_data[form],
            students,
            general=False,
        )
    else:
        return False, 'No existen respuestas en este formulario'


def forms_group():
    groups_data = groups.get_data()
    forms_data = forms.get_data()
    answers_data = forms.get_data_answers()
    form = forms.select_form(forms_data)
    group = groups.select_group(groups_data)
    form_id = forms_data[form]['id']
    group_id = groups_data[group]['id']
    if form_id in answers_data:
        if group_id in answers_data[form_id]:
            success, data = __format_form(
                answers_data[form_id][group_id],
                forms_data[form],
                groups_data[group],
            )
            return success, data, groups_data[group]['name']
        else:
            return False, 'No existen respuestas en este groupo'
    else:
        return False, 'No existen respuestas en este formulario'


def grades_general():
    groups_data = groups.get_data()
    grades_data = grades.get_data()
    format_grade = []
    for group in grades_data:
        group_data = list(filter(lambda x: x['id'] == group, groups_data))
        summation = 0
        i = 0
        for student_key in grades_data[group]['students_grades']:
            student = grades_data[group]['students_grades'][student_key]
            summation_student = functools.reduce(lambda a, b: a+b, student)
            i += len(student)
            summation += summation_student
        average = round(summation / i, 1)
        format_grade.append({
            'Grupo': group_data[0]['name'],
            'Promedio': average,
        })
    return format_grade


def __format_grades_group(groups_data, grades_data):
    format_grade = {}
    students = groups_data['students']
    for grade in grades_data['students_grades']:
        student = list(filter(lambda x: x['id'] == grade, students))
        grades = grades_data['students_grades'][grade]
        format_grade[grade] = {
            'Estudiante': student[0]['name'],
            'Calificaciones': grades,
            'Promedio': round((functools.reduce(
                lambda a, b: a+b, grades)/len(grades)
            ), 1)
        }
    new_format_grade = []
    for student in format_grade:
        new_format_grade.append(format_grade[student])
    return new_format_grade


def grades_group():
    groups_data = groups.get_data()
    grades_data = grades.get_data()
    group = groups.select_group(groups_data)
    key_group = groups_data[group]['id']
    if key_group in grades_data:
        data = __format_grades_group(
            groups_data[group],
            grades_data[key_group],
        )
        return True, data, groups_data[group]['name']
    else:
        return False, 'No existen calificaciones en este grupo', None


def payroll():
    menu_open = True
    while menu_open:
        print('1) Calificaciones por grupo')
        print('2) Calificaciones generales (Promedios)')
        print('3) Encuestas por grupo')
        print('4) Encuestas generales')
        print('5) Retroceder')
        option = input('Escoga una opci??n: ')
        if option == '1':
            success, data, _ = grades_group()
            if success:
                print(f"\nDatos: {pd.DataFrame(data)}\n")
            else:
                print(data)
        elif option == '2':
            data = grades_general()
            print(f"\nDatos: {pd.DataFrame(data)}\n")
        elif option == '3':
            success, data, _ = forms_group()
            if success:
                __print_form(data[0], data[1])
            else:
                print(data)
        elif option == '4':
            success, data = forms_general()
            if success:
                __print_form(data[0], data[1])
            else:
                print(data)
        elif option == '5':
            menu_open = False
        else:
            print('Escoga una opci??n v??lida')
