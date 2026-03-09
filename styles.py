COLORS = {
    "primary": "#7B5C3E",
    "primary_light": "#9B7C5E",
    "background": "#E8E6E2",
    "surface": "#FFFFFF",
    "text": "#4A4035",
    "text_secondary": "#7A7065",
    "accent": "#8B6914",
    "border": "#E8E2D9",
}

STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS["background"]};
}}

QFrame#centralBg, QFrame#menuPanelBg {{
    background-color: {COLORS["background"]};
}}

QDialog {{
    background-color: {COLORS["surface"]};
}}

QMessageBox {{
    background-color: {COLORS["surface"]};
}}

QMessageBox QWidget {{
    background-color: {COLORS["surface"]};
}}

QMessageBox QLabel {{
    color: {COLORS["text"]};
}}

QMessageBox QPushButton {{
    background-color: {COLORS["primary"]};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
}}

QFileDialog {{
    background-color: {COLORS["surface"]};
}}

QFileDialog QWidget {{
    background-color: {COLORS["surface"]};
}}

QFileDialog QTreeView, QFileDialog QListView {{
    background-color: {COLORS["surface"]};
    color: {COLORS["text"]};
}}

QWidget {{
    background-color: transparent;
    color: {COLORS["text"]};
    font-family: "Segoe UI", sans-serif;
}}

QLabel {{
    color: {COLORS["text"]};
    font-size: 14px;
}}

QLabel#title {{
    font-size: 20px;
    font-weight: 600;
    color: {COLORS["primary"]};
}}

QLabel#receipt_id {{
    font-size: 13px;
    font-weight: 600;
    color: {COLORS["text_secondary"]};
}}

QLabel#total {{
    font-size: 22px;
    font-weight: 700;
    color: {COLORS["primary"]};
}}

QLabel#empty_state {{
    color: {COLORS["text_secondary"]};
    font-size: 14px;
}}

QLineEdit {{
    padding: 12px 16px;
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    background-color: {COLORS["surface"]};
    font-size: 14px;
    color: {COLORS["text"]};
}}

QLineEdit:focus {{
    border-color: {COLORS["accent"]};
}}

QPushButton {{
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}}

QPushButton#primary {{
    background-color: {COLORS["primary"]};
    color: white;
}}

QPushButton#primary:hover {{
    background-color: {COLORS["primary_light"]};
}}

QPushButton#primary:pressed {{
    background-color: #6B4C2E;
}}

QPushButton#secondary {{
    background-color: #F0EDE7;
    color: {COLORS["text"]};
    border: 1px solid {COLORS["border"]};
}}

QPushButton#secondary:hover {{
    background-color: {COLORS["border"]};
}}

QPushButton#qty_btn {{
    background-color: {COLORS["primary"]};
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: bold;
}}

QPushButton#qty_btn:hover {{
    background-color: {COLORS["primary_light"]};
}}

QPushButton#add_btn {{
    background-color: {COLORS["primary"]};
    color: white;
    border: none;
    border-radius: 6px;
    min-width: 28px;
    min-height: 28px;
    padding: 2px;
    font-size: 14px;
}}

QPushButton#add_btn:hover {{
    background-color: {COLORS["primary_light"]};
}}

QPushButton#add_btn:pressed {{
    background-color: #6B4C2E;
}}

QPushButton#category {{
    background-color: {COLORS["surface"]};
    color: {COLORS["text"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    padding: 10px 18px;
}}

QPushButton#category:hover {{
    border-color: {COLORS["accent"]};
}}

QPushButton#category:checked {{
    background-color: {COLORS["primary"]};
    color: white;
    border-color: {COLORS["primary"]};
}}

QPushButton#dine_toggle {{
    background-color: #F0EDE7;
    color: {COLORS["text"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    padding: 10px 16px;
}}

QPushButton#dine_toggle:hover {{
    border-color: {COLORS["accent"]};
}}

QPushButton#dine_toggle:checked {{
    background-color: {COLORS["primary"]};
    color: white;
    border-color: {COLORS["primary"]};
}}

QScrollArea {{
    border: none;
    background-color: {COLORS["background"]};
}}

QAbstractScrollArea::viewport {{
    background-color: {COLORS["background"]};
}}

QScrollBar:vertical {{
    background: #E0DDD8;
    width: 10px;
    border-radius: 5px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: #C4C0B8;
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QFrame#menu_card {{
    background-color: {COLORS["surface"]};
    border-radius: 12px;
    border: 1px solid {COLORS["border"]};
}}

QFrame#menu_card:hover {{
    border-color: {COLORS["accent"]};
}}

QFrame#order_panel {{
    background-color: #F5F3EF;
    border-radius: 16px;
    border: 1px solid #D8D4CC;
}}

QListWidget {{
    background-color: #FAF8F5;
    border: 1px dashed {COLORS["border"]};
    border-radius: 8px;
    padding: 16px;
    outline: none;
}}

QListWidget:focus {{
    outline: none;
    border: 1px dashed {COLORS["border"]};
}}

QListWidget::item {{
    padding: 12px;
    border-radius: 8px;
    margin: 4px 0;
}}

QListWidget::item:hover {{
    background-color: {COLORS["border"]};
}}

QListWidget::item:selected {{
    background-color: #E8E2D9;
    color: {COLORS["text"]};
    border-radius: 8px;
    border: none;
    outline: none;
}}

QCalendarWidget {{
    background: #FFFFFF;
}}

QCalendarWidget QWidget#qt_calendar_navigationbar {{
    background: {COLORS["primary"]};
    color: white;
    min-height: 36px;
}}

QCalendarWidget QToolButton {{
    background: transparent;
    color: white;
    border: none;
}}

QCalendarWidget QAbstractItemView {{
    selection-background-color: {COLORS["primary"]};
    selection-color: white;
    color: {COLORS["text"]};
    font-size: 13px;
}}

QCalendarWidget QWidget {{
    alternate-background-color: transparent;
}}
"""
