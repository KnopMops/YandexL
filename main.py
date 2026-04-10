def main():
    print("Hello from yandexl!")


if __name__ == "__main__":
    main()
    import os
    import sys

    from PyQt6 import uic
    from PyQt6.QtCore import Qt, QUrl
    from PyQt6.QtGui import QKeySequence, QShortcut
    from PyQt6.QtMultimedia import QSoundEffect
    from PyQt6.QtWidgets import QApplication, QMainWindow

    class PianoApp(QMainWindow):
        def __init__(self):
            super().__init__()
            uic.loadUi("piano.ui", self)

            self.sounds = {}
            self.key_to_note = {
                Qt.Key.Key_A: "C",
                Qt.Key.Key_S: "D",
                Qt.Key.Key_D: "E",
                Qt.Key.Key_F: "F",
                Qt.Key.Key_G: "G",
                Qt.Key.Key_H: "A",
                Qt.Key.Key_J: "B",
            }
            self.note_files = {
                "C": "C.wav",
                "D": "D.wav",
                "E": "E.wav",
                "F": "F.wav",
                "G": "G.wav",
                "A": "A.wav",
                "B": "B.wav",
            }

            self.btnC.clicked.connect(lambda: self.play_note("C"))
            self.btnD.clicked.connect(lambda: self.play_note("D"))
            self.btnE.clicked.connect(lambda: self.play_note("E"))
            self.btnF.clicked.connect(lambda: self.play_note("F"))
            self.btnG.clicked.connect(lambda: self.play_note("G"))
            self.btnA.clicked.connect(lambda: self.play_note("A"))
            self.btnB.clicked.connect(lambda: self.play_note("B"))

            self.load_sounds()
            self.setup_shortcuts()

        def load_sounds(self):
            sounds_dir = "sounds"
            if not os.path.exists(sounds_dir):
                os.makedirs(sounds_dir)
                print(
                    f"Создана папка {sounds_dir}. Поместите туда файлы: C.wav, D.wav, E.wav, F.wav, G.wav, A.wav, B.wav"
                )

            for note, filename in self.note_files.items():
                filepath = os.path.join(sounds_dir, filename)
                if os.path.exists(filepath):
                    effect = QSoundEffect()
                    effect.setSource(QUrl.fromLocalFile(filepath))
                    effect.setVolume(1.0)
                    self.sounds[note] = effect
                else:
                    print(
                        f"Файл {filepath} не найден. Звук для ноты {note} не будет воспроизводиться."
                    )

        def setup_shortcuts(self):
            for key, note in self.key_to_note.items():
                shortcut = QShortcut(QKeySequence(key), self)
                shortcut.activated.connect(lambda n=note: self.play_note(n))

        def play_note(self, note):
            if note in self.sounds:
                self.sounds[note].stop()
                self.sounds[note].play()
            else:
                print(f"Звук для ноты {note} не загружен.")

    def main():
        app = QApplication(sys.argv)
        window = PianoApp()
        window.show()
        sys.exit(app.exec())

    if __name__ == "__main__":
        main()
