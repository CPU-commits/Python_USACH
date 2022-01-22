from functools import reduce
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors


from deployment_data import payroll
from files_data import files


def __calculate_height(table):
    return reduce(lambda a, b: a + b, table._rowHeights)


def __calculate_width(table):
    return reduce(lambda a, b: a + b, table._colWidths)


def __generate_table(pdf_file, max, dataTable, width, height):
    table = Table(dataTable)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (max, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (max, 0), colors.white),
    ]))
    table.wrapOn(pdf_file, 0, 0)
    table_height = __calculate_height(table)
    table_width = __calculate_width(table)
    table.drawOn(pdf_file, (width-table_width)/2, height-(table_height + 70))
    return table


def __generate_grades_group(pdf_file, w, h, data):
    dataTable = [['Estudiante']]
    max_grades = 0
    for student in data:
        student_len = len(student['Calificaciones'])
        if student_len > max_grades:
            max_grades = student_len
    i = 0
    while i < max_grades:
        dataTable[0].append(str(i+1))
        i += 1
    dataTable[0].append('Promedio')
    for student in data:
        dataStudent = [student['Estudiante']]
        i = 0
        while i < max_grades:
            try:
                dataStudent.append(student['Calificaciones'][i])
            except IndexError:
                dataStudent.append('S/N')
            i += 1
        dataStudent.append(student['Promedio'])
        dataTable.append(dataStudent)
    __generate_table(
        pdf_file,
        max_grades+1,
        dataTable,
        w,
        h,
    )
    pdf_file.showPage()
    return pdf_file


def __generate_pdf_grades_group(data, group_name):
    pdf_file, w, h = files.generate_pdf(
        'calificaciones_grupo',
        f'Calificaciones grupo "{group_name}"',
    )
    pdf_file = __generate_grades_group(pdf_file, w, h, data)
    pdf_file.save()


def __generate_pdf_grades_general(data):
    pdf_file, w, h = files.generate_pdf(
        'calificaciones_general',
        f'Calificaciones Generales (Promedios)',
    )
    dataTable = [['Grupo', 'Promedio']]
    for group in data:
        dataTable.append([
            group['Grupo'],
            group['Promedio'],
        ])
    __generate_table(
        pdf_file,
        1,
        dataTable,
        w,
        h,
    )
    pdf_file.showPage()
    pdf_file.save()


def __generate_pdf_forms_group(data, title, filename):
    pdf_file, _, h = files.generate_pdf(
        filename,
        f'{title} "{data[0]["name"]}" ({data[0]["date"]})',
    )
    y = h - 70
    for question in data[1]:
        pdf_file.setFont('Times-Roman', 18)
        pdf_file.drawString(10, y, f"- {question}")
        y -= 20
        for answer in data[1][question]:
            pdf_file.setFont('Times-Roman', 16)
            pdf_file.drawString(
                30,
                y,
                f"{answer['Estudiante']}: {answer['Respuesta']}",
            )
            y -= 16
            if y <= 0:
                y = h - 20
                pdf_file.showPage()
        y -= 18
    pdf_file.showPage()
    pdf_file.save()


def pdf():
    menu_open = True
    while menu_open:
        print('1) Calificaciones por grupo')
        print('2) Calificaciones generales (Promedios)')
        print('3) Encuestas por grupo')
        print('4) Encuestas generales')
        print('5) Retroceder')
        option = input('Escoga una opción: ')
        if option == '1':
            success, data, group_name = payroll.grades_group()
            if success:
                __generate_pdf_grades_group(data, group_name)
            else:
                print(data)
        elif option == '2':
            data = payroll.grades_general()
            __generate_pdf_grades_general(data)
        elif option == '3':
            success, data, group = payroll.forms_group()
            if success:
                __generate_pdf_forms_group(
                    data,
                    f'Grupo "{group}" Encuesta',
                    'encuesta_grupo',
                )
            else:
                print(data)
        elif option == '4':
            success, data = payroll.forms_general()
            if success:
                __generate_pdf_forms_group(
                    data,
                    'Encuesta general',
                    'encuesta_general',
                )
            else:
                print(data)
        elif option == '5':
            menu_open = False
        else:
            print('Escoga una opción válida')
