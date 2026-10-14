import json
import os
from datetime import datetime, timezone, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTabWidget, QLabel, QGridLayout, QTextEdit, 
                             QComboBox, QCalendarWidget, QLineEdit, QFrame, QPushButton, QFileDialog, QSizePolicy, QScrollArea)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap

class EditableMealCard(QFrame):
    """Clase personalizada para una tarjeta de comida"""
    textChanged = pyqtSignal()

    def __init__(self, style_sheet, show_image=True):
        super().__init__()
        self.setStyleSheet(style_sheet)
        self.image_path = ""
        self.show_image_section = show_image
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)
        
        # 1. Nombre del plato
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del plato...")
        self.name_input.setStyleSheet("""
            QLineEdit {
                font-weight: bold; 
                border: none; 
                background: transparent; 
                border-bottom: 2px solid rgba(0, 0, 0, 30);
                padding-bottom: 4px;
            }
        """)
        self.name_input.textChanged.connect(self.textChanged.emit)
        layout.addWidget(self.name_input)
        
        # 2. Sección de imagen (Solo en Dashboard)
        if self.show_image_section:
            image_layout = QHBoxLayout()
            
            self.img_preview = QLabel("Sin imagen")
            self.img_preview.setAlignment(Qt.AlignCenter)
            self.img_preview.setFixedSize(85, 85)
            self.img_preview.setStyleSheet("""
                QLabel {
                    border: 2px dashed rgb(200, 205, 210);
                    border-radius: 8px;
                    background: rgb(245, 247, 250);
                    color: rgb(120, 130, 140);
                    font-size: 11px;
                }
            """)
            
            img_btn_layout = QVBoxLayout()
            img_btn_layout.setSpacing(5)
            
            self.img_btn = QPushButton("📁 Buscar")
            self.img_btn.setMinimumHeight(32)
            self.img_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgb(240, 242, 245);
                    border: 1px solid rgb(210, 215, 220);
                    border-radius: 6px;
                    padding: 4px 10px;
                    font-weight: bold;
                    color: rgb(70, 80, 90);
                }
                QPushButton:hover {
                    background-color: rgb(230, 235, 240);
                }
            """)
            self.img_btn.clicked.connect(self.load_image)
            
            self.remove_img_btn = QPushButton("❌ Quitar")
            self.remove_img_btn.setMinimumHeight(32)
            self.remove_img_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgb(254, 226, 226);
                    border: 1px solid rgb(252, 165, 165);
                    border-radius: 6px;
                    padding: 4px 10px;
                    font-weight: bold;
                    color: rgb(185, 28, 28);
                }
                QPushButton:hover {
                    background-color: rgb(254, 202, 202);
                }
            """)
            self.remove_img_btn.clicked.connect(self.remove_image)
            
            img_btn_layout.addWidget(self.img_btn)
            img_btn_layout.addWidget(self.remove_img_btn)
            
            image_layout.addWidget(self.img_preview)
            image_layout.addLayout(img_btn_layout)
            layout.addLayout(image_layout)
        
        # 3. Ingredientes
        self.label_ing = QLabel("Ingredientes:")
        self.label_ing.setStyleSheet("font-weight: bold; color: rgb(90, 100, 110); border: none; background: transparent;")
        
        self.ingredients_input = QTextEdit()
        self.ingredients_input.setPlaceholderText("Ej. Pollo, arroz...")
        self.ingredients_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ingredients_input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ingredients_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid rgba(0, 0, 0, 40);
                background: rgba(255, 255, 255, 180);
                border-radius: 6px;
                padding: 4px;
            }
        """)
        self.ingredients_input.textChanged.connect(self.textChanged.emit)
        
        # 4. Descripción / Pasos
        self.label_desc = QLabel("Descripción / Pasos:")
        self.label_desc.setStyleSheet("font-weight: bold; color: rgb(90, 100, 110); border: none; background: transparent;")
        
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Instrucciones...")
        self.desc_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.desc_input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.desc_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid rgba(0, 0, 0, 40);
                background: rgba(255, 255, 255, 180);
                border-radius: 6px;
                padding: 4px;
            }
        """)
        self.desc_input.textChanged.connect(self.textChanged.emit)
        
        layout.addWidget(self.label_ing)
        layout.addWidget(self.ingredients_input)
        layout.addWidget(self.label_desc)
        layout.addWidget(self.desc_input)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.image_path = file_name
            self.update_image_preview()
            self.textChanged.emit()

    def remove_image(self):
        self.image_path = ""
        self.update_image_preview()
        self.textChanged.emit()

    def update_image_preview(self):
        if not self.show_image_section:
            return
        if self.image_path and os.path.exists(self.image_path):
            pixmap = QPixmap(self.image_path)
            scaled_pixmap = pixmap.scaled(81, 81, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.img_preview.setPixmap(scaled_pixmap)
            self.img_preview.setStyleSheet("""
                QLabel {
                    border: 2px solid rgb(34, 197, 94);
                    border-radius: 8px;
                    background: rgb(255, 255, 255);
                }
            """)
        else:
            self.img_preview.clear()
            self.img_preview.setText("Sin imagen")
            self.img_preview.setStyleSheet("""
                QLabel {
                    border: 2px dashed rgb(200, 205, 210);
                    border-radius: 8px;
                    background: rgb(245, 247, 250);
                    color: rgb(120, 130, 140);
                    font-size: 11px;
                }
            """)

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "ingredients": self.ingredients_input.toPlainText(),
            "description": self.desc_input.toPlainText(),
            "image_path": self.image_path
        }

    def set_data(self, data):
        self.name_input.blockSignals(True)
        self.ingredients_input.blockSignals(True)
        self.desc_input.blockSignals(True)
        
        if isinstance(data, dict):
            self.name_input.setText(data.get("name", ""))
            self.ingredients_input.setPlainText(data.get("ingredients", ""))
            self.desc_input.setPlainText(data.get("description", ""))
            self.image_path = data.get("image_path", "")
            self.update_image_preview()
        elif isinstance(data, str):
            self.name_input.setText(data)
            self.ingredients_input.setPlainText("")
            self.desc_input.setPlainText("")
            self.image_path = ""
            self.update_image_preview()
            
        self.name_input.blockSignals(False)
        self.ingredients_input.blockSignals(False)
        self.desc_input.blockSignals(False)


