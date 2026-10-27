# Lista de tareas CLI en Python

Ejercicio de 4Geeks. Requiere Python 3, sin dependencias externas.

## Ejecutar

```bash
python3 app.py
```

El menu permite agregar, listar, eliminar por posicion (desde 1), guardar,
cargar y salir. Los titulos vacios y las posiciones invalidas se rechazan.
No se incluye edicion de tareas.

Las tareas se cargan automaticamente al iniciar desde `todos.csv` en el
directorio actual. Usa la opcion 4 para guardar antes de salir: la salida
normal, Ctrl+C y el fin de entrada no guardan automaticamente. El CSV usa
UTF-8 y el encabezado `title`. Cargar reemplaza la lista, sin acumular copias.

## Probar

```bash
python3 test.py
```

Las pruebas usan directorios temporales y no modifican tu `todos.csv`.
Para probar manualmente: agrega tres tareas, lista, elimina la posicion 2,
guarda y sal. Ejecuta de nuevo y lista para comprobar la carga automatica.
Puedes inspeccionar el archivo con `cat todos.csv`.
