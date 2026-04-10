import sys

import numpy as np
import pyqtgraph as pg
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow


class FunctionPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("plotter.ui", self)

        old_placeholder = self.graph_placeholder
        layout = self.centralwidget.layout()
        index = layout.indexOf(old_placeholder)
        layout.removeWidget(old_placeholder)
        old_placeholder.deleteLater()

        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground("w")
        self.graph_widget.showGrid(x=True, y=True, alpha=0.3)
        styles = {"color": "#333", "font-size": "12pt"}
        self.graph_widget.setLabel("left", "Y", **styles)
        self.graph_widget.setLabel("bottom", "X", **styles)
        self.graph_widget.setTitle("График функции", color="#333", size="14pt")

        layout.insertWidget(index, self.graph_widget)

        self.plotButton.clicked.connect(self.plot_function)

    def plot_function(self):
        self.statusLabel.setText("")
        self.statusLabel.setStyleSheet("color: red;")

        try:
            x_min = float(self.xMinInput.text())
            x_max = float(self.xMaxInput.text())
            if x_min >= x_max:
                raise ValueError("X_min должно быть меньше X_max")
        except ValueError as e:
            self.statusLabel.setText(f"Ошибка в диапазоне X: {e}")
            return

        y_min, y_max = None, None
        if self.yMinInput.text() and self.yMaxInput.text():
            try:
                y_min = float(self.yMinInput.text())
                y_max = float(self.yMaxInput.text())
                if y_min >= y_max:
                    raise ValueError("Y_min должно быть меньше Y_max")
            except ValueError as e:
                self.statusLabel.setText(f"Ошибка в диапазоне Y: {e}")
                return

        func_str = self.funcInput.text()

        try:
            x = np.linspace(x_min, x_max, 1000)
            safe_dict = {
                "x": x,
                "np": np,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "arcsin": np.arcsin,
                "arccos": np.arccos,
                "arctan": np.arctan,
                "exp": np.exp,
                "log": np.log,
                "log10": np.log10,
                "sqrt": np.sqrt,
                "abs": np.abs,
                "pi": np.pi,
                "e": np.e,
            }
            y = eval(func_str, {"__builtins__": {}}, safe_dict)
            y = np.array(y)
            y = np.where(np.isfinite(y), y, np.nan)
        except Exception as e:
            self.statusLabel.setText(f"Ошибка в функции: {e}")
            return

        self.graph_widget.clear()
        self.graph_widget.plot(x, y, pen=pg.mkPen(color="b", width=2))

        if y_min is not None and y_max is not None:
            self.graph_widget.setYRange(y_min, y_max)
        else:
            self.graph_widget.autoRange()

        self.statusLabel.setText("График успешно построен.")
        self.statusLabel.setStyleSheet("color: green;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FunctionPlotter()
    window.show()
    sys.exit(app.exec())
