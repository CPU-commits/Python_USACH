from datetime import date
import pandas as pd
import uuid
import json


from files_data import files
from historical import historical


def __open_answers(mode):
    return open('src/db/answers.json', mode)


def __open_forms(mode):
    return open('src/db/forms.json', mode)


def get_data_answers():
    file = __open_answers('r')
    data = json.load(file)
    file.close()
    return data


def get_data():
    file = __open_forms('r')
    data = json.load(file)
    file.close()
    return data


def __format_forms(forms_data):
    format_forms = []
    for form in forms_data:
        format_forms.append({
            "id": form['id'],
            "name": form['name'],
            "date": form['date'],
        })
    return format_forms


def select_form(forms_data):
    format_forms = __format_forms(forms_data)
    print(pd.DataFrame(format_forms))
    menu_open = True
    while menu_open:
        selected_group = input('Seleccione una encuesta (Posición): ')
        if 0 <= int(selected_group) < len(format_forms):
            menu_open = False
        else:
            print('Seleccione una encuesta válida')
    return int(selected_group)


def __validate_keys(form, group, answers_data):
    if form in answers_data:
        if group not in answers_data[form]:
            answers_data[form][group] = []
    else:
        answers_data[form] = {
            group: []
        }
    return answers_data


def __read_answers():
    data = files.read_excel_file_forms()
    if data['success']:
        answers_data = get_data_answers()
        answers_file = __open_answers('w')
        for form in data['data']:
            groups = data['data'][form].keys()
            for group in groups:
                answers = data['data'][form][group]
                answers_data = __validate_keys(form, group, answers_data)
                for answer in answers:
                    answers_data[form][group].append(answer)
        json.dump(answers_data, answers_file)
        answers_file.close()
        historical.historical('Insertar', 'Se insertan respuestas de alumnos')
        print('Se han añadido las respuestas con éxito')


def __validate_unique_name(name, forms_data):
    unique = list(filter(lambda x: x['name'] == name, forms_data))
    if len(unique) > 0:
        return False
    return True


def __create_form():
    forms_data = get_data()
    menu_open = True
    while menu_open:
        form_name = input('Nombre de formulario: ')
        if len(form_name) > 31:
            print('El nombre debe tener máximo 31 caracteres')
        else:
            unique = __validate_unique_name(form_name, forms_data)
            if unique is False:
                print('El nombre indicado ya está registrado')
            else:
                menu_open = False
    questions = []
    menu_open = True
    while menu_open:
        print('1) Escribir pregunta')
        print('2) Terminar encuesta')
        option = input('Escoga una opción: ')
        if option == '1':
            question = input('Escriba una pregunta: ')
            questions.append(question)
        elif option == '2':
            if len(questions) > 0:
                today = date.today()
                date_format = today.strftime("%d/%m/%Y")
                forms_file = __open_forms('w')
                forms_data.append({
                    "id": str(uuid.uuid4()),
                    "name": form_name,
                    "date": date_format,
                    "questions": questions
                })
                json.dump(forms_data, forms_file)
                forms_file.close()
                historical.historical('Insertar', 'Se inserta formulario')
                menu_open = False
            else:
                print('No tiene ninguna pregunta')


def __print_instructions():
    a_point = ' A) Las respuestas son solo en escala de 0 - 10 (Enteros)'
    b_point = '\n B) El punto A está dado de esta forma ya que,'
    ' es la manera más eficiente de gráficar'
    ' y sacar estadisticas a parametros, que a primera vista, son subjetivos'
    c_point = '\n C) Considere el "0" como menos satisfecho,'
    ' o la respuesta más negativa. Por el contrario, al "10",'
    ' como la respuesta más positiva'
    print('\n Instrucciones: \n')
    print(
        '1. En el menú de encuestas, seleccionar la opción '
        '"1) Crear encuestas"')
    print(
        '2. Las encuestas tienen ciertas consideraciones: '
        f'\n{a_point}{b_point}{c_point}'
    )
    print(
        'Tome en cuenta las consideraciones '
        'antes dadas para así mejorar sus métricas'
    )
    print(
        '3. Cree formularios completos con preguntas acorde a lo '
        'anteriormente dicho'
    )
    print(
        '4. Introdusca las respuestas de estudiantes '
        '(A través de Excel)'
    )
    print('5. El archivo Excel debe llevar como nombre "forms.xlsx"')
    print(
        '6. Para leer las respuestas, las hojas deben llevar el '
        '"id" del formulario como nombre. Consulte el "id" '
        'del formulario en la opción "4)"')
    print(
        '7. Los datos requeridos son (columnas): '
        '\n A) Grupo (id)\n B) Estudiante (id)\n C) Pregunta (Posición)\n '
        'D) Respuesta (Escala 0 - 10) -> Enteros'
    )
    print(
        'Se empezará a leer desde la primera fila, por tanto, '
        'obvie escribir el nombre de las columnas'
    )
    print(
        '8. Guardar el archivo dentro de la carpeta "input" para su lectura,'
        ' y posterior escritura.'
        ' Si esta no está generada, puede crearla '
        'manualmente dentro de "src". '
        '(Cualquier error, será notificado para su corrección)\n'
    )


def __show_forms():
    forms_data = get_data()
    print(pd.DataFrame(forms_data))


def forms():
    menu_open = True
    while menu_open:
        print('1) Crear encuestas')
        print('2) Introducir respuestas a sus encuestas')
        print('3) Instrucciones para crear encuestas')
        print('4) Ver encuestas hechas')
        print('5) Retroceder')
        option = input('Seleccione una opción: ')
        if option == '1':
            __create_form()
        elif option == '2':
            __read_answers()
        elif option == '3':
            __print_instructions()
        elif option == '4':
            __show_forms()
        elif option == '5':
            menu_open = False
        else:
            print('Escoga una opción válida')
