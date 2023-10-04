import requests
import time

# URL base de la API
url = "http://127.0.0.1:8000"

def mostrar_menu():
    print("\n-------------------------------------------------------------------------\n")
    print("¡MENÚ GENERAL!")
    print(
            "1. Obtener información de un elemento de la tabla periódica\n" + \
            "2. Agregar un nuevo elemento a la tabla periódica\n" + \
            "3. Actualizar información de un elemento de la tabla periódica\n" + \
            "4. Eliminar un elemento de la tabla periódica\n" + \
            "5. Salir\n"
          )
    print("-------------------------------------------------------------------------\n")

def text_to_slow(text):
    for letra in text:
        print(letra, end="", flush=True)
        time.sleep(0.018)

def get_periodic_element(query):
    response = requests.get(f"{url}/periodic_elements/{query}")
    if response.status_code == 404:
        text_to_slow("Elemento no encontrado")
        return None
    else:
        response = response.json()   
        response_text = \
            f'Nombre del elemento: {response.get("element_name")}\n' + \
            f'Número atómico del elemento: {response.get("atomic_number")}\n' + \
            f'Símbolo del elemento: {response.get("element_symbol")}\n' + \
            f'Masa atómica del elemento: {response.get("atomic_mass_avg")}\n' + \
            f'Descripción adicional del elemento: {response.get("description")}\n\n'
        return response_text
           
def post_update_periodic_element(atomic_number, element):
    response = requests.put(f"{url}/periodic_elements/{atomic_number}", json=element)
    if response.status_code == 404:
        print("Elemento no encontrado")
        return None
    else:
        return response.json()

def post_create_periodic_element(element):
    response = requests.post(f"{url}/periodic_elements", json=element)
    if response.json().get('detail'):
      print('El elemento no pudo ser creado.') 
    return response.json()

def post_delete_periodic_element(atomic_number):
    response = requests.delete(f"{url}/periodic_elements/{atomic_number}")
    if response.json().get('detail'):
      print('El elemento no existe.')
    return response.json()

def get_valid_int_input(value: str) -> int:
    user_input = input(f'Ingrese un valor para {value} (debe ser entero, sino se solicita nuevamente el ingreso): ')
    return int(user_input) if user_input.isdigit() else get_valid_int_input(value)

def get_valid_float_input(value: str) -> float:
    user_input = input(f'Ingrese un valor para {value} (debe ser decimal o entero, sino se solicita nuevamente el ingreso): ').replace(',', '.')
    if user_input.count('.') > 1:
        print('Ups, tienes más de un punto decimal ingresado.')
        return get_valid_float_input(value)
    if user_input.replace('.', '').isdigit():
        return float(user_input)
    else:
        print('La entrada no es válida, debe ser un número decimal o entero.')
        return get_valid_float_input(value)

def create_periodic_element():
    options = {
            1: ["element_name", "Nombre del elemento"],
            2: ["element_symbol", "Símbolo del elemento"],
            3: ["atomic_number", "Número atómico del elemento"],
            4: ["atomic_mass_avg", "Masa atómica del elemento"],
            5: ["description", "Descripción del elemento"]
        }
    
    elements = True
    while elements:
        try:
            element = {
                        "element_name": input(f'Ingrese un valor para "{options[1][1]}": '),
                        "element_symbol": input(f'Ingrese un valor para "{options[2][1]}": '),
                        "atomic_number": get_valid_int_input(options[3][1]),
                        "atomic_mass_avg": get_valid_float_input(options[4][1]),
                        "description": input(f'Ingrese un valor para "{options[5][1]}": ')
            }
            elements = False
        except ValueError:
            text_to_slow('El valor ingresado es incorrecto, vuelva a agregar nuevamente la información.')
            continue

    if element:
        text_to_slow('\nSe insertará el elemento de la siguiente manera: \n\n')
        for value in options.values():
            for key, value_ in element.items():
                if value[0] == key:
                    print(f"{value[1]}: {value_}")
        
        text_to_slow('\n¿Estás seguro de insertar el nuevo elemento? \n1.Sí\n2.No\n\nIndique la opción elegida: ')
        yes_not = int(input())
        if yes_not == 1:
            response = post_create_periodic_element(element)
            if not response.get('detail'):
                print("\n*************************************************************************")
                print('¡EL ELEMENTO SE HA INSERTADO CORRECTAMENTE!')
                print("*************************************************************************")
        elif yes_not == 2:
            text_to_slow('Volviendo al menú principal...\n') 
        else:
            text_to_slow('Opción inválida.')

