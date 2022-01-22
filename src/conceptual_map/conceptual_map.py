import pandas as pd
import uuid
import json


from historical import historical


def __open_map(mode):
    return open('src/db/maps.json', mode)


def __get_data():
    map_file = __open_map('r')
    data = json.load(map_file)
    map_file.close()
    return data


def __write_map(map, name):
    data = __get_data()
    data.append({
        'id': str(uuid.uuid4()),
        'name': name,
        'map': map,
    })
    map_file = __open_map('w')
    json.dump(data, map_file)


def __horizontal_line(n):
    horizontal = ''
    i = 0
    while i < (n+4):
        horizontal += '―'
        i += 1
    return horizontal


def __vertical_line(n):
    vertical = ''
    i = 0
    while i < ((n+4)//2):
        vertical += ' '
        i += 1
    vertical += '|'
    return vertical


def __draw_map(map):
    print(f'Mapa: {map["name"]}')
    i = 0
    for element in map['map']:
        if i != (len(map['map'])-1):
            horizontal_line = __horizontal_line(len(element))
            vertical_line = __vertical_line(len(map['map'][i+1]))
            print(horizontal_line)
            print(f'| {element} |')
            print(horizontal_line)
            print(vertical_line)
            print(vertical_line)
            print(vertical_line)
        else:
            horizontal_line = __horizontal_line(len(element))
            print(horizontal_line)
            print(f'| {element} |')
            print(horizontal_line)
        i += 1


def __get_map():
    data = __get_data()
    if len(data) > 0:
        print(pd.DataFrame(data))
        menu_open = True
        while menu_open:
            option = int(input('Seleccione un mapa conceptual: '))
            if 0 > option >= len(data):
                print('Escoga una opción válida')
            else:
                menu_open = False
        __draw_map(data[option])
    else:
        print('No hay mapas conceptuales creados')


def __create_conceptual_map():
    name = input('Nombre del mapa conceptual: ')
    elements = []
    menu_open = True
    while menu_open:
        element = input('Escriba una definición o elemento: ')
        elements.append(element)
        print('1) Seguir creando mapa')
        print('2) Finalizar mapa')
        option = input('Seleccione una opción: ')
        if option == '1':
            pass
        elif option == '2':
            menu_open = False
        else:
            print('Escoga una opción válida')
    __write_map(elements, name)
    historical.historical('Insertar', 'Se inserta un mapa conceptual')
    print('Se ha insertado el mapa exitosamente')


def conceptual_map():
    menu_open = True
    while menu_open:
        print('1) Crear mapa conceptual')
        print('2) Ver mapa conceptual')
        print('3) Retroceder')
        option = input('Seleccione una opción: ')
        if option == '1':
            __create_conceptual_map()
        elif option == '2':
            __get_map()
        elif option == '3':
            menu_open = False
        else:
            print('Escoga una opción válida')
