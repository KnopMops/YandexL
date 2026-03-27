import random
import sys

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from api import fetch_city_map
from constants import CITIES


class LoaderThread(QThread):
    done = pyqtSignal(bytes, str, str)
    error = pyqtSignal(str)

    def __init__(self, city_name):
        super().__init__()
        self.city_name = city_name

    def run(self):
        try:
            data, resolved = fetch_city_map(self.city_name)
            self.done.emit(data, self.city_name, resolved)
        except Exception as exc:
            self.error.emit(str(exc))


class MapPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: #0f0f0f;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.map_label = QLabel(Qt.AlignmentFlag.AlignCenter)
        self.map_label.setStyleSheet("background: #1a1a2e;")
        layout.addWidget(self.map_label, stretch=1)

        bar = QWidget()
        bar.setStyleSheet("background: #0f0f0f;")
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(20, 12, 20, 12)
        bar_layout.setSpacing(12)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Название города...")
        self.input.setFont(QFont("Courier New", 14))
        self.input.setStyleSheet(
            "QLineEdit {"
            "  background: #1a1a2e; color: #e0e0e0;"
            "  border: 1px solid #333; border-radius: 6px;"
            "  padding: 8px 14px;"
            "}"
        )
        self.input.returnPressed.connect(self._on_check)

        self.btn_check = QPushButton("Проверить")
        self.btn_check.setFont(QFont("Courier New", 13))
        self.btn_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_check.setStyleSheet(
            "QPushButton {"
            "  background: #3d5afe; color: white;"
            "  border: none; border-radius: 6px; padding: 8px 22px;"
            "}"
            "QPushButton:hover { background: #536dfe; }"
        )
        self.btn_check.clicked.connect(self._on_check)

        self.btn_skip = QPushButton("Пропустить →")
        self.btn_skip.setFont(QFont("Courier New", 13))
        self.btn_skip.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_skip.setStyleSheet(
            "QPushButton {"
            "  background: #263238; color: #90a4ae;"
            "  border: 1px solid #37474f; border-radius: 6px; padding: 8px 22px;"
            "}"
            "QPushButton:hover { background: #37474f; color: #cfd8dc; }"
        )

        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Courier New", 13))
        self.result_label.setFixedWidth(240)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.score_label = QLabel("0 / 0")
        self.score_label.setFont(QFont("Courier New", 12))
        self.score_label.setStyleSheet("color: #546e7a;")

        bar_layout.addWidget(self.input, stretch=1)
        bar_layout.addWidget(self.btn_check)
        bar_layout.addWidget(self.btn_skip)
        bar_layout.addWidget(self.result_label)
        bar_layout.addStretch()
        bar_layout.addWidget(self.score_label)

        layout.addWidget(bar)

        self.current_city = None
        self.correct = 0
        self.total = 0

    def set_skip_callback(self, cb):
        self.btn_skip.clicked.connect(cb)

    def set_map(self, image_bytes, city_name):
        self.current_city = city_name
        self.result_label.setText("")
        self.input.clear()
        self.input.setFocus()

        px = QPixmap()
        px.loadFromData(image_bytes)
        scaled = px.scaled(
            self.map_label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.map_label.setPixmap(scaled)

    def _on_check(self):
        if self.current_city is None:
            return
        guess = self.input.text().strip().lower()
        answer = self.current_city.lower()
        self.total += 1
        if guess == answer:
            self.correct += 1
            self.result_label.setText("УХУ!")
            self.result_label.setStyleSheet("color: #69f0ae; font-weight: bold;")
        else:
            self.result_label.setText(f"{self.current_city}")
            self.result_label.setStyleSheet("color: #ff5252; font-weight: bold;")
        self.score_label.setText(f"{self.correct} / {self.total}")


class LoadingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: #0f0f0f;")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("Загружаю карту…")
        self.status_label.setFont(QFont("Courier New", 16))
        self.status_label.setStyleSheet("color: #546e7a;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bar = QProgressBar()
        bar.setRange(0, 0)
        bar.setFixedWidth(300)
        bar.setStyleSheet(
            "QProgressBar { background: #1a1a2e; border-radius: 4px; height: 6px; }"
            "QProgressBar::chunk { background: #3d5afe; border-radius: 4px; }"
        )

        layout.addWidget(self.status_label)
        layout.addSpacing(16)
        layout.addWidget(bar, alignment=Qt.AlignmentFlag.AlignCenter)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Угадай-ка город")
        self.resize(900, 680)
        self.setStyleSheet("background: #0f0f0f;")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.loading_page = LoadingPage()
        self.map_page = MapPage()
        self.map_page.set_skip_callback(self._next_city)

        self.stack.addWidget(self.loading_page)
        self.stack.addWidget(self.map_page)

        self.order = random.sample(CITIES, len(CITIES))
        self.index = 0
        self.loader = None

        self._next_city()

    def _next_city(self):
        if self.index >= len(self.order):
            self.order = random.sample(CITIES, len(CITIES))
            self.index = 0

        city_name = self.order[self.index]
        self.index += 1

        self.loading_page.status_label.setText("Загружаю карту…")
        self.stack.setCurrentWidget(self.loading_page)

        self.loader = LoaderThread(city_name)
        self.loader.done.connect(self._on_map_ready)
        self.loader.error.connect(self._on_error)
        self.loader.start()

    def _on_map_ready(self, data, city_name, _resolved):
        self.stack.setCurrentWidget(self.map_page)
        self.map_page.set_map(data, city_name)

    def _on_error(self, msg):
        self.loading_page.status_label.setText(f"Ошибка: {msg}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
