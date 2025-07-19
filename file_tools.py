"""
title: File Management Tools
author: Boris Mikhailenko
date: 2025-07-18
version: 1.0
license: MIT
description: File management tools.
"""

from pathlib import Path
import shutil
import logging
import datetime


logging.basicConfig(level=logging.INFO)


class Tools:
    def __init__(self):
        self.base_path = '/path/to/folder/'

    def create_folder(self, folder_name: str) -> str:
        """
        Create a new folder.
        :param folder_name: Path to the folder to create (e.g. 'documents' or 'project/docs').
        :return: A success message if the folder is created successfully.
        """
        folder_path = Path(self.base_path) / folder_name
        if not folder_path.exists():
            folder_path.mkdir(parents=True)
            logging.info(
                f"Folder '{folder_name}' created successfully at {folder_path}!"
            )
            return f"Folder '{folder_name}' created successfully!"
        else:
            logging.warning(f"Folder '{folder_name}' already exists at {folder_path}.")
            return f"Folder '{folder_name}' already exists."

    def delete_folder(self, folder_name: str) -> str:
        """
        Delete a folder.
        :param folder_name: Path to the folder to delete (e.g. 'temp' or 'project/temp').
        :return: A success message if the folder is deleted successfully.
        """
        folder_path = Path(self.base_path) / folder_name
        if folder_path.exists():
            shutil.rmtree(folder_path)
            logging.info(
                f"Folder '{folder_name}' deleted successfully from {folder_path}!"
            )
            return f"Folder '{folder_name}' deleted successfully!"
        else:
            logging.warning(f"Folder '{folder_name}' does not exist at {folder_path}.")
            return f"Folder '{folder_name}' does not exist."

    def create_file(self, file_name: str, content: str = "") -> str:
        """
        Create a new file.
        :param file_name: Path to the file to create (e.g. 'readme.txt' or 'docs/readme.txt').
        :param content: The content to write to the file.
        :return: A success message if the file is created successfully.
        """
        file_path = Path(self.base_path) / file_name
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w") as file:
            file.write(content)
        logging.info(f"File '{file_name}' created successfully at {file_path}!")
        return f"File '{file_name}' created successfully!"

    def delete_file(self, file_name: str) -> str:
        """
        Delete a file.
        :param file_name: Path to the file to delete (e.g. 'old.txt' or 'backup/old.txt').
        :return: A success message if the file is deleted successfully.
        """
        file_path = Path(self.base_path) / file_name
        if file_path.exists():
            file_path.unlink()
            logging.info(f"File '{file_name}' deleted successfully from {file_path}!")
            return f"File '{file_name}' deleted successfully!"
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def read_file(self, file_name: str) -> str:
        """
        Read the content of a file.
        :param file_name: Path to the file to read (e.g. 'data.txt' or 'config/settings.json').
        :return: The content of the file.
        """
        file_path = Path(self.base_path) / file_name
        if file_path.exists():
            with file_path.open("r") as file:
                content = file.read()
            logging.info(f"File '{file_name}' read successfully from {file_path}!")
            return content
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def write_to_file(self, file_name: str, content: str) -> str:
        """
        Write content to a file.
        :param file_name: Path to the file to write to (e.g. 'log.txt' or 'logs/app.log').
        :param content: The content to write to the file.
        :return: A success message if the content is written successfully.
        """
        file_path = Path(self.base_path) / file_name
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w") as file:
            file.write(content)
        logging.info(
            f"Content written to file '{file_name}' successfully at {file_path}!"
        )
        return f"Content written to file '{file_name}' successfully!"

    def list_files(self, directory: str = "") -> str:
        """
        List all files in the specified directory.
        :param directory: Path to the directory to list (e.g. '' for current directory, 'docs' for docs folder).
        :return: A list of files in the specified directory.
        """
        directory_path = Path(self.base_path) / directory
        files = [file.name for file in directory_path.iterdir()]
        logging.info(f"Files listed successfully from {directory_path}!")
        return "Files in the specified directory:\n" + "\n".join(files)

    def copy_file(self, src_file: str, dest_file: str) -> str:
        """
        Copy a file from source to destination.
        :param src_file: Path to the source file (e.g. 'original.txt' or 'src/data.csv').
        :param dest_file: Path to the destination file (e.g. 'copy.txt' or 'backup/data.csv').
        :return: A success message if the file is copied successfully.
        """
        src_file_path = Path(self.base_path) / src_file
        dest_file_path = Path(self.base_path) / dest_file

        # Ensure destination directory exists
        dest_file_path.parent.mkdir(parents=True, exist_ok=True)

        if src_file_path.exists():
            shutil.copy2(src_file_path, dest_file_path)
            logging.info(f"File '{src_file}' copied successfully to {dest_file_path}!")
            return f"File '{src_file}' copied successfully to {dest_file}!"
        else:
            logging.warning(f"File '{src_file}' does not exist at {src_file_path}.")
            return f"File '{src_file}' does not exist."

    def copy_folder(self, src_folder: str, dest_folder: str) -> str:
        """
        Copy a folder from source to destination.
        :param src_folder: Path to the source folder (e.g. 'docs' or 'project/docs').
        :param dest_folder: Path to the destination folder (e.g. 'docs_backup' or 'backup/docs').
        :return: A success message if the folder is copied successfully.
        """
        src_folder_path = Path(self.base_path) / src_folder
        dest_folder_path = Path(self.base_path) / dest_folder

        # Ensure parent directory of destination exists
        dest_folder_path.parent.mkdir(parents=True, exist_ok=True)

        if src_folder_path.exists():
            shutil.copytree(src_folder_path, dest_folder_path)
            logging.info(
                f"Folder '{src_folder}' copied successfully to {dest_folder_path}!"
            )
            return f"Folder '{src_folder}' copied successfully to {dest_folder}!"
        else:
            logging.warning(
                f"Folder '{src_folder}' does not exist at {src_folder_path}."
            )
            return f"Folder '{src_folder}' does not exist."

    def move_file(self, src_file: str, dest_file: str) -> str:
        """
        Move a file from source to destination.
        :param src_file: Path to the source file (e.g. 'temp.txt' or 'temp/data.json').
        :param dest_file: Path to the destination file (e.g. 'final.txt' or 'final/data.json').
        :return: A success message if the file is moved successfully.
        """
        src_file_path = Path(self.base_path) / src_file
        dest_file_path = Path(self.base_path) / dest_file

        # Ensure destination directory exists
        dest_file_path.parent.mkdir(parents=True, exist_ok=True)

        if src_file_path.exists():
            shutil.move(src_file_path, dest_file_path)
            logging.info(f"File '{src_file}' moved successfully to {dest_file_path}!")
            return f"File '{src_file}' moved successfully to {dest_file}!"
        else:
            logging.warning(f"File '{src_file}' does not exist at {src_file_path}.")
            return f"File '{src_file}' does not exist."

    def move_folder(self, src_folder: str, dest_folder: str) -> str:
        """
        Move a folder from source to destination.
        :param src_folder: Path to the source folder (e.g. 'old_docs' or 'project/old_docs').
        :param dest_folder: Path to the destination folder (e.g. 'new_docs' or 'archive/docs').
        :return: A success message if the folder is moved successfully.
        """
        src_folder_path = Path(self.base_path) / src_folder
        dest_folder_path = Path(self.base_path) / dest_folder

        # Ensure parent directory of destination exists
        dest_folder_path.parent.mkdir(parents=True, exist_ok=True)

        if src_folder_path.exists():
            shutil.move(src_folder_path, dest_folder_path)
            logging.info(
                f"Folder '{src_folder}' moved successfully to {dest_folder_path}!"
            )
            return f"Folder '{src_folder}' moved successfully to {dest_folder}!"
        else:
            logging.warning(
                f"Folder '{src_folder}' does not exist at {src_folder_path}."
            )
            return f"Folder '{src_folder}' does not exist."

    def is_file(self, path: str) -> bool:
        """
        Check if the given path is a file.
        :param path: The path to check.
        :return: True if the path is a file, False otherwise.
        """
        return Path(path).is_file()

    def is_directory(self, path: str) -> bool:
        """
        Check if the given path is a directory.
        :param path: The path to check.
        :return: True if the path is a directory, False otherwise.
        """
        return Path(path).is_dir()

    def get_file_metadata(self, file_name: str) -> dict:
        """
        Get metadata of a file.
        :param file_name: Path to the file to get metadata for (e.g. 'document.txt' or 'images/photo.jpg').
        :return: A dictionary containing the file's metadata.
        """
        file_path = Path(self.base_path) / file_name
        if file_path.exists():
            stat = file_path.stat()
            return {
                "size": stat.st_size,
                "creation_time": datetime.datetime.fromtimestamp(
                    stat.st_ctime
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "modification_time": datetime.datetime.fromtimestamp(
                    stat.st_mtime
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "access_time": datetime.datetime.fromtimestamp(
                    stat.st_atime
                ).strftime("%Y-%m-%d %H:%M:%S"),
            }
        else:
            logging.warning(f"File '{file_name}' does not exist at {file_path}.")
            return f"File '{file_name}' does not exist."

    def search_files(self, keyword: str, directory: str = "") -> list:
        """
        Search for files containing the keyword in their names or content.
        :param keyword: The keyword to search for.
        :param directory: Path to the directory to search in (e.g. '' for current directory, 'src' for src folder).
        :return: A list of file paths that match the search criteria.
        """
        search_path = Path(self.base_path) / directory
        matching_files = []

        # Функция для проверки содержимого файла
        def check_file_content(file_path):
            try:
                with file_path.open("r") as f:
                    return keyword in f.read()
            except (UnicodeDecodeError, PermissionError):
                # Skip files that can't be read as text
                return False

        # Поиск по имени и содержимому
        for file_path in search_path.rglob("*"):
            if file_path.is_file():
                if keyword in file_path.name or check_file_content(file_path):
                    matching_files.append(str(file_path))

        logging.info(
            f"Search for keyword '{keyword}' completed with {len(matching_files)} matches!"
        )
        return matching_files
