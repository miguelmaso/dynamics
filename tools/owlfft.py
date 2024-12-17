"""
======
owlfft
======

Wrap numpy.fft and numpy.loadtxt within a simple GUI.

Author: Miguel Masó, miguel.maso@upc.edu
License: MIT License
"""
import sys, os
import numpy as np

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QFileDialog,
    QGridLayout, QHBoxLayout, QFormLayout, QLabel, QPushButton, QLineEdit, QDialog)
from PyQt5.QtCore import Qt, QByteArray, QSettings
from PyQt5.QtGui import QPixmap, QIcon
from superqt import QRangeSlider

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor

__version__ = '0.0.7'

NavigationToolbar2QT.toolitems = (('Save', 'Save the figure', 'filesave', 'save_figure'),)
NavigationToolbar2QT.set_message = lambda *_: ''


class FFTCalculator():

    delimiter = ','
    time_col = 0
    acc_col = 1
    comments = '#'
    skiprows = 0

    def __init__(self):
        self.is_initialized = False

    def ReadData(self, filename: str):
        try:
            self.delimiter = self.delimiter.replace('\\t', '\t')
            self._time, self._acc = np.loadtxt(filename, usecols=(self.time_col, self.acc_col),
                delimiter=self.delimiter, unpack=True, comments=self.comments, skiprows=self.skiprows)
            self._time -= self._time[0]
            self.time = self._time
            self.acc = self._acc
            self.is_initialized = True
            return ''
        except Exception as e:
            self.is_initialized = False
            return str(e)

    def TrimTimeseries(self, limits: tuple):
        self.time = self._time[limits[0]:limits[1]]
        self.acc = self._acc[limits[0]:limits[1]]

    def TrimFrequencies(self, limits: tuple):
        self.frequencies = self._frequencies[limits[0]:limits[1]]
        self.spectrum = self._spectrum[limits[0]:limits[1]]

    def Calculate(self):
        n = len(self.time)
        dt = self.time[1] - self.time[0]
        self._spectrum = 2/n * np.abs(np.fft.rfft(self.acc))
        self._frequencies = np.fft.rfftfreq(n, dt)
        self.frequencies = self._frequencies
        self.spectrum = self._spectrum


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        super().__init__(Figure(figsize=(10,6), facecolor='None'))
        self.setStyleSheet('background:transparent')
        self.axes = self.figure.subplots(2, 1)
        self.axes[0].set_xlabel('Time (units from data)')
        self.axes[0].set_ylabel('Acc (units from data)')
        self.axes[1].set_xlabel('Cyclic frequency (Hz, units from data)')
        self.axes[1].set_ylabel('Fourier transform')
        line0, = self.axes[0].plot([], [])
        line1, = self.axes[1].plot([], [])
        self.lines = [line0, line1]
        self.cursor = AnnotatedVCursor(ax=self.axes[1], color='k', lw=.8)
        self.figure.tight_layout()

    def UpdatePlot(self, idx, xdata, ydata):
        self.lines[idx].set_data(xdata, ydata)
        self.axes[idx].relim(visible_only=True)
        self.axes[idx].autoscale()
        self.draw()


class AnnotatedVCursor(Cursor):

    def __init__(self, **cursorargs):
        super().__init__(horizOn=False, useblit=True, **cursorargs)
        self.text = self.ax.text(0, 0, '0', visible=False, animated=bool(self.useblit))

    def onmove(self, event):
        super().onmove(event)
        if event.inaxes == self.ax:
            self.text.set_position([event.xdata, event.ydata])
            self.text.set_text(f'{event.xdata:.2f}')
            self.text.set_visible(True)
            self.ax.draw_artist(self.text)
            self.canvas.blit(self.ax.bbox)
        else:
            self.text.set_visible(False)


