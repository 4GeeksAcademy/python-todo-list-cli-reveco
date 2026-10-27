import csv


todos = []


def add_one_task(title):
    title = title.strip()
    if not title:
        print("El titulo no puede estar vacio.")
        return
    todos.append(title)
    print("Tarea agregada.")


def print_list():
    if not todos:
        print("No hay tareas en la lista.")
        return
    for number, title in enumerate(todos, start=1):
        print(f"{number}. {title}")


def delete_task(number_to_delete):
    if isinstance(number_to_delete, bool) or not isinstance(
        number_to_delete, (str, int)
    ):
        print("Introduce un numero entero valido.")
        return
    try:
        number = int(number_to_delete)
    except ValueError:
        print("Introduce un numero entero valido.")
        return
    if not 1 <= number <= len(todos):
        print("La posicion esta fuera de rango.")
        return
    todos.pop(number - 1)
    print("Tarea eliminada.")


def save_todos():
    try:
        with open("todos.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["title"])
            writer.writerows([title] for title in todos)
    except (OSError, csv.Error, UnicodeError):
        print("No se pudieron guardar las tareas.")
        return
    print("Tareas guardadas en todos.csv.")


def load_todos():
    try:
        with open("todos.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != ["title"]:
                print("El archivo debe tener el encabezado title.")
                return
            loaded = [row["title"].strip() for row in reader if row["title"].strip()]
    except FileNotFoundError:
        todos.clear()
        print("No existe todos.csv; la lista esta vacia.")
        return
    except (OSError, csv.Error, UnicodeError):
        print("No se pudieron cargar las tareas.")
        return
    todos[:] = loaded
    print("Tareas cargadas desde todos.csv.")


def main():
    try:
        load_todos()
        while True:
            print("\n1. Agregar\n2. Listar\n3. Eliminar\n4. Guardar\n5. Cargar\n6. Salir")
            option = input("Elige una opcion: ").strip()
            if option == "1":
                add_one_task(input("Titulo de la tarea: "))
            elif option == "2":
                print_list()
            elif option == "3":
                delete_task(input("Posicion de la tarea: "))
            elif option == "4":
                save_todos()
            elif option == "5":
                load_todos()
            elif option == "6":
                print("Hasta luego.")
                break
            else:
                print("Opcion invalida. Elige un numero del 1 al 6.")
    except (KeyboardInterrupt, EOFError):
        print("\nHasta luego.")


if __name__ == "__main__":
    main()