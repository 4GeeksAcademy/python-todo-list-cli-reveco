import csv
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import app


class TodoTests(unittest.TestCase):
    def setUp(self):
        self.previous_directory = os.getcwd()
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.addCleanup(os.chdir, self.previous_directory)
        os.chdir(self.directory.name)
        app.todos.clear()
        self.output = io.StringIO()
        self.capture = redirect_stdout(self.output)
        self.capture.__enter__()
        self.addCleanup(self.capture.__exit__, None, None, None)

    def test_add_trims_title_and_allows_multiple_tasks(self):
        app.add_one_task("  Comprar pan  ")
        app.add_one_task("Estudiar Python")
        self.assertEqual(app.todos, ["Comprar pan", "Estudiar Python"])

    def test_add_rejects_empty_titles(self):
        for title in ("", "   ", "\t\n"):
            with self.subTest(title=title):
                app.add_one_task(title)
                self.assertEqual(app.todos, [])
        self.assertEqual(self.output.getvalue().count("El titulo no puede estar vacio."), 3)

    def test_print_list_numbers_each_task(self):
        app.todos.extend(["Comprar pan", "Estudiar Python"])
        app.print_list()
        self.assertEqual(self.output.getvalue(), "1. Comprar pan\n2. Estudiar Python\n")

    def test_print_empty_list(self):
        app.print_list()
        self.assertEqual(self.output.getvalue(), "No hay tareas en la lista.\n")

    def test_delete_valid_position(self):
        app.todos.extend(["Primera", "Segunda", "Tercera"])
        app.delete_task("2")
        self.assertEqual(app.todos, ["Primera", "Tercera"])
        app.delete_task(1)
        self.assertEqual(app.todos, ["Tercera"])

    def test_delete_out_of_range(self):
        app.todos.append("Primera")
        for number in (0, -1, 2):
            with self.subTest(number=number):
                app.delete_task(number)
                self.assertEqual(app.todos, ["Primera"])
        self.assertIn("fuera de rango", self.output.getvalue())

    def test_delete_non_numeric(self):
        app.todos.append("Primera")
        for number in ("hola", "", "1.5", 1.5, None, True):
            with self.subTest(number=number):
                app.delete_task(number)
                self.assertEqual(app.todos, ["Primera"])
        self.assertEqual(self.output.getvalue().count("numero entero valido"), 6)

    def test_delete_from_empty_list(self):
        app.delete_task(1)
        self.assertEqual(app.todos, [])
        self.assertIn("fuera de rango", self.output.getvalue())

    def test_save_load_round_trip(self):
        titles = ["Comprar pan", 'Leer "Python", capitulo 1', "Dos\nlineas"]
        app.todos.extend(titles)
        app.save_todos()
        with open("todos.csv", newline="", encoding="utf-8") as file:
            self.assertEqual(list(csv.reader(file)), [["title"]] + [[title] for title in titles])
        app.todos.clear()
        app.load_todos()
        self.assertEqual(app.todos, titles)

    def test_load_missing_file_clears_list(self):
        app.todos.append("Anterior")
        app.load_todos()
        self.assertEqual(app.todos, [])
        self.assertFalse(os.path.exists("todos.csv"))

    def test_load_replaces_list_without_duplicates(self):
        app.todos.extend(["Primera", "Segunda"])
        original_list = app.todos
        app.save_todos()
        app.todos.append("Solo en memoria")
        app.load_todos()
        app.load_todos()
        self.assertEqual(app.todos, ["Primera", "Segunda"])
        self.assertIs(app.todos, original_list)

    def test_save_load_empty_list(self):
        app.save_todos()
        app.todos.append("Temporal")
        app.load_todos()
        self.assertEqual(app.todos, [])

    def test_main_loads_saved_tasks_at_start(self):
        app.todos.append("Guardada")
        app.save_todos()
        app.todos.clear()
        with patch("builtins.input", side_effect=["2", "6"]):
            app.main()
        self.assertEqual(app.todos, ["Guardada"])
        self.assertIn("1. Guardada", self.output.getvalue())

    def test_main_handles_invalid_option(self):
        with patch("builtins.input", side_effect=["incorrecta", "6"]):
            app.main()
        self.assertIn("Opcion invalida", self.output.getvalue())

    def test_main_handles_interruption(self):
        for error in (KeyboardInterrupt, EOFError):
            with self.subTest(error=error):
                with patch("builtins.input", side_effect=error):
                    app.main()
        self.assertEqual(self.output.getvalue().count("Hasta luego."), 2)


if __name__ == "__main__":
    unittest.main()