class MainWindow(QMainWindow):

    message_duration = 8000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.icon = QPixmap()
        self.icon.loadFromData(QByteArray(OWL))

        self.fft = FFTCalculator()
        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle('Fourier transform')
        self.setMinimumWidth(500)

        layout = QFormLayout()
        widget = QWidget()
        widget.setLayout(layout)

        self.settings = QSettings(ENTITY, PROJECT)
        self._ApplySettings()
        self.settings_dialog = SettingsDialog(self)
        self.file_label = QLineEdit()
        self.file_label.setEnabled(False)
        self.file_button = QPushButton('...')
        self.file_settings_button = QPushButton('>_')
        self.file_button.clicked.connect(self._UpdateFilename)
        self.file_settings_button.clicked.connect(self.settings_dialog.exec)

        self.time_label = QLabel()
        self.time_slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.time_slider.valueChanged.connect(self._UpdateTime)
        self.time_slider.sliderReleased.connect(self._UpdateFFT)

        self.frequency_label = QLabel()
        self.frequency_slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.frequency_slider.valueChanged.connect(self._UpdateFrequency)

        self.canvas = MplCanvas()
        toolbar = NavigationToolbar2QT(self.canvas)

        container = QHBoxLayout()
        container.addWidget(self.file_label)
        container.addWidget(self.file_button)
        container.addWidget(self.file_settings_button)
        layout.addRow(container)
        layout.addRow(self.time_label)
        layout.addRow(self.time_slider)
        layout.addRow(self.frequency_label)
        layout.addRow(self.frequency_slider)
        layout.addRow(toolbar)
        layout.addRow(self.canvas)

        self.setCentralWidget(widget)
        self.update()
        self.show()

    def _ApplySettings(self):
        self.fft.delimiter = str(self.settings.value('delimiter', self.fft.delimiter))
        self.fft.time_col = int(self.settings.value('time_col', self.fft.time_col))
        self.fft.acc_col = int(self.settings.value('acc_col', self.fft.acc_col))
        self.fft.comments = str(self.settings.value('comments', self.fft.comments))
        self.fft.skiprows = int(self.settings.value('skiprows', self.fft.skiprows))

    def _UpdateFilename(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', self.settings.value('dirname', os.getcwd()),
                                               'csv files (*.csv);;text files (*.txt);;all files (*.*)',
                                               self.settings.value('selected_filter', 'csv files (*.csv)'))[0]
        if filename:
            self.file_label.setText(filename)
            self.settings.setValue('dirname', os.path.dirname(filename))
            if filename.endswith('.csv'):
                self.settings.setValue('selected_filter', 'csv files (*.csv)')
            elif filename.endswith('.txt'):
                self.settings.setValue('selected_filter', 'text files (*.txt)')
            else:
                self.settings.setValue('selected_filter', 'all files (*.*)')
            self._InitializeFFT()

    def _InitializeFFT(self):
        msg = self.fft.ReadData(self.file_label.text())
        self.statusBar().showMessage(msg, self.message_duration)
        if self.fft.is_initialized:
            n = len(self.fft._time)
            self.time_slider.setRange(0, n)
            self.time_slider.setValue([0, n])
            self._UpdateTime()
            self._UpdateFFT(reset_slider=True)
        else:
            self._Clear()

    def _UpdateTime(self):
        if self.fft.is_initialized:
            rng = self.time_slider.value()
            min_value = self.fft._time[rng[0]]
            max_value = self.fft._time[rng[1] - 1]
            self.time_label.setText(f'Time span: {min_value:.1f} to {max_value:.1f}')
            self.fft.TrimTimeseries(rng)
            self.canvas.UpdatePlot(0, self.fft.time, self.fft.acc)

    def _UpdateFFT(self, reset_slider=False):
        if self.fft.is_initialized:
            self.fft.Calculate()
            n = len(self.fft._frequencies)
            self.frequency_slider.setRange(0, n)
            if reset_slider:
                self.frequency_slider.setValue([0, n])
            self._UpdateFrequency()

    def _UpdateFrequency(self):
        if self.fft.is_initialized:
            rng = self.frequency_slider.value()
            min_value = self.fft._frequencies[rng[0]]
            max_value = self.fft._frequencies[rng[1] - 1]
            self.frequency_label.setText(f'Frequency span: {min_value:.1f} to {max_value:.1f}')
            self.fft.TrimFrequencies(rng)
            self.canvas.UpdatePlot(1, self.fft.frequencies, self.fft.spectrum)

    def _Clear(self):
        self.canvas.UpdatePlot(0, [], [])
        self.canvas.UpdatePlot(1, [], [])


