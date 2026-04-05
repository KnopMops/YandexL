import os
import sys

from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtWidgets import QApplication

from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    QWebEngineProfile.defaultProfile().setPersistentStoragePath(
        os.path.join(os.path.dirname(__file__), "web_profile")
    )
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
