import tkinter as tk
from pystray import Icon, MenuItem, Menu
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from PIL import Image, ImageTk, ImageDraw
import subprocess
import psutil
import GPUtil
import os
import ctypes
from pathlib import Path
import wmi
import cpuinfo
import threading
import winreg
import ctypes
from language.lang import t


# Для автозапуску (Windows)
try:
    import winreg
except ImportError:
    winreg = None


def load_icon(path, size=(24, 24)):
    """Безпечне завантаження іконки з перевіркою."""
    try:
        full_path = Path(__file__).parent.parent / path
        if full_path.exists():
            img = Image.open(full_path).resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"⚠️ Не вдалося завантажити {path}: {e}")
    return None


def human_size(bytes_val: int) -> str:
    """Convert bytes to human-readable size."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(bytes_val)
    idx = 0
    while size >= 1024 and idx < len(units) - 1:
        size /= 1024
        idx += 1
    return f"{size:.2f} {units[idx]}"


class CleanerGUI:

    def __init__(self, root):
        self.current_lang = "uk"
        self.root = root
        root.title("System Cleaner")
        try:
            root.state("zoomed")
        except Exception:
            root.geometry("1280x800")

        self.style = Style(theme="flatly")
        self.lang_var = tk.StringVar(value="UA")

        # Header
        self.header = tk.Frame(self.root, bg="white", height=50)
        self.header.pack(side="top", fill="x")

        self.blue_line = tk.Frame(self.header, bg="#0078D7", width=5)
        self.blue_line.pack(side="left", fill="y")

        self.title_label = tk.Label(
            self.header,
            text="System Cleaner",
            bg="white",
            fg="black",
            font=("Segoe UI", 14, "bold"),
        )
        self.title_label.pack(side="left", padx=10)

        self.button_area = tk.Frame(self.header, bg="white")
        self.button_area.pack(side="right", padx=10)

        btn_settings = tk.Button(
            self.button_area,
            text="Налаштування",
            bg="#e0e0e0",
            fg="black",
            relief="flat",
            font=("Segoe UI", 10),
            command=self.show_settings,
        )
        btn_settings.pack(side="left", padx=5)

        btn_about = tk.Button(
            self.button_area,
            text="Про програму",
            bg="#e0e0e0",
            fg="black",
            relief="flat",
            font=("Segoe UI", 10),
            command=lambda: messagebox.showinfo("Про програму", "System Cleaner v1.0"),
        )
        btn_about.pack(side="left", padx=5)

        self.add_hover_effect(btn_settings)
        self.add_hover_effect(btn_about)

        # Layout
        self.sidebar = tk.Frame(self.root, bg="#1e1e1e", width=180)
        self.sidebar.pack(side="left", fill="y")
        self.main_area = tk.Frame(self.root, bg="#2e2e2e")
        self.main_area.pack(side="right", expand=True, fill="both")

        # Icons
        self.icon_health = load_icon("icons/health.png")
        self.icon_clean = load_icon("icons/clean.png")
        self.icon_boost = load_icon("icons/boost.png")
        self.icon_uninstall = load_icon("icons/uninstall.png")
        self.icon_settings = load_icon("icons/settings.png")
        try:
            self.root.iconbitmap("icons/icon.ico")
        except Exception:
            pass

        # Session data
        self._freed_bytes_session = 0
        self.health_active = False
        self.autostart_var = tk.BooleanVar(value=False)

        self.last_scan = "Ніколи"
        self.scan_count = 0
        self.total_detections = 0

        # Build UI
        self.build_sidebar()
        self.show_health_check()

    # -------------------- Service methods --------------------

    def add_hover_effect(self, widget, hover_bg="#d0d0d0", normal_bg="#e0e0e0"):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))

    def t(self, key):
        return t(key, self.current_lang)

    def build_sidebar(self):
        for w in self.sidebar.winfo_children():
            w.destroy()

        sidebar_items = [
        (self.t("health"), self.icon_health, self.show_health_check),
        (self.t("clean"), self.icon_clean, self.show_cleanup_tools),
        (self.t("uninstall"), self.icon_uninstall, self.show_uninstaller),
        (self.t("settings"), self.icon_settings, self.show_settings),
    ]

        for text, icon, command in sidebar_items:
            btn = tk.Button(
                self.sidebar,
                text="  " + text,
                image=icon,
                compound="left",
                bg="#1e1e1e",
                fg="white",
                relief="flat",
                anchor="w",
                font=("Arial", 12),
                command=command,
            )
            btn.pack(fill="x", pady=6, padx=12)

    def clear_main(self):
        self.health_active = False
        for widget in self.main_area.winfo_children():
            widget.destroy()


    # -------------------- Health --------------------

    def get_cpu_temp(self):
        """Отримати температуру CPU через OpenHardwareMonitor."""
        try:
            w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            sensors = w.Sensor()
            for sensor in sensors:
                if sensor.SensorType == "Temperature" and "CPU Package" in sensor.Name:
                    return f"{sensor.Value:.1f}°C"
        except Exception:
            pass
        return "N/A"

    def get_cpu_name(self):
        """Отримати повну назву CPU (спочатку через WMIC, якщо не працює — через cpuinfo)."""
        try:
            output = subprocess.check_output(
                ["wmic", "cpu", "get", "Name"],
                universal_newlines=True,
            )
            lines = [
                line.strip()
                for line in output.splitlines()
                if line.strip() and "Name" not in line
            ]
            if lines:
                return lines[0]
        except Exception:
            pass
        # fallback через cpuinfo
        try:
            info = cpuinfo.get_cpu_info()
            return info.get("brand_raw", "Unknown CPU")
        except Exception:
            return "Unknown CPU"

    def show_health_check(self):
        self.clear_main()
        self.health_active = True

        tk.Label(
            self.main_area,
            text="🧾 " + self.t("system_health"),
            fg="white",
            bg="#2e2e2e",
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=(20, 10))

        self.stats_label = tk.Label(
            self.main_area,
            text=f"❌ Останнє сканування: {self.last_scan}\n"
                f"🟡 Кількість сканувань: {self.scan_count}\n"
                f"✅ Виявлено загроз: {self.total_detections}",
            bg="#2e2e2e",
            fg="white",
            font=("Segoe UI", 11),
            justify="left",
        )
        self.stats_label.pack(pady=(0, 20))

        self.output = tk.Text(
            self.main_area,
            height=12,
            width=90,
            bg="#1e1e1e",
            fg="#00ff99",
            font=("Consolas", 11),
            relief="flat",
        )
        self.output.pack(pady=10, fill="both", expand=True)
        self.output.configure(state="disabled")

        self.update_health_loop()

    def update_health_loop(self):
        if not self.health_active:
            return
        self.scan_system()
        self.main_area.after(1000, self.update_health_loop)

    def scan_system(self):
        from datetime import datetime

        self.last_scan = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.scan_count += 1

        self.output.configure(state="normal")
        self.output.delete(1.0, "end")

        # CPU
        cpu_load = psutil.cpu_percent(interval=None)
        cpu_freq_obj = psutil.cpu_freq()
        cpu_freq = cpu_freq_obj.current if cpu_freq_obj else 0
        cpu_temp = self.get_cpu_temp()
        cpu_name = self.get_cpu_name()

        self.output.insert("end", "🖥 CPU\n")
        self.output.insert("end", f"• Назва: {cpu_name}\n")
        self.output.insert("end", f"• Завантаження: {cpu_load:.1f}%\n")
        self.output.insert("end", f"• Частота: {cpu_freq:.0f} MHz\n")
        self.output.insert("end", f"• Температура: {cpu_temp}\n\n")

        # GPU
        try:
            gpus = GPUtil.getGPUs()
        except Exception:
            gpus = []

        if gpus:
            gpu = gpus[0]
            self.output.insert("end", "🎮 GPU\n")
            self.output.insert("end", f"• Назва: {gpu.name}\n")
            self.output.insert("end", f"• Завантаження: {gpu.load * 100:.1f}%\n")
            self.output.insert("end", f"• Температура: {gpu.temperature}°C\n\n")
        else:
            self.output.insert("end", "🎮 GPU\n")
            self.output.insert("end", "• Немає доступного GPU\n\n")

        # RAM
        ram = psutil.virtual_memory()
        ram_total = round(ram.total / (1024 ** 3), 2)
        ram_used = round(ram.used / (1024 ** 3), 2)

        self.output.insert("end", "🧠 RAM\n")
        self.output.insert("end", f"• Використано: {ram_used} GB\n")
        self.output.insert("end", f"• Загалом: {ram_total} GB\n")
        self.output.insert("end", f"• Завантаження: {ram.percent}%\n\n")

        self.output.configure(state="disabled")

        self.stats_label.config(
            text=f"❌ Останнє сканування: {self.last_scan}\n"
                 f"🟡 Кількість сканувань: {self.scan_count}\n"
                 f"✅ Виявлено загроз: {self.total_detections}"
        )

    # -------------------- Cleaning + Boost (об’єднана вкладка) --------------------

    def show_cleaning(self):
        self.clear_main()

        tk.Label(
            self.main_area,
            text=self.t("cleaning"),
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#2e2e2e"
        ).pack(pady=20)

        # Далі йдуть кнопки очищення

        tk.Button(
            self.main_area,
            text=self.t("kill_heavy"),
            command=self.kill_heavy_processes,
            bg="#343a40",
            fg="white",
            font=("Segoe UI", 12),
            relief="flat"
        ).pack(pady=5)

    def show_cleanup_tools(self):
        self.clear_main()

        self.content_area = tk.Frame(self.main_area, bg="#2e2e2e")
        self.content_area.pack(padx=40, pady=30, fill="both", expand=True)

        tk.Label(
            self.content_area,
            text="🧹 Очищення та оптимізація",
            fg="white",
            bg="#2e2e2e",
            font=("Segoe UI", 18, "bold"),
            anchor="w",
        ).pack(pady=(0, 20), anchor="w")

        btns = tk.Frame(self.content_area, bg="#2e2e2e")
        btns.pack(pady=10, fill="x")
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        actions = [
            (self.t("clean_temp"), self.clean_temp),
            (self.t("clean_cache"), self.clean_browsers_cache),
            (self.t("clean_logs"), self.clean_logs),
            (self.t("empty_recycle"), self.empty_recycle_bin),
            ("⚡ Завершити важкі процеси", self.run_kill_processes),
            (self.t("clean_summary"), self.show_clean_summary),
        ]

        for i, (label, func) in enumerate(actions):
            tk.Button(
                btns,
                text=label,
                command=func,
                bg="#343a40",
                fg="white",
                relief="flat",
                font=("Segoe UI", 12),
            ).grid(row=i // 2, column=i % 2, sticky="ew", padx=8, pady=6)

        self.clean_output = tk.Text(
            self.content_area,
            height=8,
            width=90,
            bg="#1e1e1e",
            fg="#d0f0ff",
            font=("Consolas", 11),
            relief="flat",
        )
        self.clean_output.pack(pady=10, fill="both", expand=True)

    def run_progress(self, steps=100, delay=20):
        """Animate progressbar without blocking GUI."""
        self.progress["value"] = 0
        self.progress["maximum"] = steps

        def step(i=0):
            if i <= steps:
                self.progress["value"] = i
                self.main_area.after(delay, step, i + 1)

        step()

    def clean_temp(self):
        self._log_clean("Починаю очистку тимчасових файлів...")
        freed = 0
        paths = [
            Path(os.environ.get("TEMP", "")),
            Path(os.environ.get("TMP", "")),
            Path(os.environ.get("WINDIR", "C:\\Windows")) / "Temp",
        ]
        for p in paths:
            if p.exists():
                freed += self._delete_tree(p)
        self._freed_bytes_session += freed
        self._log_clean(f"Готово. Звільнено: {human_size(freed)}")

    def clean_browsers_cache(self):
        self._log_clean("Очищаю кеш браузерів (Chrome/Edge)...")
        freed = 0
        user_profile = Path(os.environ.get("USERPROFILE", ""))

        for browser in ["Google\\Chrome", "Microsoft\\Edge"]:
            profiles_root = user_profile / "AppData" / "Local" / browser / "User Data"
            if profiles_root.exists():
                for profile in profiles_root.iterdir():
                    cache = profile / "Cache"
                    if cache.exists():
                        freed += self._delete_tree(cache)

        self._freed_bytes_session += freed
        self._log_clean(f"Готово. Звільнено: {human_size(freed)}")

    def clean_logs(self):
        self._log_clean("Очищаю системні логи (приклад: ProgramData\\Logs)...")
        freed = 0
        logs_root = Path(os.environ.get("ProgramData", "C:\\ProgramData")) / "Logs"
        if logs_root.exists():
            freed += self._delete_tree(logs_root)
        self._freed_bytes_session += freed
        self._log_clean(f"Готово. Звільнено: {human_size(freed)}")

    def empty_recycle_bin(self):
        self._log_clean("Очищаю кошик...")
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000007)
            self._log_clean("Кошик очищено.")
        except Exception as e:
            self._log_clean(f"Помилка очищення кошика: {e}")

    def show_clean_summary(self):
        self._log_clean(
            f"Підсумок: звільнено {human_size(self._freed_bytes_session)} за сесію"
        )

    def _delete_tree(self, path: Path) -> int:
        """Delete files in a tree and return total freed bytes."""
        total = 0
        for root, dirs, files in os.walk(path, topdown=False):
            for f in files:
                fp = Path(root) / f
                try:
                    total += fp.stat().st_size
                    fp.unlink(missing_ok=True)
                except Exception:
                    pass
            for d in dirs:
                dp = Path(root) / d
                try:
                    dp.rmdir()
                except Exception:
                    pass
        return total

    def _log_clean(self, text: str):
        self.clean_output.insert(tk.END, text + "\n")
        self.clean_output.see(tk.END)

    def run_kill_processes(self):
        killed = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):
            try:
                if (
                    proc.info["cpu_percent"] > 50
                    and proc.info["name"] not in ["System", "explorer.exe"]
                ):
                    proc.kill()
                    killed.append(proc.info["name"])
            except Exception:
                pass
        if killed:
            self._log_clean(f"🛑 Зупинено: {', '.join(killed)}")
        else:
            self._log_clean("✅ Немає важких процесів")

    # -------------------- Uninstaller --------------------

    def show_uninstaller(self):
        self.clear_main()

        self.content_area = tk.Frame(self.main_area, bg="#2e2e2e")
        self.content_area.pack(padx=40, pady=30, fill="both", expand=True)

        tk.Label(
            self.content_area,
            text=self.t("uninstall"),
            fg="white",
            bg="#2e2e2e",
            font=("Segoe UI", 18, "bold"),
            anchor="w",
        ).pack(pady=(0, 20), anchor="w")

        # Treeview з іконками (тільки якщо є)
        self.tree = ttk.Treeview(self.content_area, columns=("name"), show="tree")
        self.tree.pack(fill="both", expand=True)

        # Кеш іконок
        self.icons_cache = {}

        programs = self.get_installed_programs()

        for name, icon_path in programs:
            icon = self.extract_icon(icon_path)

            if icon:
                self.icons_cache[name] = icon
                self.tree.insert("", "end", text=name, image=icon)
            else:
                # без іконки — просто текст
                self.tree.insert("", "end", text=name)

        tk.Button(
            self.content_area,
            text="Видалити вибране",
            command=self.remove_selected_program,
            bg="#343a40",
            fg="white",
            relief="flat",
            font=("Segoe UI", 12),
        ).pack(pady=10)

        self.uninstall_output = tk.Label(
            self.content_area,
            text="",
            fg="lightgreen",
            bg="#2e2e2e",
            font=("Segoe UI", 12),
        )
        self.uninstall_output.pack(pady=5)


    def get_installed_programs(self):
        programs = []
        keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        for root, path in keys:
            try:
                with winreg.OpenKey(root, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                try:
                                    icon_path, _ = winreg.QueryValueEx(subkey, "DisplayIcon")
                                except Exception:
                                    icon_path = None
                                programs.append((name, icon_path))
                        except Exception:
                            continue
            except Exception:
                continue
        return sorted(programs, key=lambda x: x[0])


    def extract_icon(self, path, size=(24, 24)):
        try:
            if not path:
                return None

            if "," in path:
                path = path.split(",")[0]

            if not os.path.exists(path):
                return None

            large, small = ctypes.c_void_p(), ctypes.c_void_p()
            res = ctypes.windll.shell32.ExtractIconExW(path, 0, ctypes.byref(large), ctypes.byref(small), 1)

            if res > 0 and small:
                hicon = small.value
                ico = Image.frombytes("RGBA", (32, 32), ctypes.string_at(hicon, 32 * 32 * 4))
                ico = ico.resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(ico)

        except Exception:
            pass

        return None


    def remove_selected_program(self):
        selection = self.tree.selection()
        if selection:
            program_name = self.tree.item(selection[0], "text")
            self.uninstall_output.configure(text=f"✅ Видалено: {program_name}")

    # -------------------- Settings --------------------

    def show_settings(self):
        self.clear_main()

        self.content_area = tk.Frame(self.main_area, bg="#2e2e2e")
        self.content_area.pack(padx=40, pady=30, fill="both", expand=True)

        tk.Label(
            self.content_area,
            text=self.t("settings"),
            fg="white",
            bg="#2e2e2e",
            font=("Segoe UI", 18, "bold"),
            anchor="w",
        ).pack(pady=(0, 20), anchor="w")

        notebook = ttk.Notebook(self.content_area)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Тема
        theme_frame = tk.Frame(notebook, bg="#2e2e2e")
        notebook.add(theme_frame, text=self.t("theme_tab"))

        tk.Label(
            theme_frame,
            text=self.t("choose_theme"),
            fg="white",
            bg="#2e2e2e",
            font=("Segoe UI", 14),
        ).pack(pady=10)

        self.theme_var = tk.StringVar(value="darkly")
        for theme in self.style.theme_names():
            tk.Radiobutton(
                theme_frame,
                text=theme.capitalize(),
                variable=self.theme_var,
                value=theme,
                command=self.change_theme,
                bg="#2e2e2e",
                fg="white",
                selectcolor="#1e1e1e",
                font=("Segoe UI", 12),
                anchor="w",
            ).pack(fill="x", padx=30, pady=2)

        # Мова
        lang_frame = tk.Frame(notebook, bg="#2e2e2e")
        notebook.add(lang_frame, text=self.t("lang_tab"))

        tk.Label(
            lang_frame,
            text=self.t("choose_lang"),
            bg="#2e2e2e",
            fg="white",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(20, 10))

        btn_en = tk.Button(
            lang_frame,
            text="English",
            command=lambda: self.change_language("en"),
            bg="#343a40",
            fg="white",
            font=("Segoe UI", 12),
            relief="flat"
        )
        btn_en.pack(pady=5)

        btn_uk = tk.Button(
            lang_frame,
            text="Українська",
            command=lambda: self.change_language("uk"),
            bg="#343a40",
            fg="white",
            font=("Segoe UI", 12),
            relief="flat"
        )
        btn_uk.pack(pady=5)
        tk.Button(lang_frame, text="Polski", command=lambda: self.change_language("pl")).pack(pady=5)
        tk.Button(lang_frame, text="Deutsch", command=lambda: self.change_language("de")).pack(pady=5)

        # Інше
        other_frame = tk.Frame(notebook, bg="#2e2e2e")
        notebook.add(other_frame, text=self.t("other_tab"))

        tk.Checkbutton(
            other_frame,
            text=self.t("autostart"),
            variable=self.autostart_var,
            command=self.toggle_autostart,
            bg="#2e2e2e",
            fg="white",
            selectcolor="#1e1e1e",
            font=("Segoe UI", 12),
        ).pack(anchor="w", padx=30, pady=10)

    def change_theme(self):
        new_theme = self.theme_var.get()
        if new_theme in self.style.theme_names():
            try:
                self.style.theme_use(new_theme)
            except Exception:
                pass

    def change_language(self, lang):
        self.current_lang = lang
        self.build_sidebar()  # або онови весь інтерфейс


    # -------------------- Autostart --------------------

    def toggle_autostart(self):
        enabled = self.autostart_var.get()
        if winreg is None:
            messagebox.showwarning("Автозапуск", "winreg недоступний у вашому середовищі.")
            return
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE
            ) as reg:
                exe_path = str(Path(os.path.abspath(__file__)).resolve())
                if enabled:
                    winreg.SetValueEx(reg, "SystemCleanerApp", 0, winreg.REG_SZ, exe_path)
                else:
                    try:
                        winreg.DeleteValue(reg, "SystemCleanerApp")
                    except FileNotFoundError:
                        pass
        except Exception as e:
            print("Autostart error:", e)