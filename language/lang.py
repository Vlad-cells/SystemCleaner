# language/lang.py

languages = {
    "uk": {
        # Сайдбар
        "health": "Перевірка здоров’я",
        "clean": "Очищення та оптимізація",
        "boost": "Оптимізація",
        "uninstall": "Видалення програм",
        "settings": "Налаштування",

        # Вкладки
        "theme_tab": "🤡 Тема",
        "lang_tab": "🌐 Мова",
        "other_tab": "⚡ Інше",

        # Налаштування
        "choose_theme": "Оберіть стиль програми:",
        "choose_lang": "Оберіть мову інтерфейсу:",
        "autostart": "Автозапуск при старті Windows",

        # Кнопки
        "delete_selected": "Видалити вибране",
        "scan_btn": "Сканування системи",
        "cpu_btn": "CPU",
        "gpu_btn": "GPU",
        "kill_heavy": "Завершити важкі процеси",
        "cleaning": "Очищення",
        


        # Сканування
        "system_health": "Перевірка здоров’я системи",
        "last_scan": "Останнє сканування",
        "scan_count": "Кількість сканувань",
        "threats_found": "Виявлено загроз",
        

        # CPU
        "cpu": "CPU",
        "name": "Назва",
        "load": "Завантаження",
        "frequency": "Частота",
        "temperature": "Температура",

        # GPU
        "gpu": "GPU",

        # RAM
        "ram": "RAM",
        "used": "Використано",
        "total": "Загалом",

        # Очищення
        "clean_temp": "Очистити тимчасові файли",
        "clean_cache": "Очистити кеш браузерів",
        "clean_logs": "Очистити системні логи",
        "empty_recycle": "Очистити кошик",
        "clean_summary": "Порахувати підсумок",
    },

    "en": {
        # Sidebar
        "health": "Health Check",
        "clean": "Cleaning & Optimization",
        "boost": "Boost",
        "uninstall": "Uninstall Programs",
        "settings": "Settings",

        # Tabs
        "theme_tab": "🤡 Theme",
        "lang_tab": "🌐 Language",
        "other_tab": "⚡ Other",

        # Settings
        "choose_theme": "Choose program style:",
        "choose_lang": "Choose interface language:",
        "autostart": "Autostart with Windows",
        

        # Buttons
        "delete_selected": "Delete Selected",
        "scan_btn": "Scan System",
        "cpu_btn": "CPU",
        "gpu_btn": "GPU",
        "kill_heavy": "Terminate Heavy Processes",
        "cleaning": "Cleaning",


        # Scan
        "system_health": "System Health Check",
        "last_scan": "Last Scan",
        "scan_count": "Scan Count",
        "threats_found": "Threats Found",

        # CPU
        "cpu": "CPU",
        "name": "Name",
        "load": "Load",
        "frequency": "Frequency",
        "temperature": "Temperature",

        # GPU
        "gpu": "GPU",

        # RAM
        "ram": "RAM",
        "used": "Used",
        "total": "Total",

        # Cleaning
        "clean_temp": "Clean Temporary Files",
        "clean_cache": "Clean Browser Cache",
        "clean_logs": "Clean System Logs",
        "empty_recycle": "Empty Recycle Bin",
        "clean_summary": "Calculate Summary",
    },

    "pl": {
        "health": "Sprawdzenie stanu",
        "clean": "Czyszczenie i optymalizacja",
        "uninstall": "Odinstaluj programy",
        "settings": "Ustawienia",

        "theme_tab": "🤡 Motyw",
        "lang_tab": "🌐 Język",
        "other_tab": "⚡ Inne",

        "choose_theme": "Wybierz styl programu:",
        "choose_lang": "Wybierz język interfejsu:",
        "autostart": "Autostart z Windows",

        "delete_selected": "Usuń zaznaczone",
        "scan_btn": "Skanuj system",
        "cpu_btn": "CPU",
        "gpu_btn": "GPU",

        "system_health": "Kontrola stanu systemu",
        "last_scan": "Ostatnie skanowanie",
        "scan_count": "Liczba skanowań",
        "threats_found": "Znalezione zagrożenia",

        "cpu": "CPU",
        "name": "Nazwa",
        "load": "Obciążenie",
        "frequency": "Częstotliwość",
        "temperature": "Temperatura",

        "gpu": "GPU",

        "ram": "RAM",
        "used": "Użyte",
        "total": "Razem",

        "clean_temp": "Wyczyść pliki tymczasowe",
        "clean_logs": "Wyczyść logi systemowe",
        "clean_cache": "Wyczyść pamięć podręczną przeglądarki",
        "empty_recycle": "Opróżnij kosz",
        "clean_summary": "Oblicz podsumowanie",
        "kill_heavy": "Zakończ ciężkie procesy",
        "cleaning": "Czyszczenie",
        "clean_boost": "Czyszczenie i optymalizacja"
    },

    "de": {
        "health": "Systemprüfung",
        "clean": "Reinigung und Optimierung",
        "uninstall": "Programme deinstallieren",
        "settings": "Einstellungen",

        "theme_tab": "🤡 Thema",
        "lang_tab": "🌐 Sprache",
        "other_tab": "⚡ Sonstiges",

        "choose_theme": "Programmstil auswählen:",
        "choose_lang": "Sprache auswählen:",
        "autostart": "Autostart mit Windows",

        "delete_selected": "Ausgewählte löschen",
        "scan_btn": "System scannen",
        "cpu_btn": "CPU",
        "gpu_btn": "GPU",

        "system_health": "Systemzustand prüfen",
        "last_scan": "Letzter Scan",
        "scan_count": "Scan-Anzahl",
        "threats_found": "Gefundene Bedrohungen",

        "cpu": "CPU",
        "name": "Name",
        "load": "Auslastung",
        "frequency": "Frequenz",
        "temperature": "Temperatur",

        "gpu": "GPU",

        "ram": "RAM",
        "used": "Verwendet",
        "total": "Gesamt",

        "clean_temp": "Temporäre Dateien löschen",
        "clean_logs": "Systemprotokolle löschen",
        "clean_cache": "Browser-Cache löschen",
        "empty_recycle": "Papierkorb leeren",
        "clean_summary": "Zusammenfassung berechnen",
        "kill_heavy": "Schwere Prozesse beenden",
        "cleaning": "Reinigung",
        "clean_boost": "Reinigung und Optimierung"
    }
}

def t(key: str, lang: str = "uk") -> str:
    """Повертає переклад за ключем."""
    return languages.get(lang, {}).get(key, key)