class MealApp(QMainWindow):
    
    class DashboardTab(QWidget):
        def __init__(self, main_app):
            super().__init__()
            self.main_app = main_app
            self.meal_cards = []
            
            layout = QVBoxLayout(self)
            
            self.title = QLabel("Dashboard del Día")
            self.title.setStyleSheet("font-weight: bold; color: rgb(34, 197, 94);")
            layout.addWidget(self.title)
            
            selector_layout = QHBoxLayout()
            self.selector_label = QLabel("Día asignado al Dashboard:")
            self.selector_label.setStyleSheet("font-weight: bold;")
            
            self.day_selector = QComboBox()
            self.day_selector.addItems(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
            self.day_selector.setMinimumHeight(40)
            self.day_selector.setStyleSheet("""
                QComboBox {
                    padding: 5px 15px; background: white; 
                    border: 2px solid rgb(200, 200, 200); border-radius: 6px;
                }
            """)
            
            self.day_selector.currentTextChanged.connect(self.main_app.update_dashboard_from_selector)
            
            selector_layout.addWidget(self.selector_label)
            selector_layout.addWidget(self.day_selector)
            selector_layout.addStretch()
            layout.addLayout(selector_layout)
            
            cards_main_layout = QHBoxLayout()
            cards_main_layout.setSpacing(15)
            
            card_styles = [
                "background-color: rgb(255, 241, 242); border-radius: 16px; border: 2px solid rgb(251, 113, 133);",
                "background-color: rgb(255, 247, 237); border-radius: 16px; border: 2px solid rgb(251, 146, 60);",
                "background-color: rgb(254, 252, 232); border-radius: 16px; border: 2px solid rgb(250, 204, 21);",
                "background-color: rgb(254, 249, 195); border-radius: 16px; border: 2px solid rgb(234, 179, 8);"
            ]
            
            for style in card_styles:
                meal_card = EditableMealCard(style, show_image=True)
                meal_card.setMinimumWidth(280)
                meal_card.setMinimumHeight(460)
                meal_card.textChanged.connect(self.main_app.on_dashboard_text_changed)
                
                self.meal_cards.append(meal_card)
                cards_main_layout.addWidget(meal_card)
                
            layout.addLayout(cards_main_layout)
            layout.addStretch()

    class PlannerTab(QWidget):
        def __init__(self, main_app):
            super().__init__()
            self.main_app = main_app
            self.meal_cards = {}
            
            main_layout = QVBoxLayout(self)
            
            self.title = QLabel("Planificador Semanal")
            self.title.setStyleSheet("font-weight: bold; color: rgb(249, 115, 22);")
            main_layout.addWidget(self.title)
            
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setStyleSheet("background: transparent; border: none;")
            
            container_widget = QWidget()
            self.grid = QGridLayout(container_widget)
            self.grid.setSpacing(15)
            
            days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            
            row_styles = [
                "background-color: rgb(255, 241, 242); border-radius: 12px; border: 2px solid rgb(251, 113, 133);",
                "background-color: rgb(255, 247, 237); border-radius: 12px; border: 2px solid rgb(251, 146, 60);",
                "background-color: rgb(254, 252, 232); border-radius: 12px; border: 2px solid rgb(250, 204, 21);",
                "background-color: rgb(254, 249, 195); border-radius: 12px; border: 2px solid rgb(234, 179, 8);"
            ]
            
            self.headers = []
            for col_idx, day in enumerate(days):
                self.meal_cards[day] = []
                
                header = QLabel(day)
                header.setAlignment(Qt.AlignCenter)
                header.setStyleSheet("font-weight: bold; color: rgb(30, 41, 59);")
                self.headers.append(header)
                self.grid.addWidget(header, 0, col_idx)
                
            for row_idx in range(1, 5):
                planner_style = row_styles[row_idx - 1]
                
                for col_idx, day in enumerate(days):
                    slot = EditableMealCard(planner_style, show_image=False)
                    slot.setMinimumWidth(240)
                    slot.setMinimumHeight(300)
                    
                    slot.textChanged.connect(lambda d=day, r=row_idx-1: self.main_app.on_planner_text_changed(d, r))
                    
                    self.meal_cards[day].append(slot)
                    self.grid.addWidget(slot, row_idx, col_idx)
                    
            scroll_area.setWidget(container_widget)
            main_layout.addWidget(scroll_area)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("App de Organización de Comidas")
        self.showFullScreen()
        
        self.load_data()
        
        self.current_font_size = 16
        self.update_global_stylesheet()
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Barra superior
        top_bar_layout = QHBoxLayout()
        self.app_title = QLabel("🍳 Organizador de Menús Inteligente")
        self.app_title.setStyleSheet("font-weight: bold; color: rgb(30, 41, 59);")
        
        self.exit_btn = QPushButton("❌ Salir de la App")
        self.exit_btn.setMinimumHeight(40)
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(239, 68, 68);
                color: white;
                border-radius: 8px;
                padding: 8px 22px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(220, 38, 38);
            }
        """)
        self.exit_btn.clicked.connect(self.close)
        
        top_bar_layout.addWidget(self.app_title)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.exit_btn)
        
        self.main_layout.addLayout(top_bar_layout)
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid rgb(220, 220, 220); 
                background: rgb(249, 250, 251); 
                border-radius: 10px; 
            }
            QTabBar::tab { 
                background: rgb(220, 220, 220); 
                padding: 12px 28px; 
                margin-right: 6px; 
                border-top-left-radius: 8px; 
                border-top-right-radius: 8px; 
                font-weight: bold;
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
        
        # Parte inferior: Calendario, Selector de tamaño de letra y Reloj
        bottom_layout = QHBoxLayout()
        
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumSize(360, 190)
        self.calendar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.calendar.setGridVisible(True)
        self.calendar.setStyleSheet("""
            QCalendarWidget QWidget { background-color: white; }
            QCalendarWidget QToolButton { height: 30px; font-weight: bold; color: rgb(30, 41, 59); }
            QCalendarWidget QMenu { background-color: white; }
            QCalendarWidget QSpinBox { background-color: white; }
        """)
        self.calendar.selectionChanged.connect(self.sync_calendar_to_day)
        
        controls_layout = QVBoxLayout()
        controls_layout.setAlignment(Qt.AlignBottom)
        controls_layout.setSpacing(10)
        
        font_size_layout = QHBoxLayout()
        font_size_label = QLabel("🔤 Tamaño de letra:")
        font_size_label.setStyleSheet("font-weight: bold; color: rgb(70, 80, 90);")
        
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["Pequeña", "Mediana", "Grande"])
        self.font_size_combo.setCurrentIndex(1)
        self.font_size_combo.setMinimumHeight(35)
        self.font_size_combo.setStyleSheet("""
            QComboBox {
                padding: 4px 12px; background: white; 
                border: 2px solid rgb(200, 200, 200); border-radius: 6px;
            }
        """)
        self.font_size_combo.currentIndexChanged.connect(self.change_font_size)
        
        font_size_layout.addWidget(font_size_label)
        font_size_layout.addWidget(self.font_size_combo)
        
        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.clock_label.setStyleSheet("font-weight: bold; color: rgb(100, 116, 139);")
        
        controls_layout.addLayout(font_size_layout)
        controls_layout.addWidget(self.clock_label)
        
        bottom_layout.addWidget(self.calendar)
        bottom_layout.addStretch()
        bottom_layout.addLayout(controls_layout)
        
        self.main_layout.addLayout(bottom_layout)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        
        self.update_clock() 
        
        self.populate_ui_from_data()
        self.sync_calendar_to_day()

    def change_font_size(self, index):
        if index == 0:
            self.current_font_size = 13
        elif index == 1:
            self.current_font_size = 16
        else:
            self.current_font_size = 20
            
        self.update_global_stylesheet()

    def update_global_stylesheet(self):
        base = self.current_font_size
        title_size = base + 12
        header_size = base + 3
        card_title_size = base + 2
        input_size = base
        
        style = f"""
            QMainWindow, QWidget {{
                background-color: rgb(249, 250, 251); 
                color: rgb(30, 41, 59); 
                font-size: {base}px;
            }}
            QLineEdit {{
                font-size: {card_title_size}px;
            }}
            QTextEdit {{
                font-size: {input_size}px;
            }}
        """
        self.setStyleSheet(style)
        
        if hasattr(self, 'tab_dashboard'):
            self.tab_dashboard.title.setStyleSheet(f"font-size: {title_size}px; font-weight: bold; color: rgb(34, 197, 94);")
            self.tab_dashboard.selector_label.setStyleSheet(f"font-size: {header_size}px; font-weight: bold;")
            self.tab_dashboard.day_selector.setStyleSheet(f"QComboBox {{ font-size: {header_size}px; padding: 5px 15px; background: white; border: 2px solid rgb(200, 200, 200); border-radius: 6px; }}")
            
        if hasattr(self, 'tab_planner'):
            self.tab_planner.title.setStyleSheet(f"font-size: {title_size}px; font-weight: bold; color: rgb(249, 115, 22);")
            for header in self.tab_planner.headers:
                header.setStyleSheet(f"font-weight: bold; font-size: {header_size}px; color: rgb(30, 41, 59);")
                
        if hasattr(self, 'app_title'):
            self.app_title.setStyleSheet(f"font-size: {title_size - 4}px; font-weight: bold; color: rgb(30, 41, 59);")
            self.exit_btn.setStyleSheet(f"QPushButton {{ background-color: rgb(239, 68, 68); color: white; border-radius: 8px; padding: 8px 22px; font-weight: bold; font-size: {input_size}px; }} QPushButton:hover {{ background-color: rgb(220, 38, 38); }}")
            self.clock_label.setStyleSheet(f"font-size: {base + 1}px; font-weight: bold; color: rgb(100, 116, 139);")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        else:
            super().keyPressEvent(event)

    def get_default_data(self):
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        empty_meal = {"name": "", "ingredients": "", "description": "", "image_path": ""}
        return {day: [empty_meal.copy() for _ in range(4)] for day in days}

    def load_data(self):
        if os.path.exists("plan_semanal.json"):
            try:
                with open("plan_semanal.json", "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                    
                    self.data = self.get_default_data()
                    for day, meals in raw_data.items():
                        if day in self.data:
                            for i, meal in enumerate(meals):
                                if i < 4:
                                    if isinstance(meal, str):
                                        self.data[day][i] = {"name": meal, "ingredients": "", "description": "", "image_path": ""}
                                    elif isinstance(meal, dict):
                                        self.data[day][i] = {
                                            "name": meal.get("name", ""),
                                            "ingredients": meal.get("ingredients", ""),
                                            "description": meal.get("description", ""),
                                            "image_path": meal.get("image_path", "")
                                        }
            except:
                self.data = self.get_default_data()
        else:
            self.data = self.get_default_data()
        self.save_data()

    def save_data(self):
        with open("plan_semanal.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def populate_ui_from_data(self):
        for day, meals in self.data.items():
            for i, meal_dict in enumerate(meals):
                card = self.tab_planner.meal_cards[day][i]
                card.set_data(meal_dict)
        self.update_dashboard_from_selector()

    def update_dashboard_from_selector(self):
        day = self.tab_dashboard.day_selector.currentText()
        meals = self.data[day]
        for i, meal_dict in enumerate(meals):
            card = self.tab_dashboard.meal_cards[i]
            card.set_data(meal_dict)

    def sync_calendar_to_day(self):
        selected_date = self.calendar.selectedDate()
        day_idx = selected_date.dayOfWeek() - 1
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        day_name = days[day_idx]
        self.tab_dashboard.day_selector.setCurrentText(day_name)

    def on_dashboard_text_changed(self):
        day = self.tab_dashboard.day_selector.currentText()
        for i, card in enumerate(self.tab_dashboard.meal_cards):
            meal_data = card.get_data()
            self.data[day][i] = meal_data
            
            p_card = self.tab_planner.meal_cards[day][i]
            p_card.set_data(meal_data)
            
        self.save_data()

    def on_planner_text_changed(self, day, index):
        meal_data = self.tab_planner.meal_cards[day][index].get_data()
        self.data[day][index] = meal_data
        
        if day == self.tab_dashboard.day_selector.currentText():
            d_card = self.tab_dashboard.meal_cards[index]
            d_card.set_data(meal_data)
            
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