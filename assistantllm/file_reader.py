import os

def read_file_content(file_path):
    """Читает содержимое файла по указанному пути."""
    if not os.path.exists(file_path):
        return None, f"[red]File {file_path} not found.[/red]"
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content, None
    except Exception as e:
        return None, f"[red]Error reading file {file_path}: {e}[/red]"

def file_exists(file_path):
    """Проверяет, существует ли файл."""
    return os.path.isfile(file_path)

def is_project_file(project_dir, file_path):
    """Проверяет, находится ли файл в директории проекта."""
    absolute_path = os.path.abspath(file_path)
    return absolute_path.startswith(os.path.abspath(project_dir))
