from matplotlib.pyplot import cla
import pytest
from Plotter import Plotter


@pytest.fixture
def app(qtbot):
    plotter = Plotter()
    qtbot.addWidget(plotter)
    return plotter


@pytest.fixture(scope='function', autouse=True)
def first_app(app, request):
    request.instance.app = app


class TestPlotter:

    def test_no_errors(self, request):
        assert request.instance.app.error_dialog.isHidden() == True

    def test_figure_created(self, request):
        assert request.instance.app.view.figure is not None

    def test_input_function_default_value(self, request):
        assert request.instance.app.function.text() == "x"

    def test_input_function_is_editable(self, request):
        assert request.instance.app.function.isReadOnly() == False

    def test_input_function_changed(self, request, qtbot):
        request.instance.app.function.setText("1/x")
        assert request.instance.app.function.text() == "1/x"
        with qtbot.waitSignal(request.instance.app.submit.clicked, timeout=10000):
            request.instance.app.submit.click()

    def test_input_function_changed_to_invalid(self, request):
        request.instance.app.function.setText("np")
        request.instance.app.submit.click()
        assert request.instance.app.error_dialog.isHidden() == False

    def test_onChange_signal(self, request, qtbot):
        with qtbot.waitSignal(request.instance.app.submit.clicked, timeout=10000):
            request.instance.app.submit.click()

    def test_spinbox_range_default_value(self, request):
        assert request.instance.app.mn.value() == -10
        assert request.instance.app.mx.value() == 10
        assert request.instance.app.mn_y.value() == -10
        assert request.instance.app.mx_y.value() == 10

    def test_spinbox_is_editable(self, request):
        assert request.instance.app.mn.isReadOnly() == False

    def test_spinbox_range_changed(self, request):
        request.instance.app.mn.setValue(-1)
        request.instance.app.mx.setValue(1)
        request.instance.app.mn_y.setValue(-1)
        request.instance.app.mx_y.setValue(1)
        assert request.instance.app.mn.value() == -1
        assert request.instance.app.mx.value() == 1
        assert request.instance.app.mn_y.value() == -1
        assert request.instance.app.mx_y.value() == 1

    def test_spinbox_range_changed_to_invalid(self, request):
        request.instance.app.mn.setValue(1)
        request.instance.app.mx.setValue(1)
        assert request.instance.app.error_dialog.isHidden() == False

    def test_onChange_signal_spinbox(self, request, qtbot):
        with qtbot.waitSignal(request.instance.app.mn.valueChanged, timeout=1000):
            request.instance.app.mn.setValue(1)

    def test_xlabel(self, request):
        request.instance.app.xlabel.setText("x")
        assert request.instance.app.xlabel.text() == "x"

    def test_ylabel(self, request):
        request.instance.app.ylabel.setText("y")
        assert request.instance.app.ylabel.text() == "y"
