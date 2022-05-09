from PySide2.QtGui import QFont
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QCheckBox
)


# Plotting imports
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

# Utilities imports
import numpy as np
import re

DEFAULT_FONT = QFont("Calibri", 15)
X_RANGE = (-1000, 1000)
DEFAULT_FUNCTION = "x"
DEFAULT_RANGE = (-10, 10)
X_LABEL = "X"
Y_LABEL = "Y"


allowedFunctions = {
    "x",
    "sin",
    "cos",
    "tan",
    "asin",
    "acos",
    "atan",
    "sinh",
    "cosh",
    "tanh",
    "exp",
    "log",
    "log10",
    "sqrt",
    "abs",
    "+",
    "-",
    "*",
    "/",
    "^",
}

stringFunctionConversions = {
    "^": "**",
    "sin": "np.sin",
    "cos": "np.cos",
    "tan": "np.tan",
    "log": "np.log",
    "exp": "np.exp",
    "sqrt": "np.sqrt",
    "abs": "np.abs",
}


class Plotter(QWidget):

    def __init__(self):
        super().__init__()

        self.initWindow("Function Plotter", 8, 8)
        self.mn, self.mx, range_setter = self.createRangeSpinBox("x")
        self.mn_y, self.mx_y, range_setter_y = self.createRangeSpinBox("y")
        function_input = self.createFunctionInputBox()
        self.setPlotGrid()
        labels_setter = self.setXYLabels()
        self.setVLayout(function_input, range_setter, range_setter_y,
                        labels_setter)
        self.createErrorDialog()

    def initWindow(self, title, width, height):
        self.setWindowTitle(title)
        self.view = FigureCanvas(Figure(figsize=(width, height)))
        self.view.figure.patch.set_facecolor('#000000')
        self.view.figure.patch.set_alpha(0.5)
        self.axes = self.view.figure.subplots()
        self.view.figure.savefig(
            'figure_theme.png', facecolor=self.view.figure.get_facecolor(), edgecolor='none')

        self.toolbar = NavigationToolbar2QT(self.view, self)

    def createRangeSpinBox(self, axis):
        mn = QDoubleSpinBox()
        mx = QDoubleSpinBox()
        mn.setPrefix("Min value for {axis}: ".format(axis=axis))
        mx.setPrefix("Max value for {axis}: ".format(axis=axis))
        mn.setFont(DEFAULT_FONT)
        mx.setFont(DEFAULT_FONT)
        mn.setRange(*X_RANGE)
        mx.setRange(*X_RANGE)
        mn.setValue(DEFAULT_RANGE[0])
        mx.setValue(DEFAULT_RANGE[1])
        range_setter = QHBoxLayout()
        range_setter.addWidget(mn)
        range_setter.addWidget(mx)
        return mn, mx, range_setter

    def createFunctionInputBox(self):
        self.function = QLineEdit()
        self.function.setFont(DEFAULT_FONT)
        self.function.setText(DEFAULT_FUNCTION)
        self.func_label = QLabel(text="Function: ")
        self.func_label.setFont(DEFAULT_FONT)
        self.submit = QPushButton(text="plot")
        self.submit.setFont(DEFAULT_FONT)
        function_input = QHBoxLayout()
        function_input.addWidget(self.func_label)
        function_input.addWidget(self.function)
        function_input.addWidget(self.submit)
        return function_input

    def setPlotGrid(self):
        self.grid = QCheckBox(text="Grid")

    def setXYLabels(self):
        self.xlabel = QLineEdit()
        self.xlabel.setFont(DEFAULT_FONT)
        self.xlabel.setText(X_LABEL)
        self.xlabel_text = QLabel(text="XLabel: ")
        self.xlabel_text.setFont(DEFAULT_FONT)
        self.ylabel = QLineEdit()
        self.ylabel.setFont(DEFAULT_FONT)
        self.ylabel.setText(Y_LABEL)
        self.ylabel_text = QLabel(text="YLabel: ")
        self.ylabel_text.setFont(DEFAULT_FONT)
        labels_setter = QHBoxLayout()
        labels_setter.addWidget(self.xlabel_text)
        labels_setter.addWidget(self.xlabel)
        labels_setter.addWidget(self.ylabel_text)
        labels_setter.addWidget(self.ylabel)
        return labels_setter

    def setVLayout(self, function_input, range_setter, range_setter_y, labels_setter):
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.toolbar)
        vlayout.addWidget(self.view)
        vlayout.addLayout(function_input)
        vlayout.addLayout(range_setter)
        vlayout.addLayout(range_setter_y)
        vlayout.addLayout(labels_setter)
        vlayout.addWidget(self.grid)
        self.setLayout(vlayout)

    def convertStringToFunction(self, string):
        for word in re.findall('[a-zA-Z_]+', string):
            if word not in allowedFunctions:
                raise TypeError("Invalid function Input")
        for key, value in stringFunctionConversions.items():
            string = string.replace(key, value)
        if "x" not in string:
            string = f"{string}+0*x"

        def func(x):
            return eval(string)

        return func

    def createErrorDialog(self):
        self.error_dialog = QMessageBox()
        self.error_dialog.setFont(DEFAULT_FONT)
        self.mn.valueChanged.connect(lambda _: self.onChange(1))
        self.mx.valueChanged.connect(lambda _: self.onChange(2))
        self.mn_y.valueChanged.connect(lambda _: self.onChange(3))
        self.mx_y.valueChanged.connect(lambda _: self.onChange(4))

        self.submit.clicked.connect(lambda _: self.onChange(5))
        self.grid.stateChanged.connect(lambda _: self.onChange(5))

    @ Slot()
    def onChange(self, index):
        x = np.linspace(X_RANGE[0], X_RANGE[1])
        if index == 1 and self.mx.value() <= self.mn.value():
            self.mx.setValue(self.mx.value()-1)
            self.error_dialog.setWindowTitle("x limits Error!")
            self.error_dialog.setText(
                "Min value cannot be greater than or equal max value")
            self.error_dialog.show()
            return

        elif index == 2 and self.mx.value() <= self.mn.value():
            self.mx.setValue(self.mn.value()+1)
            self.error_dialog.setWindowTitle("x limits Error!")
            self.error_dialog.setText(
                "Max value cannot be less than or equal min value")
            self.error_dialog.show()
            return

        if index == 3 and self.mx_y.value() <= self.mn_y.value():
            self.mx_y.setValue(self.mx_y.value()-1)
            self.error_dialog.setWindowTitle("y limits Error!")
            self.error_dialog.setText(
                "Min value cannot be greater than or equal max value")
            self.error_dialog.show()
            return

        elif index == 4 and self.mx_y.value() <= self.mn_y.value():
            self.mx_y.setValue(self.mn_y.value()+1)
            self.error_dialog.setWindowTitle("y limits Error!")
            self.error_dialog.setText(
                "Max value cannot be less than or equal min value")
            self.error_dialog.show()
            return

        elif index == 5:
            x = np.linspace(self.mn.value(), self.mx.value())
            try:
                y = self.convertStringToFunction(self.function.text())(x)
            except ValueError as e:
                self.error_dialog.setWindowTitle("Function Error!")
                self.error_dialog.setText(str(e))
                self.error_dialog.show()
                return
            except NameError as e:
                self.error_dialog.setWindowTitle("Function Error!")
                self.error_dialog.setText(str(e))
                self.error_dialog.show()
                return
            except Exception as e:
                self.error_dialog.setWindowTitle("Function Error!")
                self.error_dialog.setText(str(e))
                self.error_dialog.show()
                return

            self.axes.clear()
            self.axes.plot(x, y)
            self.axes.set_xlabel(self.xlabel.text())
            self.axes.set_ylabel(self.ylabel.text())
            self.axes.set_ylim(self.mn_y.value(), self.mx_y.value())
            self.axes.grid(self.grid.isChecked())
            self.axes.set_title(self.function.text())
            self.view.draw()
