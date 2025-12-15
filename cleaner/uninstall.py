import subprocess

def get_installed_programs():
    # Отримуємо список програм через WMIC
    try:
        output = subprocess.check_output(
            ['wmic', 'product', 'get', 'name'],
            universal_newlines=True,
            stderr=subprocess.DEVNULL
        )
        lines = output.split('\n')[1:]
        programs = [line.strip() for line in lines if line.strip()]
        return programs
    except Exception as e:
        return [f"Помилка: {e}"]

def uninstall_program(program_name):
    try:
        subprocess.run(['wmic', 'product', 'where', f'name="{program_name}"', 'call', 'uninstall'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"✅ Видалено: {program_name}"
    except Exception as e:
        return f"❌ Помилка при видаленні {program_name}: {e}"