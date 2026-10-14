import json
import os
from datetime import datetime, timezone, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTabWidget, QLabel, QGridLayout, QTextEdit,
                             QComboBox, QCalendarWidget)
from PyQt5.QtCore import Qt, QTimer

class EditableMealCard(QTextEdit):
    """Clase personalizada para las cajas de comida editables"""
    def __init__(self, style_sheet):
        super().__init__()
        self.setStyleSheet(style_sheet)
        self.setPlaceholderText("Escribe un plato aquí...")
        # Deshabilitamos la barra de desplazamiento para que parezca una caja estática
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
    def focusOutEvent(self, event):
        """Este evento se dispara cuando haces clic fuera de la caja"""
        super().focusOutEvent(event)
        self.clearFocus() # Quita el cursor parpadeante

class MealApp(QMainWindow):
    
    class DashboardTab(QWidget):
        """Pestaña 1: Resumen del día"""
        def __init__(self, main_app):
            super().__init__()
            self.main_app = main_app
            self.meal_cards = [] # Guardaremos las 4 tarjetas aquí para modificarlas
            
            layout = QVBoxLayout(self)
            
            title = QLabel("Dashboard del Día")
            title.setStyleSheet("font-size: 28px; font-weight: bold; color: rgb(34, 197, 94);")
            layout.addWidget(title)
            
            # Selector de día para el dashboard
            selector_layout = QHBoxLayout()
            selector_label = QLabel("Día asignado al Dashboard:")
            selector_label.setStyleSheet("font-size: 18px; font-weight: bold;")
            
            self.day_selector = QComboBox()
            self.day_selector.addItems(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
            self.day_selector.setStyleSheet("""
                QComboBox {
                    font-size: 18px; padding: 5px; background: white;
                    border: 2px solid rgb(200, 200, 200); border-radius: 5px;
                }
            """)
            
            self.day_selector.currentTextChanged.connect(self.main_app.update_dashboard_from_selector)
            
            selector_layout.addWidget(selector_label)
            selector_layout.addWidget(self.day_selector)
            selector_layout.addStretch()
            layout.addLayout(selector_layout)
            
            meals_layout = QHBoxLayout()
            
            dashboard_style = """
                QTextEdit {
                    background-color: rgb(255, 255, 255);
                    border-radius: 15px;
                    border: 2px solid rgb(34, 197, 94);
                    padding: 10px;
                    font-size: 20px;
                }
                QTextEdit:focus {
                    border: 3px solid rgb(34, 197, 94);
                }
            """
            
            for _ in range(4):
                meal_card = EditableMealCard(dashboard_style)
                meal_card.setFixedSize(180, 250)
                meal_card.textChanged.connect(self.main_app.on_dashboard_text_changed)
                
                self.meal_cards.append(meal_card)
                meals_layout.addWidget(meal_card)
                
            layout.addLayout(meals_layout)
            layout.addStretch()

    class PlannerTab(QWidget):
        """Pestaña 2: Planificador semanal"""
        def __init__(self, main_app):
            super().__init__()
            self.main_app = main_app
            self.meal_cards = {} # Diccionario para guardar las tarjetas por día
            
            layout = QVBoxLayout(self)
            
            title = QLabel("Planificador Semanal")
            title.setStyleSheet("font-size: 28px; font-weight: bold; color: rgb(249, 115, 22);")
            layout.addWidget(title)
            
            grid = QGridLayout()
            grid.setSpacing(12)
            
            days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            
            planner_style = """
                QTextEdit {
                    background-color: rgb(255, 255, 255);
                    border-radius: 8px;
                    border: 2px dashed rgb(200, 200, 200);
                    padding: 5px;
                    font-size: 18px;
                }
                QTextEdit:focus {
                    border: 2px solid rgb(249, 115, 22);
                }
            """
            
            for col_idx, day in enumerate(days):
                self.meal_cards[day] = []
                
                header = QLabel(day)
                header.setAlignment(Qt.AlignCenter)
                header.setStyleSheet("font-weight: bold; font-size: 18px;")
                grid.addWidget(header, 0, col_idx)
                
                for row_idx in range(1, 5):
                    slot = EditableMealCard(planner_style)
                    slot.setMinimumHeight(100)
                    
                    slot.textChanged.connect(lambda d=day, r=row_idx-1: self.main_app.on_planner_text_changed(d, r))
                    
                    self.meal_cards[day].append(slot)
                    grid.addWidget(slot, row_idx, col_idx)
                    
            layout.addLayout(grid)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("App de Organización de Comidas")
        self.resize(1000, 700)
        
        self.load_data()
        
        self.setStyleSheet("background-color: rgb(249, 250, 251); color: rgb(30, 41, 59); font-size: 16px;")
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgb(220, 220, 220);
                background: rgb(249, 250, 251);
                border-radius: 8px;
            }
            QTabBar::tab {
                background: rgb(220, 220, 220);
                padding: 12px 25px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                font-size: 16px;
            }
            QTabBar::tab:selected {
                background: rgb(30, 41, 59);
                color: rgb(255, 255, 255);
            }
        """)
        
        self.tab_dashboard = self.DashboardTab(self)
        self.tab_planner = self.PlannerTab(self)
        
        self.tabs.addTab(self.tab_dashboard, "Dashboard")
        self.tabs.addTab(self.tab_planner, "Planificador")
        
        self.main_layout.addWidget(self.tabs)
        
        self.calendar = QCalendarWidget()
        self.calendar.setMaximumHeight(200)
        self.calendar.setMaximumWidth(350)
        self.calendar.setGridVisible(True)
        self.calendar.setStyleSheet("font-size: 14px; background-color: white; border-radius: 5px;")
        self.calendar.selectionChanged.connect(self.sync_calendar_to_day)
        
        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.clock_label.setStyleSheet("font-size: 16px; font-weight: bold; color: rgb(100, 116, 139);")
        
        clock_layout = QHBoxLayout()
        clock_layout.addWidget(self.calendar)
        clock_layout.addStretch()
        clock_layout.addWidget(self.clock_label, alignment=Qt.AlignBottom)
        
        self.main_layout.addLayout(clock_layout)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        
        self.update_clock()
        
        self.populate_ui_from_data()
        self.sync_calendar_to_day()

    def get_default_data(self):
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        return {day: ["", "", "", ""] for day in days}

    def load_data(self):
        if os.path.exists("plan_semanal.json"):
            try:
                with open("plan_semanal.json", "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except:
                self.data = self.get_default_data()
        else:
            self.data = self.get_default_data()

    def save_data(self):
        with open("plan_semanal.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def populate_ui_from_data(self):
        for day, meals in self.data.items():
            for i, text in enumerate(meals):
                card = self.tab_planner.meal_cards[day][i]
                card.blockSignals(True)
                card.setPlainText(text)
                card.blockSignals(False)
        self.update_dashboard_from_selector()

    def update_dashboard_from_selector(self):
        day = self.tab_dashboard.day_selector.currentText()
        meals = self.data[day]
        for i, text in enumerate(meals):
            card = self.tab_dashboard.meal_cards[i]
            card.blockSignals(True)
            card.setPlainText(text)
            card.blockSignals(False)

    def sync_calendar_to_day(self):
        selected_date = self.calendar.selectedDate()
        day_idx = selected_date.dayOfWeek() - 1
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        day_name = days[day_idx]
        self.tab_dashboard.day_selector.setCurrentText(day_name)

    def on_dashboard_text_changed(self):
        day = self.tab_dashboard.day_selector.currentText()
        for i, card in enumerate(self.tab_dashboard.meal_cards):
            text = card.toPlainText()
            self.data[day][i] = text
            
            p_card = self.tab_planner.meal_cards[day][i]
            p_card.blockSignals(True)
            p_card.setPlainText(text)
            p_card.blockSignals(False)
            
        self.save_data()

    def on_planner_text_changed(self, day, index):
        text = self.tab_planner.meal_cards[day][index].toPlainText()
        self.data[day][index] = text
        
        if day == self.tab_dashboard.day_selector.currentText():
            d_card = self.tab_dashboard.meal_cards[index]
            d_card.blockSignals(True)
            d_card.setPlainText(text)
            d_card.blockSignals(False)
            
        self.save_data()

    def update_clock(self):
        tz_gmt4 = timezone(timedelta(hours=-4))
        now = datetime.now(tz_gmt4)
        
        if 6 <= now.hour < 19:
            period = "☀️ Día"
        else:
            period = "🌙 Noche"
            
        time_str = now.strftime("%I:%M:%S %p")
        self.clock_label.setText(f"{period} | Hora local (GMT-4): {time_str}")

if __name__ == "__main__":
    app = QApplication([])
    window = MealApp()
    window.show()
    app.exec_()