import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QFrame, QScrollArea, QLineEdit,
    QListWidget, QListWidgetItem, QButtonGroup, QAbstractItemView,
    QDialog, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QStackedWidget, QSizePolicy, QFileDialog, QDateEdit,
)
from PyQt6.QtCore import Qt, QTimer, QDate, QLocale
from PyQt6.QtGui import QFont, QPixmap, QIcon, QPalette, QColor

import json
from datetime import datetime
from models import Beverage, Snack, Category, Order, OrderItem
from models.menu import create_menu_item
from styles import STYLESHEET, COLORS


MENU_DATA = [
    ("beverage", "Espresso", 45.0, Category.COFFEE, "espresso.png"),
    ("beverage", "Cappuccino", 55.0, Category.COFFEE, "cappuccino.png"),
    ("beverage", "Latte", 60.0, Category.COFFEE, "latte.png"),
    ("beverage", "Americano", 50.0, Category.COFFEE, "americano.png"),
    ("beverage", "Mocha", 65.0, Category.COFFEE, "mocha.png"),
    ("beverage", "Iced Coffee Milk", 55.0, Category.COFFEE, "iced-coffee-milk.png"),
    ("beverage", "Cold Brew", 65.0, Category.COFFEE, "cold-brew.png"),
    ("beverage", "Flat White", 60.0, Category.COFFEE, "flat-white.png"),
    ("beverage", "Green Tea Latte", 60.0, Category.TEA, "green-tea-latte.png"),
    ("beverage", "Thai Tea", 45.0, Category.TEA, "thai-tea.png"),
    ("beverage", "Matcha Latte", 65.0, Category.TEA, "matcha-latte.png"),
    ("snack", "Croissant", 45.0, Category.SNACK, "croissant.png"),
    ("snack", "Chocolate Cake", 75.0, Category.SNACK, "chocolate-cake.png"),
    ("snack", "Sandwich", 85.0, Category.SNACK, "sandwich.png"),
]

ASSETS_DIR = Path(__file__).parent / "assets" / "images"


def show_info(parent, title: str, message: str):
    d = QDialog(parent)
    d.setWindowTitle(title)
    d.setFixedSize(400, 140)
    d.setAutoFillBackground(True)
    pal = d.palette()
    pal.setColor(QPalette.ColorRole.Window, QColor(0xFF, 0xFF, 0xFF))
    pal.setColor(QPalette.ColorRole.Base, QColor(0xFF, 0xFF, 0xFF))
    d.setPalette(pal)
    d.setStyleSheet("""
        QDialog { background-color: #FFFFFF; }
        QLabel { color: #4A4035; font-size: 14px; }
        QPushButton {
            background-color: #7B5C3E; color: white; border: none;
            border-radius: 6px; padding: 8px 16px; min-width: 80px;
        }
        QPushButton:hover { background-color: #9B7C5E; }
    """)
    layout = QVBoxLayout(d)
    layout.setContentsMargins(24, 24, 24, 16)
    lbl = QLabel(message)
    lbl.setWordWrap(True)
    lbl.setAutoFillBackground(True)
    lbl.setStyleSheet("background-color: #FFFFFF; color: #4A4035; font-size: 14px;")
    layout.addWidget(lbl)
    btn = QPushButton("ตกลง")
    btn.clicked.connect(d.accept)
    layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignRight)
    d.exec()


def show_warning(parent, title: str, message: str):
    show_info(parent, title, message)


