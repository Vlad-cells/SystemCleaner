import tkinter as tk
from tkinter import ttk

class CleanerGUI:
    def __init__(self, root):
        root.title("System Cleaner")
        root.geometry("800x500")
        root.configure(bg="#1e1e1e")

        # Бокове меню
        sidebar = tk.Frame(root, bg="#2e2e2e", width=200)
        sidebar.pack(side="left", fill="y")

        buttons = ["🧠 Система", "🧹 Очищення", "🚀 Оптимізація", "🧼 Видалення програм"]
        for b in buttons:
            tk.Button(sidebar, text=b, bg="#2e2e2e", fg="white", relief="flat").pack(fill="x", pady=5)

        # Основна панель
        main_area = tk.Frame(root, bg="#1e1e1e")
        main_area.pack(side="right", expand=True, fill="both")

        tk.Label(main_area, text="Сканування...", fg="white", bg="#1e1e1e", font=("Arial", 16)).pack(pady=20)

        # Прогрес-бар
        self.progress = ttk.Progressbar(main_area, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)
        self.progress["value"] = 70  # приклад, 70%

if __name__ == "__main__":
    root = tk.Tk()
    app = CleanerGUI(root)
    root.mainloop()