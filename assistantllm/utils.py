import os

def get_project_files(project_dir):
    """Сканирует директорию проекта и возвращает список всех файлов."""
    file_list = []
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list