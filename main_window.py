import os

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from html_template import HTML_TEMPLATE
from map_bridge import MapBridge


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Яндекс.Карты – поиск и навигация")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        control_layout = QHBoxLayout()

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Введите название объекта...")
        control_layout.addWidget(QLabel("Поиск:"))
        control_layout.addWidget(self.search_edit)

        self.search_btn = QPushButton("Искать")
        self.search_btn.clicked.connect(self.on_search)
        control_layout.addWidget(self.search_btn)

        self.reset_btn = QPushButton("Сброс результата")
        self.reset_btn.clicked.connect(self.on_reset)
        control_layout.addWidget(self.reset_btn)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Светлая", "Тёмная"])
        self.theme_combo.currentIndexChanged.connect(self.on_theme_changed)
        control_layout.addWidget(QLabel("Тема:"))
        control_layout.addWidget(self.theme_combo)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Схема", "Спутник", "Гибрид", "Народная"])
        self.type_combo.currentIndexChanged.connect(self.on_type_changed)
        control_layout.addWidget(QLabel("Вид карты:"))
        control_layout.addWidget(self.type_combo)

        self.postal_check = QCheckBox("Показывать почтовый индекс")
        self.postal_check.stateChanged.connect(self.on_postal_toggled)
        control_layout.addWidget(self.postal_check)

        main_layout.addLayout(control_layout)

        self.address_display = QTextEdit()
        self.address_display.setReadOnly(True)
        self.address_display.setMaximumHeight(80)
        main_layout.addWidget(QLabel("Полный адрес найденного объекта:"))
        main_layout.addWidget(self.address_display)

        self.web_view = QWebEngineView()
        main_layout.addWidget(self.web_view)

        self.channel = QWebChannel()
        self.bridge = MapBridge()
        self.bridge.addressUpdated.connect(self.update_address_display)
        self.channel.registerObject("bridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        self.web_view.setHtml(HTML_TEMPLATE)

        QTimer.singleShot(500, self.sync_initial_state)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def sync_initial_state(self):
        self.on_theme_changed(0)
        self.on_type_changed(0)

    def on_search(self):
        query = self.search_edit.text().strip()
        if query:
            self.web_view.page().runJavaScript(f"searchByText('{query}');")

    def on_reset(self):
        self.web_view.page().runJavaScript("clearPlacemark();")
        self.address_display.clear()

    def on_theme_changed(self, index):
        is_dark = index == 1
        self.web_view.page().runJavaScript(f"setTheme({str(is_dark).lower()});")

    def on_type_changed(self, index):
        types = ["base", "satellite", "hybrid", "people"]
        self.web_view.page().runJavaScript(f"setMapType('{types[index]}');")

    def on_postal_toggled(self, state):
        show = state == Qt.CheckState.Checked.value
        self.web_view.page().runJavaScript(
            f"showPostalCode = {str(show).lower()}; updateAddressDisplay();"
        )

    def update_address_display(self, address):
        self.address_display.setText(address)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_PageUp:
            self.web_view.page().runJavaScript("""
                var z = map.getZoom();
                if (z < 19) map.setZoom(z + 1);
            """)
        elif key == Qt.Key.Key_PageDown:
            self.web_view.page().runJavaScript("""
                var z = map.getZoom();
                if (z > 1) map.setZoom(z - 1);
            """)
        elif key == Qt.Key.Key_Up:
            self.web_view.page().runJavaScript("move(0, 0.1);")
        elif key == Qt.Key.Key_Down:
            self.web_view.page().runJavaScript("move(0, -0.1);")
        elif key == Qt.Key.Key_Left:
            self.web_view.page().runJavaScript("move(-0.1, 0);")
        elif key == Qt.Key.Key_Right:
            self.web_view.page().runJavaScript("move(0.1, 0);")
        else:
            super().keyPressEvent(event)
