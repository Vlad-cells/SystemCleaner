import os
import shutil
import tempfile
from send2trash import send2trash

def clean_temp_files():
    temp_dir = tempfile.gettempdir()
    for root, dirs, files in os.walk(temp_dir):
        for name in files:
            try:
                file_path = os.path.join(root, name)
                send2trash(file_path)
            except Exception as e:
                print(f"Не вдалося видалити {file_path}: {e}")
    return "Тимчасові файли очищено."

def clean_cache():
    cache_paths = [
        os.path.expanduser("~\\AppData\\Local\\Temp"),
        os.path.expanduser("~\\AppData\\Local\\Microsoft\\Windows\\Caches")
    ]
    for path in cache_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for name in files:
                    try:
                        file_path = os.path.join(root, name)
                        send2trash(file_path)
                    except Exception as e:
                        print(f"Не вдалося видалити {file_path}: {e}")
    return "Кеш очищено."

def clean_recycle_bin():
    try:
        os.system("PowerShell.exe Clear-RecycleBin -Force")
        return "Корзина очищена."
    except Exception as e:
        return f"Помилка очищення корзини: {e}"

def full_clean():
    results = []
    results.append(clean_temp_files())
    results.append(clean_cache())
    results.append(clean_recycle_bin())
    return results