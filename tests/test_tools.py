import os
import shutil
import tempfile
import unittest
from file_tools import Tools
from pathlib import Path

class TestTools(unittest.TestCase):
    def setUp(self):
        # Создаем временную директорию для тестов
        self.temp_dir = tempfile.mkdtemp()
        # Инициализируем инструмент с временной директорией
        self.tools = Tools()
        # Переопределяем базовый путь на временную директорию
        self.tools.base_path = self.temp_dir

    def tearDown(self):
        # Удаляем временную директорию после завершения тестов
        shutil.rmtree(self.temp_dir)

    def test_create_folder(self):
        # Тест создания папки
        folder_name = "test_folder"
        result = self.tools.create_folder(folder_name)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, folder_name)))
        self.assertIn("created successfully", result)

        # Тест создания вложенной папки
        nested_folder = "parent/child"
        result = self.tools.create_folder(nested_folder)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, nested_folder)))
        self.assertIn("created successfully", result)

        # Тест повторного создания существующей папки
        result = self.tools.create_folder(folder_name)
        self.assertIn("already exists", result)

    def test_delete_folder(self):
        # Создаем папку для тестирования удаления
        folder_name = "folder_to_delete"
        os.makedirs(os.path.join(self.temp_dir, folder_name))

        # Тест удаления папки
        result = self.tools.delete_folder(folder_name)
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, folder_name)))
        self.assertIn("deleted successfully", result)

        # Тест удаления несуществующей папки
        result = self.tools.delete_folder("nonexistent_folder")
        self.assertIn("does not exist", result)

    def test_create_file(self):
        # Тест создания файла
        file_name = "test_file.txt"
        content = "Hello, World!"
        result = self.tools.create_file(file_name, content)
        file_path = os.path.join(self.temp_dir, file_name)
        self.assertTrue(os.path.exists(file_path))
        self.assertIn("created successfully", result)

        # Проверяем содержимое файла
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), content)

        # Тест создания файла в подпапке
        nested_file = "subfolder/test.txt"
        result = self.tools.create_file(nested_file, content)
        nested_path = os.path.join(self.temp_dir, nested_file)
        self.assertTrue(os.path.exists(nested_path))
        self.assertTrue(os.path.exists(os.path.dirname(nested_path)))
        self.assertIn("created successfully", result)

    def test_delete_file(self):
        # Создаем файл для тестирования удаления
        file_name = "file_to_delete.txt"
        file_path = os.path.join(self.temp_dir, file_name)
        with open(file_path, 'w') as f:
            f.write("Test content")

        # Тест удаления файла
        result = self.tools.delete_file(file_name)
        self.assertFalse(os.path.exists(file_path))
        self.assertIn("deleted successfully", result)

        # Тест удаления несуществующего файла
        result = self.tools.delete_file("nonexistent_file.txt")
        self.assertIn("does not exist", result)

    def test_read_file(self):
        # Создаем файл для тестирования чтения
        file_name = "file_to_read.txt"
        content = "This is test content for reading."
        file_path = os.path.join(self.temp_dir, file_name)
        with open(file_path, 'w') as f:
            f.write(content)

        # Тест чтения файла
        result = self.tools.read_file(file_name)
        self.assertEqual(result, content)

        # Тест чтения несуществующего файла
        result = self.tools.read_file("nonexistent_file.txt")
        self.assertIn("does not exist", result)

    def test_write_to_file(self):
        # Тест записи в файл
        file_name = "file_to_write.txt"
        content = "This is test content for writing."
        result = self.tools.write_to_file(file_name, content)
        file_path = os.path.join(self.temp_dir, file_name)
        self.assertTrue(os.path.exists(file_path))
        self.assertIn("written to file", result)

        # Проверяем содержимое файла
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), content)

        # Тест перезаписи файла
        new_content = "This is updated content."
        self.tools.write_to_file(file_name, new_content)
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), new_content)

    def test_list_files(self):
        # Создаем файлы для тестирования списка
        file_names = ["file1.txt", "file2.txt", "file3.txt"]
        for file_name in file_names:
            with open(os.path.join(self.temp_dir, file_name), 'w') as f:
                f.write("Content")

        # Создаем подпапку и файл в ней
        subfolder = "subfolder"
        os.makedirs(os.path.join(self.temp_dir, subfolder))
        with open(os.path.join(self.temp_dir, subfolder, "subfile.txt"), 'w') as f:
            f.write("Subfolder content")

        # Тест списка файлов в корневой директории
        result = self.tools.list_files()
        for file_name in file_names:
            self.assertIn(file_name, result)
        self.assertIn(subfolder, result)

        # Тест списка файлов в подпапке
        result = self.tools.list_files(subfolder)
        self.assertIn("subfile.txt", result)

    def test_copy_file(self):
        # Создаем файл для тестирования копирования
        src_file = "source.txt"
        dest_file = "destination.txt"
        content = "This is source file content."
        src_path = os.path.join(self.temp_dir, src_file)
        dest_path = os.path.join(self.temp_dir, dest_file)

        with open(src_path, 'w') as f:
            f.write(content)

        # Тест копирования файла
        result = self.tools.copy_file(src_file, dest_file)
        self.assertTrue(os.path.exists(dest_path))
        self.assertIn("copied successfully", result)

        # Проверяем содержимое скопированного файла
        with open(dest_path, 'r') as f:
            self.assertEqual(f.read(), content)

        # Тест копирования файла в подпапку
        nested_dest = "subfolder/nested_dest.txt"
        result = self.tools.copy_file(src_file, nested_dest)
        nested_path = os.path.join(self.temp_dir, nested_dest)
        self.assertTrue(os.path.exists(nested_path))
        self.assertIn("copied successfully", result)

        # Тест копирования несуществующего файла
        result = self.tools.copy_file("nonexistent.txt", "any_dest.txt")
        self.assertIn("does not exist", result)

    def test_copy_folder(self):
        # Создаем папку с файлами для тестирования копирования
        src_folder = "source_folder"
        dest_folder = "dest_folder"
        src_path = os.path.join(self.temp_dir, src_folder)
        dest_path = os.path.join(self.temp_dir, dest_folder)

        os.makedirs(src_path)
        with open(os.path.join(src_path, "file1.txt"), 'w') as f:
            f.write("File 1 content")
        with open(os.path.join(src_path, "file2.txt"), 'w') as f:
            f.write("File 2 content")

        # Создаем вложенную папку
        os.makedirs(os.path.join(src_path, "subdir"))
        with open(os.path.join(src_path, "subdir", "subfile.txt"), 'w') as f:
            f.write("Subfile content")

        # Тест копирования папки
        result = self.tools.copy_folder(src_folder, dest_folder)
        self.assertTrue(os.path.exists(dest_path))
        self.assertTrue(os.path.exists(os.path.join(dest_path, "file1.txt")))
        self.assertTrue(os.path.exists(os.path.join(dest_path, "file2.txt")))
        self.assertTrue(os.path.exists(os.path.join(dest_path, "subdir")))
        self.assertTrue(os.path.exists(os.path.join(dest_path, "subdir", "subfile.txt")))
        self.assertIn("copied successfully", result)

        # Тест копирования несуществующей папки
        result = self.tools.copy_folder("nonexistent_folder", "any_dest")
        self.assertIn("does not exist", result)

    def test_move_file(self):
        # Создаем файл для тестирования перемещения
        src_file = "source_move.txt"
        dest_file = "destination_move.txt"
        content = "This is file to move."
        src_path = os.path.join(self.temp_dir, src_file)
        dest_path = os.path.join(self.temp_dir, dest_file)

        with open(src_path, 'w') as f:
            f.write(content)

        # Тест перемещения файла
        result = self.tools.move_file(src_file, dest_file)
        self.assertFalse(os.path.exists(src_path))
        self.assertTrue(os.path.exists(dest_path))
        self.assertIn("moved successfully", result)

        # Проверяем содержимое перемещенного файла
        with open(dest_path, 'r') as f:
            self.assertEqual(f.read(), content)

        # Тест перемещения несуществующего файла
        result = self.tools.move_file("nonexistent.txt", "any_dest.txt")
        self.assertIn("does not exist", result)

    def test_move_folder(self):
        # Создаем папку с файлами для тестирования перемещения
        src_folder = "source_move_folder"
        dest_folder = "dest_move_folder"
        src_path = os.path.join(self.temp_dir, src_folder)
        dest_path = os.path.join(self.temp_dir, dest_folder)

        os.makedirs(src_path)
        with open(os.path.join(src_path, "file1.txt"), 'w') as f:
            f.write("File 1 content")

        # Тест перемещения папки
        result = self.tools.move_folder(src_folder, dest_folder)
        self.assertFalse(os.path.exists(src_path))
        self.assertTrue(os.path.exists(dest_path))
        self.assertTrue(os.path.exists(os.path.join(dest_path, "file1.txt")))
        self.assertIn("moved successfully", result)

        # Тест перемещения несуществующей папки
        result = self.tools.move_folder("nonexistent_folder", "any_dest")
        self.assertIn("does not exist", result)

    def test_is_file(self):
        # Создаем файл для тестирования
        file_name = "test_is_file.txt"
        file_path = os.path.join(self.temp_dir, file_name)
        with open(file_path, 'w') as f:
            f.write("Content")

        # Создаем папку для тестирования
        folder_name = "test_is_file_folder"
        folder_path = os.path.join(self.temp_dir, folder_name)
        os.makedirs(folder_path)

        # Тест проверки файла
        self.assertTrue(self.tools.is_file(file_path))
        self.assertFalse(self.tools.is_file(folder_path))
        self.assertFalse(self.tools.is_file(os.path.join(self.temp_dir, "nonexistent.txt")))

    def test_is_directory(self):
        # Создаем файл для тестирования
        file_name = "test_is_dir.txt"
        file_path = os.path.join(self.temp_dir, file_name)
        with open(file_path, 'w') as f:
            f.write("Content")

        # Создаем папку для тестирования
        folder_name = "test_is_dir_folder"
        folder_path = os.path.join(self.temp_dir, folder_name)
        os.makedirs(folder_path)

        # Тест проверки директории
        self.assertTrue(self.tools.is_directory(folder_path))
        self.assertFalse(self.tools.is_directory(file_path))
        self.assertFalse(self.tools.is_directory(os.path.join(self.temp_dir, "nonexistent_dir")))

    def test_get_file_metadata(self):
        # Создаем файл для тестирования метаданных
        file_name = "metadata_test.txt"
        content = "This is test content for metadata."
        file_path = Path(self.temp_dir) / file_name
        with file_path.open('w') as f:
            f.write(content)

        # Тест получения метаданных
        metadata = self.tools.get_file_metadata(file_name)
        self.assertIsInstance(metadata, str)
        self.assertIn(f"size: {len(content)}", metadata)
        self.assertIn("creation_time:", metadata)
        self.assertIn("modification_time:", metadata)
        self.assertIn("access_time:", metadata)

        # Тест получения метаданных несуществующего файла
        result = self.tools.get_file_metadata("nonexistent_file.txt")
        self.assertIsInstance(result, str)
        self.assertIn("does not exist", result)

    def test_search_files(self):
        # Создаем файлы для тестирования поиска
        file1 = "search_test1.txt"
        file2 = "another_file.txt"
        file3 = "subfolder/search_test2.txt"

        os.makedirs(os.path.join(self.temp_dir, "subfolder"))

        with open(os.path.join(self.temp_dir, file1), 'w') as f:
            f.write("This file contains search keyword")

        with open(os.path.join(self.temp_dir, file2), 'w') as f:
            f.write("This file does not contain the term")

        with open(os.path.join(self.temp_dir, file3), 'w') as f:
            f.write("Another file with search keyword")

        # Тест поиска по имени файла
        results = self.tools.search_files("search")
        self.assertEqual(len(results), 2)
        self.assertTrue(any(file1 in r for r in results))
        self.assertTrue(any(file3 in r for r in results))

        # Тест поиска по содержимому
        results = self.tools.search_files("keyword")
        self.assertEqual(len(results), 2)

        # Тест поиска в подпапке
        results = self.tools.search_files("Another", "subfolder")
        self.assertEqual(len(results), 1)


if __name__ == "__main__":
    unittest.main()