class SettingsDialog(QDialog):

    def __init__(self, parent: MainWindow):
        super().__init__()
        self.parent: MainWindow = parent
        self.setWindowIcon(QIcon(self.parent.icon))
        self.setWindowTitle('File settings')

        layout = QGridLayout()
        self.setLayout(layout)

        delimiter_label = QLabel('Delimiter')
        self.delimiter = QLineEdit()
        self.delimiter.setToolTip('The character used to separate the values.')
        time_col_label = QLabel('Time at column')
        self.time_col = QLineEdit()
        self.time_col.setToolTip('Zero-based index.')
        acc_col_label = QLabel('Acceleration at column')
        self.acc_col = QLineEdit()
        self.acc_col.setToolTip('Zero-based index.')
        comments_label = QLabel('Comments')
        self.comments = QLineEdit()
        self.comments.setToolTip('Character or list of characters.')
        skiprows_label = QLabel('Skiprows')
        self.skiprows = QLineEdit()
        self.skiprows.setToolTip('Skip the first lines, including comments.')
        button = QPushButton('Accept')
        button.clicked.connect(self.hide)
        layout.addWidget(delimiter_label, 0, 0)
        layout.addWidget(self.delimiter, 0, 1)
        layout.addWidget(time_col_label, 1, 0)
        layout.addWidget(self.time_col, 1, 1)
        layout.addWidget(acc_col_label, 2, 0)
        layout.addWidget(self.acc_col, 2, 1)
        layout.addWidget(comments_label, 3, 0)
        layout.addWidget(self.comments, 3, 1)
        layout.addWidget(skiprows_label, 4, 0)
        layout.addWidget(self.skiprows, 4, 1)
        layout.addWidget(button, 5, 1)

    def showEvent(self, event) -> None:
        self.delimiter.setText(str(self.parent.settings.value('delimiter', self.parent.fft.delimiter)))
        self.time_col.setText(str(self.parent.settings.value('time_col', self.parent.fft.time_col)))
        self.acc_col.setText(str(self.parent.settings.value('acc_col', self.parent.fft.acc_col)))
        self.comments.setText(str(self.parent.settings.value('comments', self.parent.fft.comments)))
        self.skiprows.setText(str(self.parent.settings.value('skiprows', self.parent.fft.skiprows)))
        super().showEvent(event)

    def hideEvent(self, event) -> None:
        try:
            self.parent.settings.setValue('delimiter', str(self.delimiter.text()))
            self.parent.settings.setValue('time_col', str(self.time_col.text()))
            self.parent.settings.setValue('acc_col', str(self.acc_col.text()))
            self.parent.settings.setValue('comments', str(self.comments.text()))
            self.parent.settings.setValue('skiprows', str(self.skiprows.text()))
            self.parent._ApplySettings()
            self.parent._InitializeFFT()
        except Exception as e:
            self.parent.statusBar().showMessage(str(e), self.parent.message_duration)
        super().hideEvent(event)


ENTITY = 'ETSCCPB'
PROJECT = 'owlfft'
OWL = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x18\x00\x00\x00\x18\x08\x03\x00\x00\x00\xd7\xa9\xcd\xca\x00\x00\x00BPLTEGpL\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00s\xd3\xb4\xfb\x00\x00\x00\x15tRNS\x00\x03\x11\x19+?M[fgjz\x86\x96\xa6\xb1\xbd\xca\xdb\xec\xf5\x93\xc0G\xfc\x00\x00\x00\xddIDATx\xdau\xce\xd1n\xc5 \x08\x80aT\xaa]\xab\x05A\xde\xffU\xe7<mG\x96\xec\xbf!\xfa%"\xcc\x9ab,\xac6S.\x11\xa5\xc1\'\\w\xb4\xcfh)\xc2]T\xadb\'\xc0iRU#\xdc\x85b\x1b\x84f\xc7a-\xc0f\x05\x9e\x98av\x8dq\xdd\xa7\'\xad\x80\r\x93\x8d4\x07T\xf1@F\xd0\xfb\x1aU\x7f\x81 \xf7\x0c\xf4\x19\xec`\xa4\xb5d\xadH\xc3\x81qx\xbf\xc8\xe6\x80\x07%X%2\xff\xd4\x99u\xb4\xbd\x94\xbd\r\xcd\xa7\x07HUl&5\x81\x03\xa9\xeb\xf5\xd8\xd7v\x07\xf3b\xc5\x7f\xa1\xc9\x0b\x88\x1e\xb2\xe1\x03\x17{\x08Bk\x12A\x13\x0fP,\xdfOf\xcb\x1e\x02\r\x9cc\xb3\r.\x13\x07\x10\xfb\xc8st\x89\xe1\x98\xe0\x85\x8d\x10P\xfb\xfb\xab\xfd\xee\xab\x9bI\xbb\xcc\x88\xc7\xcf\x19\xec\x9f\xbe\x01\x81\xae\x10P\nk\xe4b\x00\x00\x00\x00IEND\xaeB`\x82'


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