class MenuCard(QFrame):

    def __init__(self, menu_item, on_add, parent=None):
        super().__init__(parent)
        self.menu_item = menu_item
        self.on_add = on_add
        self.setObjectName("menu_card")
        self.setFixedHeight(180)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        img_name = getattr(self.menu_item, "image_path", None) or "coffee-menu.png"
        img_path = ASSETS_DIR / img_name
        if img_path.exists():
            pix = QPixmap(str(img_path)).scaled(72, 72, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            img_label = QLabel()
            img_label.setPixmap(pix)
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(img_label)

        name = QLabel(self.menu_item.name)
        name.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        name.setWordWrap(True)
        layout.addWidget(name)

        price = QLabel(self.menu_item.get_display_price())
        price.setStyleSheet(f"color: {COLORS['text']}; font-weight: 600; font-size: 14px;")
        layout.addWidget(price)

        add_btn = QPushButton("+")
        add_btn.setObjectName("add_btn")
        add_btn.setFixedSize(32, 32)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(lambda: self.on_add(self.menu_item))
        layout.addWidget(add_btn, alignment=Qt.AlignmentFlag.AlignRight)


class ReceiptDialog(QDialog):
    def __init__(self, receipt_text: str, order=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ใบเสร็จ")
        self.setMinimumSize(380, 200)
        self.resize(400, 380)
        self._receipt_text = receipt_text
        self._order = order
        self.setStyleSheet(STYLESHEET)
        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setHtml(self._receipt_to_html(receipt_text, order))
        self.text_edit.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Minimum
        )
        self.text_edit.setFixedWidth(360)
        self.text_edit.setMaximumHeight(450)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #B8A88A;
                border-radius: 4px;
                padding: 20px;
            }
        """)
        layout.addWidget(self.text_edit)
        QTimer.singleShot(0, self._fit_to_content)
        btn_layout = QHBoxLayout()
        receipt_btn = QPushButton("บันทึกใบเสร็จ")
        receipt_btn.setObjectName("secondary")
        receipt_btn.clicked.connect(self._save_as_image)
        ok_btn = QPushButton("ปิด")
        ok_btn.setObjectName("primary")
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(receipt_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)

    def _fit_to_content(self):
        doc = self.text_edit.document()
        h = int(doc.size().height()) + 40
        self.text_edit.setFixedHeight(min(max(h, 120), 480))
        self.adjustSize()

    def _receipt_to_html(self, txt: str, order=None) -> str:
        lines = txt.strip().split("\n")
        css = (
            "font-family: 'Consolas','Courier New',monospace; "
            "color: #1a1a1a; font-size: 12px; line-height: 1.6; "
            "min-width: 100%; max-width: 360px; padding: 0; word-wrap: break-word;"
        )
        body = [f'<div style="{css}">']
        i = 0
        while i < len(lines):
            s = lines[i].rstrip()
            if not s:
                body.append('<div style="height: 6px;"></div>')
                i += 1
                continue
            if set(s.strip()) <= set("=-"):
                body.append(f'<pre style="margin: 4px 0; font-size: 11px; color: #333;">{s}</pre>')
                i += 1
                continue
            if "GREEN GROUNDS" in s:
                body.append(f'<div style="font-weight: bold; font-size: 15px; margin: 6px 0; text-align: center;">{s}</div>')
                i += 1
                continue
            if "รวมทั้งสิ้น" in s:
                body.append(f'<div style="font-size: 15px; font-weight: bold; margin: 12px 0 6px 0;">{s}</div>')
                i += 1
                continue
            if "ขอบคุณ" in s or "รับเครื่องดื่ม" in s:
                body.append(f'<div style="font-size: 11px; margin: 3px 0; color: #555; text-align: center;">{s}</div>')
                i += 1
                continue
            if "รายการ" in s and "จำนวน" in s and order is not None:
                tbl_css = "border-collapse: collapse; width: 100%; font-size: 12px; margin: 4px 0;"
                body.append(f'<table style="{tbl_css}"><thead><tr>')
                body.append('<th style="text-align: left; padding: 2px 8px 2px 0; font-weight: bold;">รายการ</th>')
                body.append('<th style="text-align: right; padding: 2px 8px; font-weight: bold;">จำนวน</th>')
                body.append('<th style="text-align: right; padding: 2px 0 2px 8px; font-weight: bold;">ราคา</th>')
                body.append('</tr></thead><tbody>')
                for oi in order.items:
                    name = (oi.menu_item.name[:18] + "..") if len(oi.menu_item.name) > 20 else oi.menu_item.name
                    body.append(f'<tr><td style="text-align: left; padding: 2px 8px 2px 0;">{name}</td>')
                    body.append(f'<td style="text-align: right; padding: 2px 8px;">{oi.quantity}</td>')
                    body.append(f'<td style="text-align: right; padding: 2px 0 2px 8px;">{oi.menu_item.price:.2f}</td></tr>')
                body.append('</tbody></table>')
                i += 1
                if i < len(lines) and set(lines[i].strip()) <= set("-"):
                    i += 1
                while i < len(lines):
                    t = lines[i].strip()
                    if set(t) <= set("-") or "รวมทั้งสิ้น" in lines[i]:
                        break
                    i += 1
                continue
            if "รายการ" in s and "จำนวน" in s:
                body.append(f'<div style="font-weight: bold; font-size: 11px; margin: 4px 0;">{s}</div>')
                i += 1
                continue
            if s.strip():
                body.append(f'<pre style="margin: 2px 0; font-size: 12px;">{s}</pre>')
            i += 1
        body.append('</div>')
        return "".join(body)

    def _save_as_image(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "บันทึกภาพใบเสร็จ",
            f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            "PNG Image (*.png);;All Files (*)"
        )
        if path:
            try:
                pixmap = self.text_edit.grab()
                pixmap.save(path)
                show_info(self, "สำเร็จ", f"บันทึกใบเสร็จแล้วที่ {path}")
            except Exception as e:
                show_warning(self, "ผิดพลาด", f"บันทึกภาพไม่ได้: {e}")

class ReportDialog(QDialog):
    def __init__(self, history_path: Path, parent=None):
        super().__init__(parent)
        self._history_path = history_path
        self.setWindowTitle("รายงานและสถิติ")
        self.setMinimumSize(760, 560)
        self.resize(860, 640)
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, QColor(0xF5, 0xF2, 0xED))
        pal.setColor(QPalette.ColorRole.Base, QColor(0xFF, 0xFF, 0xFF))
        self.setPalette(pal)
        self.setStyleSheet("""
            QDialog { background-color: #F5F2ED; }
            QPushButton { background-color: #7B5C3E; color: white; border: none; border-radius: 8px; padding: 10px 20px; }
            QPushButton:hover { background-color: #9B7C5E; }
            QDateEdit {
                padding: 8px 10px;
                border: 1px solid #D4CFC4;
                border-radius: 6px;
                background: #FFFFFF;
                color: #4A4035;
            }
            QDateEdit:focus { border-color: #7B5C3E; }
            QCalendarWidget {
                background: #FFFFFF;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background: #7B5C3E;
                color: white;
            }
            QCalendarWidget QToolButton {
                background: transparent;
                color: white;
                border: none;
                min-width: 32px;
            }
            QCalendarWidget QMenu { background: #FFFFFF; }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #7B5C3E;
                selection-color: white;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: #4A4035;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)

        today = QDate.currentDate()
        filter_frame = QFrame()
        filter_frame.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border-radius: 8px;
                border: 1px solid #E0DDD8;
            }
        """)
        filter_row = QHBoxLayout(filter_frame)
        filter_row.setSpacing(14)
        filter_row.setContentsMargins(18, 14, 18, 14)
        lb1 = QLabel("ตั้งแต่")
        lb1.setMinimumWidth(40)
        lb1.setStyleSheet("border: none; background: transparent; color: #4A4035;")
        filter_row.addWidget(lb1)
        self.date_from = QDateEdit(today)
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat("dd/MM/yyyy")
        self.date_from.setMinimumWidth(120)
        self.date_from.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        filter_row.addWidget(self.date_from)
        lb2 = QLabel("ถึง")
        lb2.setMinimumWidth(24)
        lb2.setStyleSheet("border: none; background: transparent; color: #4A4035;")
        filter_row.addWidget(lb2)
        self.date_to = QDateEdit(today)
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("dd/MM/yyyy")
        self.date_to.setMinimumWidth(120)
        self.date_to.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        filter_row.addWidget(self.date_to)
        filter_row.addSpacing(20)
        for btn_label, days in [("วันนี้", 0), ("7 วัน", 7), ("30 วัน", 30)]:
            btn = QPushButton(btn_label)
            btn.setMinimumWidth(56)
            btn.setStyleSheet("background: #F5F3EF; color: #4A4035; padding: 8px 14px; border-radius: 6px; border: 1px solid #E0DDD8;")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda c, d=days: self._set_date_range_and_refresh(d))
            filter_row.addWidget(btn)
        view_btn = QPushButton("ดูสรุป")
        view_btn.setMinimumWidth(70)
        view_btn.setStyleSheet("background: #7B5C3E; color: white; padding: 8px 20px; border-radius: 6px;")
        view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        view_btn.clicked.connect(self._refresh)
        filter_row.addWidget(view_btn)
        filter_row.addStretch()
        filter_frame.setMinimumWidth(720)
        layout.addWidget(filter_frame)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        card1, self._card1_val = self._stat_card_with_ref("จำนวนคำสั่ง", "0", "รายการ")
        card2, self._card2_val = self._stat_card_with_ref("รายได้รวม", "฿0", "")
        stats_layout.addWidget(card1)
        stats_layout.addWidget(card2)
        layout.addLayout(stats_layout)

        section = QLabel("สินค้าขายดี")
        section.setStyleSheet("font-weight: 600; font-size: 14px; color: #4A4035;")
        layout.addWidget(section)
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["อันดับ", "รายการ", "จำนวน"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #E8E2D9;
                border-radius: 8px;
                gridline-color: #E8E2D9;
                outline: none;
            }
            QTableWidget::item {
                padding: 10px;
                color: #4A4035;
                background-color: #FFFFFF;
            }
            QTableWidget::item:alternate {
                background-color: #F5F3EF;
                color: #4A4035;
            }
            QHeaderView::section {
                background-color: #F0EDE7;
                color: #4A4035;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #E8E2D9;
            }
        """)
        tp = table.palette()
        tp.setColor(QPalette.ColorRole.Base, QColor(0xFF, 0xFF, 0xFF))
        tp.setColor(QPalette.ColorRole.AlternateBase, QColor(0xF5, 0xF3, 0xEF))
        tp.setColor(QPalette.ColorRole.Text, QColor(0x4A, 0x40, 0x35))
        tp.setColor(QPalette.ColorRole.Highlight, QColor(0xF5, 0xF3, 0xEF))
        tp.setColor(QPalette.ColorRole.HighlightedText, QColor(0x4A, 0x40, 0x35))
        table.setPalette(tp)
        layout.addWidget(table, 1)
        self._table = table

        ok_btn = QPushButton("ปิด")
        ok_btn.setObjectName("primary")
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)

        self._refresh()

    def _set_date_range_and_refresh(self, days: int):
        today = QDate.currentDate()
        if days == 0:
            self.date_from.setDate(today)
            self.date_to.setDate(today)
        else:
            self.date_to.setDate(today)
            self.date_from.setDate(today.addDays(-days))
        self._refresh()

    def _refresh(self):
        from_date = self.date_from.date().toPyDate()
        to_date = self.date_to.date().toPyDate()
        total_orders, total_revenue, item_counts = self._load_data(self._history_path, from_date, to_date)
        self._card1_val.setText(f"{total_orders} รายการ")
        self._card2_val.setText(f"฿{total_revenue:,.0f}")
        self._table.setRowCount(0)
        sorted_items = sorted(item_counts.items(), key=lambda x: -x[1])[:10]
        self._table.setRowCount(len(sorted_items) if sorted_items else 1)
        for i, (name, qty) in enumerate(sorted_items, 1):
            self._table.setItem(i - 1, 0, QTableWidgetItem(str(i)))
            self._table.setItem(i - 1, 1, QTableWidgetItem(name))
            self._table.setItem(i - 1, 2, QTableWidgetItem(f"{qty} รายการ"))
        if not sorted_items:
            self._table.setItem(0, 0, QTableWidgetItem("-"))
            self._table.setItem(0, 1, QTableWidgetItem("ยังไม่มีข้อมูล"))
            self._table.setItem(0, 2, QTableWidgetItem("-"))

    def _stat_card_with_ref(self, title: str, value: str, suffix: str):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E8E2D9;
            }
            QFrame QLabel {
                background: transparent;
                border: none;
                outline: none;
            }
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        lbl = QLabel(title)
        lbl.setStyleSheet("color: #7A7065; font-size: 13px; border: none; background: transparent;")
        layout.addWidget(lbl)
        val = QLabel(value + (" " + suffix if suffix else ""))
        val.setStyleSheet("color: #7B5C3E; font-size: 20px; font-weight: 700; border: none; background: transparent;")
        val.setWordWrap(True)
        layout.addWidget(val)
        card.setMinimumWidth(180)
        return card, val

    def _load_data(self, path: Path, from_date=None, to_date=None):
        total_orders = 0
        total_revenue = 0.0
        item_counts = {}
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    history = json.load(f)
                filtered = []
                for o in history:
                    dt_str = o.get("datetime", "")
                    if not dt_str:
                        continue
                    try:
                        order_date = datetime.fromisoformat(dt_str).date()
                    except (ValueError, TypeError):
                        continue
                    if from_date and order_date < from_date:
                        continue
                    if to_date and order_date > to_date:
                        continue
                    filtered.append(o)
                total_orders = len(filtered)
                total_revenue = sum(o.get("total", 0) for o in filtered)
                for o in filtered:
                    for it in o.get("items", []):
                        n = it.get("name", "")
                        q = it.get("qty", 0)
                        item_counts[n] = item_counts.get(n, 0) + q
            except (json.JSONDecodeError, IOError):
                pass
        return total_orders, total_revenue, item_counts


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.order = Order()
        self._order_counter = 1000
        self._order_history_file = Path(__file__).parent / "order_history.json"
        self._menu_items = [
            create_menu_item(m[0], m[1], m[2], m[3], image_path=m[4]) for m in MENU_DATA
        ]
        self._current_category = None
        self.setWindowTitle("Green Grounds Coffee - Natthawat Khaokaew 68114540337")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 750)
        self.setStyleSheet(STYLESHEET)
        self._build_ui()

    def _build_ui(self):
        central = QFrame()
        central.setObjectName("centralBg")
        central.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(32)

        layout.addWidget(self._create_menu_panel(), 3)
        layout.addWidget(self._create_order_panel(), 1)

    def _create_header(self):
        header = QWidget()
        h = QHBoxLayout(header)
        h.setContentsMargins(0, 0, 0, 24)

        title = QLabel("GREEN GROUNDS COFFEE")
        title.setObjectName("title")
        h.addWidget(title)

        h.addStretch()
        report_btn = QPushButton("สรุปยอดขาย")
        report_btn.setObjectName("secondary")
        report_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        report_btn.clicked.connect(self._show_report)
        h.addWidget(report_btn)
        date_lbl = QLabel(datetime.now().strftime("%A, %d %B"))
        date_lbl.setStyleSheet(f"color: {COLORS['text_secondary']};")
        h.addWidget(date_lbl)
        return header

    def _create_menu_panel(self):
        panel = QFrame()
        panel.setObjectName("menuPanelBg")
        panel.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._create_header())

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("ค้นหาเมนู...")
        self.search_edit.textChanged.connect(self._filter_menu)
        layout.addWidget(self.search_edit)

        cat_layout = QHBoxLayout()
        cat_layout.setSpacing(12)
        self.cat_group = QButtonGroup()
        for cat in [Category.COFFEE, Category.TEA, Category.SNACK]:
            btn = QPushButton(cat.value)
            btn.setObjectName("category")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, c=cat: self._filter_category(c))
            self.cat_group.addButton(btn)
            cat_layout.addWidget(btn)
        cat_layout.addStretch()
        layout.addLayout(cat_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"QScrollArea {{ background-color: {COLORS['background']}; }} QAbstractScrollArea::viewport {{ border: none; background-color: {COLORS['background']}; }}")
        grid_w = QWidget()
        p = grid_w.palette()
        p.setColor(QPalette.ColorRole.Window, QColor(0xE8, 0xE6, 0xE2))
        grid_w.setPalette(p)
        grid_w.setAutoFillBackground(True)
        self.menu_grid = QGridLayout(grid_w)
        self.menu_grid.setSpacing(20)
        scroll.setWidget(grid_w)
        layout.addWidget(scroll)

        self._populate_menu()
        return panel

    def _filter_category(self, cat):
        self._current_category = cat
        self._populate_menu()

    def _filter_menu(self):
        self._populate_menu()

    def _populate_menu(self):
        for i in reversed(range(self.menu_grid.count())):
            w = self.menu_grid.itemAt(i).widget()
            if w:
                w.deleteLater()

        items = self._menu_items
        if self._current_category:
            items = [m for m in items if m.category == self._current_category]
        q = self.search_edit.text().strip().lower() if hasattr(self, "search_edit") else ""
        if q:
            items = [m for m in items if q in m.name.lower()]

        for i, item in enumerate(items):
            row, col = i // 4, i % 4
            card = MenuCard(item, self._add_to_order)
            self.menu_grid.addWidget(card, row, col)

    def _create_order_panel(self):
        panel = QFrame()
        panel.setObjectName("order_panel")
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)

        self._order_counter += 1
        self.receipt_label = QLabel(f"ใบเสร็จ #{self._order_counter}")
        self.receipt_label.setObjectName("receipt_id")
        layout.addWidget(self.receipt_label)

        toggle = QHBoxLayout()
        self.dine_btn = QPushButton("ทานที่ร้าน")
        self.dine_btn.setObjectName("dine_toggle")
        self.dine_btn.setCheckable(True)
        self.dine_btn.setChecked(True)
        self.dine_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dine_btn.clicked.connect(lambda: self._set_dine_in(True))
        self.takeaway_btn = QPushButton("ซื้อกลับบ้าน")
        self.takeaway_btn.setObjectName("dine_toggle")
        self.takeaway_btn.setCheckable(True)
        self.takeaway_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.takeaway_btn.clicked.connect(lambda: self._set_dine_in(False))
        toggle.addWidget(self.dine_btn)
        toggle.addWidget(self.takeaway_btn)
        layout.addLayout(toggle)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("ชื่อลูกค้า")
        layout.addWidget(self.name_edit)

        self.table_row = QWidget()
        table_layout = QVBoxLayout(self.table_row)
        table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_edit = QLineEdit()
        self.table_edit.setPlaceholderText("เลขโต๊ะ")
        table_layout.addWidget(self.table_edit)
        layout.addWidget(self.table_row)

        layout.addWidget(QLabel("รายการสั่ง"))
        self.order_stack = QStackedWidget()
        self.empty_label = QLabel("ยังไม่มีรายการ\nกด + ที่เมนูเพื่อเพิ่มรายการ")
        self.empty_label.setObjectName("empty_state")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setMinimumHeight(120)
        self.order_list = QListWidget()
        self.order_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.order_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.order_stack.addWidget(self.empty_label)
        self.order_stack.addWidget(self.order_list)
        self.order_stack.setCurrentWidget(self.empty_label)
        layout.addWidget(self.order_stack, 1)
        qty_btns = QHBoxLayout()
        qty_minus = QPushButton("-")
        qty_minus.setObjectName("qty_btn")
        qty_minus.setFixedSize(44, 36)
        qty_minus.setCursor(Qt.CursorShape.PointingHandCursor)
        qty_minus.clicked.connect(lambda: self._change_quantity(-1))
        qty_plus = QPushButton("+")
        qty_plus.setObjectName("qty_btn")
        qty_plus.setFixedSize(50, 36)
        qty_plus.setCursor(Qt.CursorShape.PointingHandCursor)
        qty_plus.clicked.connect(lambda: self._change_quantity(1))
        remove_btn = QPushButton("ลบ")
        remove_btn.setObjectName("secondary")
        remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_btn.clicked.connect(self._remove_selected_item)
        qty_btns.addWidget(qty_minus)
        qty_btns.addWidget(qty_plus)
        qty_btns.addWidget(remove_btn)
        layout.addLayout(qty_btns)

        total_frame = QFrame()
        total_frame.setStyleSheet("background-color: #FAF8F5; border-radius: 8px; padding: 4px;")
        total_layout = QVBoxLayout(total_frame)
        total_layout.setContentsMargins(16, 12, 16, 12)
        self.total_label = QLabel("รวมทั้งสิ้น ฿0")
        self.total_label.setObjectName("total")
        total_layout.addWidget(self.total_label)
        layout.addWidget(total_frame)

        confirm_btn = QPushButton("ยืนยันคำสั่ง")
        confirm_btn.setObjectName("primary")
        confirm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        confirm_btn.clicked.connect(self._confirm_order)
        layout.addWidget(confirm_btn)

        clear_btn = QPushButton("ล้างรายการ")
        clear_btn.setObjectName("secondary")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self._clear_order)
        layout.addWidget(clear_btn)

        return panel

    def _set_dine_in(self, is_dine):
        self.dine_btn.setChecked(is_dine)
        self.takeaway_btn.setChecked(not is_dine)
        self.order.is_dine_in = is_dine
        self.table_row.setVisible(is_dine)

    def _add_to_order(self, menu_item):
        self.order.add_item(menu_item)
        self._refresh_order_list()

    def _remove_selected_item(self):
        idx = self.order_list.currentRow()
        if idx >= 0:
            self.order.remove_item(idx)
            self._refresh_order_list()

    def _change_quantity(self, delta: int):
        idx = self.order_list.currentRow()
        if idx < 0 or idx >= len(self.order.items):
            return
        oi = self.order.items[idx]
        menu_name = oi.menu_item.name
        new_qty = oi.quantity + delta
        if new_qty <= 0:
            self.order.remove_item(idx)
        else:
            self.order.update_quantity(idx, new_qty)
        self._refresh_order_list(keep_selected=menu_name if new_qty > 0 else None)

    def _refresh_order_list(self, keep_selected: str = None):
        self.order_list.clear()
        for oi in self.order.items:
            item = QListWidgetItem(f"{oi.menu_item.name} x{oi.quantity}  ·  ฿{oi.subtotal:.0f}")
            img_name = getattr(oi.menu_item, "image_path", None)
            if img_name:
                img_path = ASSETS_DIR / img_name
                if img_path.exists():
                    pix = QPixmap(str(img_path)).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    item.setIcon(QIcon(pix))
            self.order_list.addItem(item)
        if keep_selected:
            for i in range(self.order_list.count()):
                if keep_selected in self.order_list.item(i).text():
                    self.order_list.setCurrentRow(i)
                    break
        if self.order.items:
            self.order_stack.setCurrentWidget(self.order_list)
        else:
            self.order_stack.setCurrentWidget(self.empty_label)
        self.total_label.setText(f"รวมทั้งสิ้น ฿{self.order.total:.0f}")

    def _confirm_order(self):
        if not self.order.items:
            show_warning(self, "แจ้งเตือน", "ยังไม่มีรายการสั่ง กรุณาเลือกเมนูก่อน")
            return
        self.order.customer_name = self.name_edit.text().strip() or "ลูกค้า"
        self.order.table_no = self.table_edit.text().strip()
        self.order.order_id = self._order_counter
        receipt = self._build_receipt()
        self._save_order_history()
        dlg = ReceiptDialog(receipt, self.order, self)
        dlg.exec()
        self._clear_order()
        self._order_counter += 1
        self.receipt_label.setText(f"ใบเสร็จ #{self._order_counter}")

    def _build_receipt(self) -> str:
        W = 38
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M")
        customer_display = f"คุณ {self.order.customer_name}" if self.order.customer_name != "ลูกค้า" else self.order.customer_name
        type_str = "ทานที่ร้าน" if self.order.is_dine_in else "ซื้อกลับบ้าน"
        info_lines = [
            f"เลขที่: {self.order.order_id}",
            f"วันที่: {date_str}",
            f"เวลา: {time_str}",
            f"ลูกค้า: {customer_display}",
        ]
        if self.order.is_dine_in:
            info_lines.insert(4, f"โต๊ะ: {self.order.table_no}")
        info_lines.append(f"ประเภท: {type_str}")
        lines = [
            "=" * W,
            "      GREEN GROUNDS COFFEE",
            "=" * W,
            *info_lines,
            "-" * W,
            f"{'รายการ':<20}{'จำนวน':>6}{'ราคา':>8}",
            "-" * W,
        ]
        for oi in self.order.items:
            name = (oi.menu_item.name[:18] + "..") if len(oi.menu_item.name) > 20 else oi.menu_item.name
            lines.append(f"{name:<20}{oi.quantity:>6}{oi.menu_item.price:>8.2f}")
        total_str = f"{self.order.total:.2f} บาท"
        lines.extend([
            "-" * W,
            "รวมทั้งสิ้น".ljust(W - len(total_str)) + total_str,
            "-" * W,
            "",
            "  ขอบคุณที่ใช้บริการ Green Grounds Coffee",
            "  กรุณานำใบเสร็จมารับเครื่องดื่มที่เคาน์เตอร์",
            "=" * W,
        ])
        return "\n".join(lines)

    def _clear_order(self):
        self.order.clear()
        self._refresh_order_list()

    def _save_order_history(self):
        record = {
            "order_id": self.order.order_id,
            "customer": self.order.customer_name,
            "table": self.order.table_no,
            "type": "ทานที่ร้าน" if self.order.is_dine_in else "ซื้อกลับบ้าน",
            "items": [{"name": oi.menu_item.name, "qty": oi.quantity, "subtotal": oi.subtotal} for oi in self.order.items],
            "total": self.order.total,
            "datetime": datetime.now().isoformat(),
        }
        history = []
        if self._order_history_file.exists():
            try:
                with open(self._order_history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except (json.JSONDecodeError, IOError):
                history = []
        history.append(record)
        with open(self._order_history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def _show_report(self):
        ReportDialog(self._order_history_file, self).exec()


def main():
    QLocale.setDefault(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(0xFF, 0xFF, 0xFF))
    palette.setColor(QPalette.ColorRole.Base, QColor(0xFF, 0xFF, 0xFF))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(0x4A, 0x40, 0x35))
    palette.setColor(QPalette.ColorRole.Button, QColor(0xFF, 0xFF, 0xFF))
    palette.setColor(QPalette.ColorRole.Text, QColor(0x4A, 0x40, 0x35))
    app.setPalette(palette)
    app.setStyleSheet(STYLESHEET)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
