# Requirements:
# pip install PyQt5 psutil pyqtgraph

import sys
import os
import time
import platform
import psutil
import webbrowser
import json

from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QGroupBox, QGridLayout, QMessageBox, QFileDialog, QLineEdit, QInputDialog
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon

import pyqtgraph as pg

CONFIG_FILE = "booster_config.json"

LANGUAGES = {
    "EN": {
        "performance": "Performance Monitoring",
        "cpu": "CPU Usage:",
        "mem": "Memory Usage:",
        "disk": "Disk Usage:",
        "temp": "CPU Temp:",
        "start_monitor": "Start Monitoring",
        "stop_monitor": "Stop Monitoring",
        "clean_ram": "Clean RAM",
        "open_startup": "Open Startup Folder",
        "drivers_update": "Driver Updater",
        "game_launcher": "Game Launcher",
        "add_game": "Add Game",
        "remove_game": "Remove Game",
        "run_game": "Run Selected Game",
        "graphics": "Graphics Settings",
        "graphics_quality": "Graphics Quality",
        "apply_settings": "Apply Settings",
        "theme": "Theme",
        "dark": "Dark",
        "light": "Light",
        "auto_recommend": "Recommend Best Settings",
        "github": "My GitHub",
        "about": "About",
        "about_text": "PerformanceBoosterPC - GUI Edition\nKhalidaldawish & Copilot\n2025\n",
        "help": "Help",
        "help_text": "• Performance Monitoring: Shows CPU, RAM, Disk usage, and temperature.\n"
                     "• Clean RAM: Tries to free unused memory.\n"
                     "• Open Startup Folder: Manage programs that start with Windows.\n"
                     "• Driver Updater: Opens a driver update tool website.\n"
                     "• Game Launcher: Add and launch your favorite games easily.\n"
                     "• Graphics: Set your preferred graphics quality.\n"
                     "• Auto Recommend: Suggests the best settings for your hardware.\n"
                     "• Theme: Switch between Light and Dark modes.\n"
                     "• All rights reserved for Khalidaldawish.",
        "design_note": "Modern gaming-inspired design 🎨✨",
        "all_rights": "All Rights Reserved 2025 - Khalidaldawish",
        "language": "Language",
        "arabic": "Arabic",
        "english": "English",
        "add_success": "Game added successfully.",
        "remove_success": "Game removed.",
        "select_game": "Please select a game.",
        "no_game": "No game selected.",
        "recommend_msg": "For your system, we recommend graphics quality: ",
        "ram_cleaned": "RAM cleaned. Closed processes: ",
        "theme_changed": "Theme changed.",
        "open_github": "Opening GitHub page...",
        "startup_hint": "You can remove or add startup programs in this folder.",
        "disk_total": "Total",
        "disk_used": "Used",
        "disk_free": "Free"
    },
    "AR": {
        "performance": "مراقبة الأداء",
        "cpu": "معدل استهلاك المعالج:",
        "mem": "معدل استهلاك الذاكرة:",
        "disk": "استخدام القرص:",
        "temp": "درجة حرارة المعالج:",
        "start_monitor": "ابدأ المراقبة",
        "stop_monitor": "أوقف المراقبة",
        "clean_ram": "تنظيف الرام",
        "open_startup": "مجلد بدء التشغيل",
        "drivers_update": "تحديث التعريفات",
        "game_launcher": "مشغل الألعاب",
        "add_game": "إضافة لعبة",
        "remove_game": "حذف لعبة",
        "run_game": "تشغيل اللعبة المحددة",
        "graphics": "إعدادات الرسوميات",
        "graphics_quality": "جودة الرسوميات",
        "apply_settings": "تطبيق الإعدادات",
        "theme": "الثيم",
        "dark": "داكن",
        "light": "فاتح",
        "auto_recommend": "توصية تلقائية",
        "github": "صفحتي على GitHub",
        "about": "عن البرنامج",
        "about_text": "PerformanceBoosterPC - واجهة رسومية\nKhalidaldawish & Copilot\n2025\n",
        "help": "مساعدة",
        "help_text": "• مراقبة الأداء: عرض استهلاك المعالج والذاكرة والقرص ودرجة الحرارة.\n"
                     "• تنظيف الرام: محاولة تحرير الذاكرة غير المستخدمة.\n"
                     "• مجلد بدء التشغيل: إدارة البرامج التي تبدأ مع ويندوز.\n"
                     "• تحديث التعريفات: يفتح موقع أداة تحديث التعريفات.\n"
                     "• مشغل الألعاب: أضف ألعابك المفضلة وشغلها بسهولة.\n"
                     "• الرسوميات: اختر جودة الرسوميات المناسبة.\n"
                     "• التوصية التلقائية: يقترح أفضل إعدادات لجهازك.\n"
                     "• الثيم: التبديل بين الوضع الفاتح والداكن.\n"
                     "• جميع الحقوق محفوظة لخالد الدويش.",
        "design_note": "تصميم عصري مستوحى من الألعاب 🎨✨",
        "all_rights": "جميع الحقوق محفوظة 2025 - خالد الدويش",
        "language": "اللغة",
        "arabic": "العربية",
        "english": "الإنجليزية",
        "add_success": "تم إضافة اللعبة بنجاح.",
        "remove_success": "تم حذف اللعبة.",
        "select_game": "يرجى تحديد لعبة.",
        "no_game": "لم يتم تحديد أي لعبة.",
        "recommend_msg": "نوصي لجهازك بجودة رسوميات: ",
        "ram_cleaned": "تم تنظيف الرام. عدد العمليات المغلقة: ",
        "theme_changed": "تم تغيير الثيم.",
        "open_github": "فتح صفحة GitHub...",
        "startup_hint": "يمكنك إضافة أو إزالة برامج بدء التشغيل من هذا المجلد.",
        "disk_total": "الإجمالي",
        "disk_used": "المستخدم",
        "disk_free": "المتاح"
    }
}

