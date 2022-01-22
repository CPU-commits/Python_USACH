operators = ['+', '-', '*', '/', '**']


def __calculate(n1, operator, n2):
    if operator == '+':
        return n1 + n2
    elif operator == '-':
        return n1 - n2
    elif operator == '*':
        return n1 * n2
    elif operator == '/':
        return n1 / n2
    elif operator == '**':
        return n1 ** n2


def __validate(operator):
    if operator not in operators:
        return False
    return True


def __n2andoperator(number1):
    operation_open = True
    while operation_open:
        operator = input('Operador ( + - * / ** ): ')
        if __validate(operator) is False:
            print('Indique un operador válido')
        else:
            operation_open = False
    number2 = float(input('Número 2: '))
    calculate = __calculate(number1, operator, number2)
    print(calculate)
    return calculate


def calculator():
    operation_open = True
    try:
        number1 = float(input('Número: '))
        i = 0
        while operation_open:
            if i == 0:
                number1 = __n2andoperator(number1)
            else:
                menu_open = True
                while menu_open:
                    print('1) Seguir desde el resultado anterior')
                    print('2) Terminar')
                    option = input('Seleccione una opción: ')
                    if option == '1':
                        number1 = __n2andoperator(number1)
                    elif option == '2':
                        menu_open = False
                        operation_open = False
                    else:
                        print('Escoga una opción válida')
            i += 1

    except ValueError:
        print('Debe seleccionar un número')
        calculator()