def update_periodic_element(atomic_number):
    response_text = get_periodic_element(atomic_number)
    if response_text:
        text_to_slow('\nLa información que contiene actualmente el elemento indicado es: \n\n')
        text_to_slow(response_text)

        options = {
            2: ["element_name", "Nombre del Elemento"],
            3: ["element_symbol", "Símbolo del Elemento"],
            4: ["atomic_mass_avg", "Masa atómica del Elemento"],
            5: ["description", "Descripción del Elemento"]
        }
        element = {}
        while True:
            print("-------------------------------------------------------------------------\n")
            text_to_slow('¡MENU DE EDICIÓN!\n')
            print(
                    '1. Editar toda la información del elemento. \n' + \
                    '2. Editar nombre del elemento. \n' + \
                    '3. Editar el símbolo del elemento. \n' + \
                    '4. Editar masa atómica del elemento. \n' + \
                    '5. Editar la descripción del elemento. \n' + \
                    '6. Volver al menú. \n' + \
                    '7. Salir.\n'
                )
            print("-------------------------------------------------------------------------\n")
            text_to_slow('Si desea editar la información actual, seleccione alguna de las opciones: ')
            option = int(input())

            if option == 1:
                elements = True
                while elements:
                    try:
                        element = {
                            "element_name": input(f'\nIngrese un nuevo valor para "{options[2][1]}": '),
                            "element_symbol": input(f'Ingrese un nuevo valor para "{options[3][1]}": '),
                            "atomic_mass_avg": get_valid_float_input(options[4][1]),
                            "description": input(f'Ingrese un nuevo valor para "{options[5][1]}": ')
                        }
                        elements = False
                    except ValueError:
                        text_to_slow('El valor ingresado es incorrecto. Ingresar nuevamente toda la información.')
                        continue
                break
            elif (1<option<6):
                field, field_name = options[option]
                if option == 4:
                    new_value = get_valid_float_input(field_name)
                else:
                    new_value = input(f'\nIngrese un nuevo valor para "{field_name}": ')
                if new_value:
                    element[field] = new_value
                    break
                else:
                    text_to_slow('Opción inválida.')
            elif option == 6:     
                break
            elif option == 7:
                text_to_slow('¡Hasta luego!')
                return 
        
        if element:
            element["atomic_number"] = atomic_number
            text_to_slow('\nSe modificará el elemento de la siguiente manera: \n')
            for value in options.values():
                for key, value_ in element.items():
                    if value[0] == key:
                        print(f"{value[1]}: {value_}")

            text_to_slow('\n¿Estás seguro de editar la información? \n1.Sí\n2.No\n\nIndique la opción elegida: ')
            yes_not = int(input())
            if yes_not == 1:
                response = post_update_periodic_element(atomic_number, element)
                if not response.get('detail'):
                    print("\n*************************************************************************")
                    print('¡EL ELEMENTO SE HA ACTUALIZADO CORRECTAMENTE!')
                    print("*************************************************************************")
                else:
                    print(response.get('detail'))
            elif yes_not == 2:
                text_to_slow('Volviendo al menú principal...\n') 
            else:
                text_to_slow('Opción inválida.')

def delete_periodic_element(atomic_number):
    response_text = get_periodic_element(atomic_number)
    if response_text:
        text_to_slow('\nLa información que contiene actualmente el elemento indicado es: \n')
        text_to_slow(response_text)

        text_to_slow('\n¿Estás seguro de eliminar el elemento? \n1.Sí\n2.No\n\nIndique la opción elegida: ')
        yes_not = int(input())
        if yes_not == 1:
            response = post_delete_periodic_element(atomic_number)
            if not response.get('detail'):
                print("\n*************************************************************************")
                print('¡EL ELEMENTO SE HA ELIMINADO CORRECTAMENTE!')
                print("*************************************************************************")
            else:
                print(response.get('detail'))

def main():
    print("\n¡Sea usted bienvenido a PT (Periodic Table) By Melisa Carricart!")
    while True:
        mostrar_menu()
        opcion = input("Seleccione por favor alguna de las opciones: ")

        print("\n-------------------------------------------------------------------------\n")

        if opcion == "1":
            query = input('Indique el número atómico ó el símbolo del elemento de la tabla periódica: ')
            response_text = get_periodic_element(query)
            if response_text:
                element_name = response_text.split('\n')[0].split(':')[1].strip(' ')
                print(f'\nEl elemento seleccionado es: "{element_name}".\n\nLe proporcionamos más información detallada a continuación:\n')
                text_to_slow(response_text)
        elif opcion == "2":
            create_periodic_element()
            continue
        elif opcion == "3":
            atomic_number = input('Indique el número atómico del elemento de la tabla periódica: ')
            update_periodic_element(atomic_number)
        elif opcion == "4":
            atomic_number = input('Indique el número atómico del elemento de la tabla periódica: ')
            delete_periodic_element(atomic_number)
        elif opcion == "5":
            text_to_slow("¡Hasta luego!")
            break
        else:
            text_to_slow("Opción inválida. Por favor, selecciona una opción válida.\n")

main()