def get_cpu_temp():
    """
    Returns CPU temperature (Celsius) if available (Windows only), else None.
    """
    try:
        import wmi
        w = wmi.WMI(namespace="root\\wmi")
        temps = w.MSAcpi_ThermalZoneTemperature()
        if temps:
            return int(temps[0].CurrentTemperature / 10 - 273.15)
    except Exception:
        pass
    return None

def get_disk_info():
    usage = psutil.disk_usage('/')
    return usage.total//(1024**3), usage.used//(1024**3), usage.free//(1024**3)

class GameList:
    def __init__(self, file="gamelist.json"):
        self.file = file
        self.games = []
        self.load()
    def load(self):
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                self.games = json.load(f)
        except Exception:
            self.games = []
    def save(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.games, f, indent=2, ensure_ascii=False)
    def add(self, name, path):
        self.games.append({"name": name, "path": path})
        self.save()
    def remove(self, idx):
        if 0 <= idx < len(self.games):
            del self.games[idx]
            self.save()

class PerformanceBoosterPC(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Performance Booster PC")
        self.setWindowIcon(QIcon())
        self.resize(800, 600)
        self.username = os.getlogin() if hasattr(os, "getlogin") else "Player1"
        self.lang = self.load_config().get("lang", "EN")
        self.theme = self.load_config().get("theme", "dark")
        self.set_theme(self.theme)
        self.gamelist = GameList()
        self.performance_log = {"cpu": [], "mem": [], "disk": []}
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_performance_ui)
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_performance_plot)
        self.plot_timer.start(1500)

    def init_ui(self):
        main_layout = QVBoxLayout()
        # Language & Theme Switcher
        top_layout = QHBoxLayout()
        self.lang_btn_en = QPushButton(LANGUAGES["EN"]["english"])
        self.lang_btn_ar = QPushButton(LANGUAGES["EN"]["arabic"])
        self.lang_btn_en.clicked.connect(lambda: self.set_language("EN"))
        self.lang_btn_ar.clicked.connect(lambda: self.set_language("AR"))
        self.theme_btn = QPushButton(LANGUAGES[self.lang]["theme"])
        self.theme_btn.clicked.connect(self.toggle_theme)
        top_layout.addWidget(QLabel(LANGUAGES[self.lang]["language"] + " / " + LANGUAGES["AR"]["language"]))
        top_layout.addWidget(self.lang_btn_en)
        top_layout.addWidget(self.lang_btn_ar)
        top_layout.addWidget(self.theme_btn)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)

        # Tabs
        self.tabs = QTabWidget()
        self.tab_performance = QWidget()
        self.tab_graphics = QWidget()
        self.tab_game_launcher = QWidget()
        self.tabs.addTab(self.tab_performance, LANGUAGES[self.lang]["performance"])
        self.tabs.addTab(self.tab_graphics, LANGUAGES[self.lang]["graphics"])
        self.tabs.addTab(self.tab_game_launcher, LANGUAGES[self.lang]["game_launcher"])
        main_layout.addWidget(self.tabs)

        # --- Performance Tab ---
        perf_layout = QVBoxLayout()
        perf_group = QGroupBox(LANGUAGES[self.lang]["performance"])
        perf_grid = QGridLayout()
        self.cpu_label = QLabel(LANGUAGES[self.lang]["cpu"])
        self.cpu_val = QLabel("-- %")
        self.mem_label = QLabel(LANGUAGES[self.lang]["mem"])
        self.mem_val = QLabel("-- %")
        self.disk_label = QLabel(LANGUAGES[self.lang]["disk"])
        self.disk_val = QLabel("-- %")
        self.temp_label = QLabel(LANGUAGES[self.lang]["temp"])
        self.temp_val = QLabel("-- °C")
        self.btn_start_monitor = QPushButton(LANGUAGES[self.lang]["start_monitor"])
        self.btn_stop_monitor = QPushButton(LANGUAGES[self.lang]["stop_monitor"])
        self.btn_clean_ram = QPushButton(LANGUAGES[self.lang]["clean_ram"])
        self.btn_open_startup = QPushButton(LANGUAGES[self.lang]["open_startup"])
        self.btn_drivers_update = QPushButton(LANGUAGES[self.lang]["drivers_update"])
        self.btn_start_monitor.clicked.connect(self.start_monitor)
        self.btn_stop_monitor.clicked.connect(self.stop_monitor)
        self.btn_clean_ram.clicked.connect(self.clean_ram)
        self.btn_open_startup.clicked.connect(self.open_startup_folder)
        self.btn_drivers_update.clicked.connect(self.open_drivers_update)
        # Disk info details
        self.disk_info_label = QLabel("")
        # Layout
        perf_grid.addWidget(self.cpu_label, 0, 0); perf_grid.addWidget(self.cpu_val, 0, 1)
        perf_grid.addWidget(self.mem_label, 1, 0); perf_grid.addWidget(self.mem_val, 1, 1)
        perf_grid.addWidget(self.disk_label, 2, 0); perf_grid.addWidget(self.disk_val, 2, 1)
        perf_grid.addWidget(self.temp_label, 3, 0); perf_grid.addWidget(self.temp_val, 3, 1)
        perf_grid.addWidget(self.btn_start_monitor, 4, 0)
        perf_grid.addWidget(self.btn_stop_monitor, 4, 1)
        perf_grid.addWidget(self.btn_clean_ram, 5, 0)
        perf_grid.addWidget(self.btn_open_startup, 5, 1)
        perf_grid.addWidget(self.btn_drivers_update, 6, 0, 1, 2)
        perf_grid.addWidget(self.disk_info_label, 7, 0, 1, 2)
        perf_group.setLayout(perf_grid)
        perf_layout.addWidget(perf_group)
        # Performance Chart
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setYRange(0, 100)
        self.plot_widget.setBackground("#282828" if self.theme == "dark" else "#f6f6f6")
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setLabel('left', "Usage %")
        self.plot_widget.setLabel('bottom', "Time (s)")
        self.cpu_curve = self.plot_widget.plot(pen=pg.mkPen(color=(255, 120, 120), width=2), name="CPU")
        self.mem_curve = self.plot_widget.plot(pen=pg.mkPen(color=(120, 255, 120), width=2), name="RAM")
        self.disk_curve = self.plot_widget.plot(pen=pg.mkPen(color=(120, 120, 255), width=2), name="Disk")
        perf_layout.addWidget(self.plot_widget)
        self.tab_performance.setLayout(perf_layout)

        # --- Graphics Tab ---
        graphics_layout = QVBoxLayout()
        graphics_group = QGroupBox(LANGUAGES[self.lang]["graphics"])
        graphics_grid = QGridLayout()
        self.graphics_quality_label = QLabel(LANGUAGES[self.lang]["graphics_quality"])
        self.graphics_combo = QComboBox()
        self.graphics_combo.addItems(["low", "medium", "high", "ultra"])
        self.graphics_combo.setCurrentText("high")
        self.btn_apply_graphics = QPushButton(LANGUAGES[self.lang]["apply_settings"])
        self.btn_apply_graphics.clicked.connect(self.apply_graphics)
        self.btn_auto_recommend = QPushButton(LANGUAGES[self.lang]["auto_recommend"])
        self.btn_auto_recommend.clicked.connect(self.recommend_graphics)
        graphics_grid.addWidget(self.graphics_quality_label, 0, 0)
        graphics_grid.addWidget(self.graphics_combo, 0, 1)
        graphics_grid.addWidget(self.btn_apply_graphics, 1, 0, 1, 2)
        graphics_grid.addWidget(self.btn_auto_recommend, 2, 0, 1, 2)
        graphics_group.setLayout(graphics_grid)
        graphics_layout.addWidget(graphics_group)
        self.tab_graphics.setLayout(graphics_layout)

        # --- Game Launcher Tab ---
        game_layout = QVBoxLayout()
        game_group = QGroupBox(LANGUAGES[self.lang]["game_launcher"])
        game_grid = QGridLayout()
        self.game_list_combo = QComboBox()
        self.update_game_list()
        self.btn_add_game = QPushButton(LANGUAGES[self.lang]["add_game"])
        self.btn_remove_game = QPushButton(LANGUAGES[self.lang]["remove_game"])
        self.btn_run_game = QPushButton(LANGUAGES[self.lang]["run_game"])
        self.btn_add_game.clicked.connect(self.add_game)
        self.btn_remove_game.clicked.connect(self.remove_game)
        self.btn_run_game.clicked.connect(self.run_game)
        game_grid.addWidget(self.game_list_combo, 0, 0, 1, 3)
        game_grid.addWidget(self.btn_add_game, 1, 0)
        game_grid.addWidget(self.btn_remove_game, 1, 1)
        game_grid.addWidget(self.btn_run_game, 1, 2)
        game_group.setLayout(game_grid)
        game_layout.addWidget(game_group)
        self.tab_game_launcher.setLayout(game_layout)

        # --- Footer (About, Help, GitHub) ---
        bottom_layout = QHBoxLayout()
        self.about_btn = QPushButton(LANGUAGES[self.lang]["about"])
        self.about_btn.clicked.connect(self.show_about)
        self.help_btn = QPushButton(LANGUAGES[self.lang]["help"])
        self.help_btn.clicked.connect(self.show_help)
        self.github_btn = QPushButton(LANGUAGES[self.lang]["github"])
        self.github_btn.clicked.connect(lambda: self.open_github())
        self.design_label = QLabel(LANGUAGES[self.lang]["design_note"])
        self.rights_label = QLabel(LANGUAGES[self.lang]["all_rights"])
        bottom_layout.addWidget(self.about_btn)
        bottom_layout.addWidget(self.help_btn)
        bottom_layout.addWidget(self.github_btn)
        bottom_layout.addWidget(self.design_label)
        bottom_layout.addWidget(self.rights_label)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    # ----------------- Features -----------------
    def start_monitor(self):
        if not self.timer.isActive():
            self.timer.start(1000)

    def stop_monitor(self):
        if self.timer.isActive():
            self.timer.stop()

    def update_performance_ui(self):
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        self.cpu_val.setText(f"{cpu:.1f} %")
        self.mem_val.setText(f"{mem:.1f} %")
        self.disk_val.setText(f"{disk:.1f} %")
        # Disk info
        total, used, free = get_disk_info()
        self.disk_info_label.setText(
            f'{LANGUAGES[self.lang]["disk_total"]}: {total} GB | {LANGUAGES[self.lang]["disk_used"]}: {used} GB | {LANGUAGES[self.lang]["disk_free"]}: {free} GB')
        # CPU Temp
        temp = get_cpu_temp()
        self.temp_val.setText(f"{temp} °C" if temp else "-- °C")
        # Save for plotting
        self.performance_log["cpu"].append(cpu)
        self.performance_log["mem"].append(mem)
        self.performance_log["disk"].append(disk)
        max_len = 60  # last 60 seconds
        for k in self.performance_log:
            if len(self.performance_log[k]) > max_len:
                self.performance_log[k] = self.performance_log[k][-max_len:]

    def update_performance_plot(self):
        x = list(range(len(self.performance_log["cpu"])))
        self.cpu_curve.setData(x, self.performance_log["cpu"])
        self.mem_curve.setData(x, self.performance_log["mem"])
        self.disk_curve.setData(x, self.performance_log["disk"])

    def clean_ram(self):
        closed = 0
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                if proc.info['memory_info'].rss < 100*1024*1024 and proc.info['name'] not in ('explorer.exe', 'python.exe', 'System'):
                    os.kill(proc.info['pid'], 9)
                    closed += 1
            except Exception:
                pass
        QMessageBox.information(self, LANGUAGES[self.lang]["clean_ram"],
                                f"{LANGUAGES[self.lang]['ram_cleaned']}{closed}")

    def open_startup_folder(self):
        try:
            if sys.platform.startswith('win'):
                os.startfile(os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup'))
                QMessageBox.information(self, LANGUAGES[self.lang]["open_startup"], LANGUAGES[self.lang]["startup_hint"])
            else:
                QMessageBox.information(self, LANGUAGES[self.lang]["open_startup"], "Only available on Windows.")
        except Exception as e:
            QMessageBox.warning(self, LANGUAGES[self.lang]["open_startup"], str(e))

    def open_drivers_update(self):
        webbrowser.open("https://www.iobit.com/en/driver-booster.php")

    # ---------- Game Launcher ----------
    def update_game_list(self):
        self.game_list_combo.clear()
        for g in self.gamelist.games:
            self.game_list_combo.addItem(g["name"])

    def add_game(self):
        path, _ = QFileDialog.getOpenFileName(self, LANGUAGES[self.lang]["add_game"], "", "Executables (*.exe);;All Files (*)")
        if path:
            name, ok = QInputDialog.getText(self, LANGUAGES[self.lang]["add_game"], "Game name:")
            if ok and name.strip():
                self.gamelist.add(name.strip(), path)
                self.update_game_list()
                QMessageBox.information(self, LANGUAGES[self.lang]["add_game"], LANGUAGES[self.lang]["add_success"])

    def remove_game(self):
        idx = self.game_list_combo.currentIndex()
        if idx >= 0:
            self.gamelist.remove(idx)
            self.update_game_list()
            QMessageBox.information(self, LANGUAGES[self.lang]["remove_game"], LANGUAGES[self.lang]["remove_success"])
        else:
            QMessageBox.warning(self, LANGUAGES[self.lang]["remove_game"], LANGUAGES[self.lang]["select_game"])

    def run_game(self):
        idx = self.game_list_combo.currentIndex()
        if idx >= 0 and idx < len(self.gamelist.games):
            path = self.gamelist.games[idx]["path"]
            try:
                os.startfile(path)
            except Exception as e:
                QMessageBox.warning(self, LANGUAGES[self.lang]["run_game"], str(e))
        else:
            QMessageBox.warning(self, LANGUAGES[self.lang]["run_game"], LANGUAGES[self.lang]["no_game"])

    # --------- Graphics ---------------
    def apply_graphics(self):
        quality = self.graphics_combo.currentText()
        QMessageBox.information(self, LANGUAGES[self.lang]["apply_settings"], f"{LANGUAGES[self.lang]['apply_settings']} - {quality}")

    def recommend_graphics(self):
        ram = psutil.virtual_memory().total // (1024 ** 3)
        cpu_cores = psutil.cpu_count(logical=False)
        if ram < 6 or cpu_cores <= 2:
            rec = "low"
        elif ram < 8 or cpu_cores <= 4:
            rec = "medium"
        elif ram < 12:
            rec = "high"
        else:
            rec = "ultra"
        self.graphics_combo.setCurrentText(rec)
        QMessageBox.information(self, LANGUAGES[self.lang]["auto_recommend"],
                                f"{LANGUAGES[self.lang]['recommend_msg']}{rec}")

    # ---------- Themes ---------------
    def set_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet("""
                QWidget { background-color: #222; color: #EEE; }
                QPushButton { background-color: #444; color: #FFF; border-radius: 6px; padding: 6px; }
                QPushButton:hover { background-color: #666; }
                QGroupBox { border: 2px solid #555; border-radius: 8px; margin-top: 10px;}
                QTabWidget::pane { border: 1px solid #555; }
                QTabBar::tab { background: #333; color: #EEE; padding: 6px; border-radius: 4px; }
                QTabBar::tab:selected { background: #222; }
                QLabel { color: #EEE; }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: #f6f6f6; color: #222; }
                QPushButton { background-color: #e0e0e0; color: #222; border-radius: 6px; padding: 6px; }
                QPushButton:hover { background-color: #dadada; }
                QGroupBox { border: 2px solid #aaa; border-radius: 8px; margin-top: 10px;}
                QTabWidget::pane { border: 1px solid #aaa; }
                QTabBar::tab { background: #fff; color: #222; padding: 6px; border-radius: 4px; }
                QTabBar::tab:selected { background: #f6f6f6; }
                QLabel { color: #222; }
            """)
        self.theme = theme
        self.save_config()
        if hasattr(self, "plot_widget"):
            self.plot_widget.setBackground("#282828" if theme == "dark" else "#f6f6f6")

    def toggle_theme(self):
        self.set_theme("light" if self.theme == "dark" else "dark")
        QMessageBox.information(self, LANGUAGES[self.lang]["theme"], LANGUAGES[self.lang]["theme_changed"])

    # ----------- Language ------------
    def set_language(self, lang):
        self.lang = lang
        self.save_config()
        # update all UI labels
        self.tabs.setTabText(0, LANGUAGES[lang]["performance"])
        self.tabs.setTabText(1, LANGUAGES[lang]["graphics"])
        self.tabs.setTabText(2, LANGUAGES[lang]["game_launcher"])
        self.cpu_label.setText(LANGUAGES[lang]["cpu"])
        self.mem_label.setText(LANGUAGES[lang]["mem"])
        self.disk_label.setText(LANGUAGES[lang]["disk"])
        self.temp_label.setText(LANGUAGES[lang]["temp"])
        self.btn_start_monitor.setText(LANGUAGES[lang]["start_monitor"])
        self.btn_stop_monitor.setText(LANGUAGES[lang]["stop_monitor"])
        self.btn_clean_ram.setText(LANGUAGES[lang]["clean_ram"])
        self.btn_open_startup.setText(LANGUAGES[lang]["open_startup"])
        self.btn_drivers_update.setText(LANGUAGES[lang]["drivers_update"])
        self.disk_info_label.setText("")
        self.graphics_quality_label.setText(LANGUAGES[lang]["graphics_quality"])
        self.btn_apply_graphics.setText(LANGUAGES[lang]["apply_settings"])
        self.btn_auto_recommend.setText(LANGUAGES[lang]["auto_recommend"])
        self.about_btn.setText(LANGUAGES[lang]["about"])
        self.help_btn.setText(LANGUAGES[lang]["help"])
        self.github_btn.setText(LANGUAGES[lang]["github"])
        self.design_label.setText(LANGUAGES[lang]["design_note"])
        self.rights_label.setText(LANGUAGES[lang]["all_rights"])
        self.lang_btn_en.setText(LANGUAGES[lang]["english"])
        self.lang_btn_ar.setText(LANGUAGES[lang]["arabic"])
        self.theme_btn.setText(LANGUAGES[lang]["theme"])
        self.tab_game_launcher.setTitle = LANGUAGES[lang]["game_launcher"]
        self.btn_add_game.setText(LANGUAGES[lang]["add_game"])
        self.btn_remove_game.setText(LANGUAGES[lang]["remove_game"])
        self.btn_run_game.setText(LANGUAGES[lang]["run_game"])

    # ----------- About, Help, GitHub -------------
    def show_about(self):
        QMessageBox.information(self, LANGUAGES[self.lang]["about"], LANGUAGES[self.lang]["about_text"])

    def show_help(self):
        QMessageBox.information(self, LANGUAGES[self.lang]["help"], LANGUAGES[self.lang]["help_text"])

    def open_github(self):
        webbrowser.open("https://github.com/Khalidaldawish")
        QMessageBox.information(self, LANGUAGES[self.lang]["github"], LANGUAGES[self.lang]["open_github"])

    # ----------- Config --------------
    def save_config(self):
        config = {"lang": self.lang, "theme": self.theme}
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f)
        except Exception:
            pass

    def load_config(self):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PerformanceBoosterPC()
    win.show()
    sys.exit(app.exec_())