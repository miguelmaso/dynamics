"""
======
owlfft
======

Wrap scipy fft and numpy loadtxt within a simple GUI.

Author: Miguel Masó, miguel.maso@upc.edu
License: MIT License
"""
import sys, os
import numpy as np
from scipy.fft import fft, fftfreq

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QFileDialog,
    QGridLayout, QHBoxLayout, QFormLayout, QLabel, QPushButton, QLineEdit, QStatusBar)
from PyQt5.QtCore import Qt, QByteArray, QSettings
from PyQt5.QtGui import QPixmap, QIcon
from superqt import QRangeSlider

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor


class FFTCalculator():

    delimiter = ','
    time_col = 1
    acc_col = 3
    comments = '#'
    skiprows = 0

    def __init__(self):
        self.is_initialized = False

    def ReadData(self, filename):
        try:
            self._time, self._acc = np.loadtxt(filename, usecols=(self.time_col, self.acc_col),
                delimiter=self.delimiter, unpack=True, comments=self.comments, skiprows=self.skiprows)
            self._time -= self._time[0]
            self.time = self._time
            self.acc = self._acc
            self.is_initialized = True
            return ''
        except Exception as e:
            return str(e)

    def TrimTimeseries(self, limits):
        self.time = self._time[limits[0]:limits[1]]
        self.acc = self._acc[limits[0]:limits[1]]

    def TrimFrequencies(self, limits):
        self.frequencies = self._frequencies[limits[0]:limits[1]]
        self.spectrum = self._spectrum[limits[0]:limits[1]]

    def Calculate(self):
        n = len(self.time)
        self._spectrum = fft(self.acc)[:n//2]
        self._spectrum = 2/n * np.abs(self._spectrum)
        self._frequencies = fftfreq(n, (self.time[1] - self.time[0]))[:n//2]
        self.frequencies = self._frequencies
        self.spectrum = self._spectrum


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        fig = Figure(figsize=(10, 6), dpi=100, facecolor='gray')
        fig.patch.set_alpha(0.12)
        self.ax0 = fig.add_subplot(211)
        self.ax0.set_xlabel('Time (units from data)')
        self.ax0.set_ylabel('Acc (units from data)')
        self.ax1 = fig.add_subplot(212)
        self.ax1.set_xlabel('Cyclic frequency (Hz, units from data)')
        self.ax1.set_ylabel('Fourier transform')
        fig.tight_layout()
        super().__init__(fig)


class AnnotatedVCursor(Cursor):

    def __init__(self, **cursorargs):
        super().__init__(horizOn=False, useblit=True, **cursorargs)
        self.text = self.ax.text(0, 0, "0", visible=False, animated=bool(self.useblit))

    def onmove(self, event):
        super().onmove(event)
        if event.inaxes:
            self.text.set_position([event.xdata, event.ydata])
            self.text.set_text(f'{event.xdata:.2f}')
            self.text.set_visible(True)
            self.ax.draw_artist(self.text)
            self.canvas.blit(self.ax.bbox)
        else:
            self.text.set_visible(False)


class MainWindow(QMainWindow):

    message_duration = 5000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.icon = QPixmap()
        self.icon.loadFromData(QByteArray(OWL))

        self.fft = FFTCalculator()
        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle("Fourier transform")
        self.setMinimumWidth(500)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        layout = QFormLayout()
        widget = QWidget()
        widget.setLayout(layout)
        
        self.settings = QSettings(ENTITY, PROJECT)
        self.settings_widget = SettingsWidget(self)
        self.file_label = QLineEdit()
        self.file_button = QPushButton('...')
        self.settings_button = QPushButton('>_')
        self.file_button.clicked.connect(self.UpdateFilename)
        self.settings_button.clicked.connect(self.settings_widget.show)

        self.time_label = QLabel()
        self.time_slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.time_slider.valueChanged.connect(self.UpdateTime)
        self.time_slider.sliderReleased.connect(self.UpdateCalculations)

        self.frequency_label = QLabel()
        self.frequency_slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.frequency_slider.valueChanged.connect(self.UpdateFrequency)

        self.canvas = MplCanvas()
        
        container = QHBoxLayout()
        container.addWidget(self.file_label)
        container.addWidget(self.file_button)
        container.addWidget(self.settings_button)
        layout.addRow(container)
        layout.addRow(self.time_label)
        layout.addRow(self.time_slider)
        layout.addRow(self.frequency_label)
        layout.addRow(self.frequency_slider)
        layout.addRow(self.canvas)

        self.setCentralWidget(widget)
        self.update()
        self.show()

    def UpdateFilename(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', self.settings.value('dirname', os.getcwd()), 'csv files (*.csv)')[0]
        if filename:
            self.file_label.setText(filename)
            self.settings.setValue('dirname', os.path.dirname(filename))
            self.InitializeFFT()

    def InitializeFFT(self):
        msg = self.fft.ReadData(self.file_label.text())
        self.statusBar.showMessage(msg, self.message_duration)
        if self.fft.is_initialized:
            n = len(self.fft._time)
            self.time_slider.setRange(0, n)
            self.time_slider.setValue([0, n])
            self.UpdateCalculations(True)

    def UpdateTime(self):
        if self.fft.is_initialized:
            idx = self.time_slider.value()
            min_value = self.fft._time[idx[0]]
            max_value = self.fft._time[idx[1] - 1]
            self.time_label.setText(f'Time span: {min_value:.1f} to {max_value:.1f}')
            self.UpdateTimeDomainPlot()

    def UpdateTimeDomainPlot(self):
        self.fft.TrimTimeseries(self.time_slider.value())
        self.canvas.ax0.cla()
        self.canvas.ax0.plot(self.fft.time, self.fft.acc)
        self.canvas.draw()

    def UpdateCalculations(self, update_slider=False):
        if self.fft.is_initialized:
            self.fft.Calculate()
            n = len(self.fft._frequencies)
            self.frequency_slider.setRange(0, n)
            if update_slider:
                self.frequency_slider.setValue([0, n])
            self.UpdateFrequency()

    def UpdateFrequency(self):
        if self.fft.is_initialized:
            idx = self.frequency_slider.value()
            min_value = self.fft._frequencies[idx[0]]
            max_value = self.fft._frequencies[idx[1] - 1]
            self.frequency_label.setText(f'Frequency span: {min_value:.1f} to {max_value:.1f}')
            self.UpdateFrequencyDomainPlot()

    def UpdateFrequencyDomainPlot(self):
        self.fft.TrimFrequencies(self.frequency_slider.value())
        self.canvas.ax1.cla()
        self.canvas.ax1.plot(self.fft.frequencies, self.fft.spectrum)
        self.canvas.cursor = AnnotatedVCursor(ax=self.canvas.ax1, color='k', lw=.8)
        self.canvas.draw()


class SettingsWidget(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowIcon(QIcon(self.parent.icon))
        self.setWindowTitle("File settings")

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
            self.parent.fft.delimiter = str(self.delimiter.text())
            self.parent.fft.time_col = int(self.time_col.text())
            self.parent.fft.acc_col = int(self.acc_col.text())
            self.parent.fft.comments = str(self.comments.text())
            self.parent.fft.skiprows = int(self.skiprows.text())
            self.parent.settings.setValue('delimiter', str(self.delimiter.text()))
            self.parent.settings.setValue('time_col', str(self.time_col.text()))
            self.parent.settings.setValue('acc_col', str(self.acc_col.text()))
            self.parent.settings.setValue('comments', str(self.comments.text()))
            self.parent.settings.setValue('skiprows', str(self.skiprows.text()))
        except Exception as e:
            self.parent.statusBar.showMessage(str(e), self.parent.message_duration)
        if self.parent.file_label.text():
            self.parent.InitializeFFT()
        super().hideEvent(event)

ENTITY = 'ETSCCPB'
PROJECT = 'owlfft'
OWL = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x06\x00\x00\x00\x8d\x89\x1d\r\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\xf5IDAT8O\x9d\x941\x0e\x02A\x08E\xdf\xdaib<\x9c\x16\x16\x1e\xc2\xce\xce\xc6\xca\xce;X\x99\xe8\xe54\xd1N\xcd\x98e\xc3\xb2\xb0L\xdc\x8ae\x98?|\xf8\xd0\xd0\xff>@\xd3\xba\x8a=\xf6\xe98\xb1\xbb\xcbr\xf1\tL\rJ\x17\x1c<\xf4\x02fr\xc7\x06\x17\x7f\xc9l\x05\xdcZ\xbb\xf8l\xd6\xe5\x7f\t\\\xd5\xd9\x0f3\x02\xd4\xfe\rpn3X\x03\x17\xc5@\x97\xc8\x05\x94\xbaE4S\xffX\x80\x06\xaf\xb1\xab2\x9c\x00oSK\xf1I\xbd{\xa5K)$\xd2\x19\x94hL\x12^\xc34\xbe\xd6i\xa8C\t:\x01\xdb\xf6v\xf4\xe8\x11\xd8\xd9\x98\x8cr4-\x9e.\xab\x9ab)f\tT\t[@\x07"v&\xe9o@\x01O\xbb,\xda\xda\x03\x87d\x13\x15\xfaU\x80\x02\x9aM\xd1\x1cxd]\xd6\xf5\xf2\x96G\xb4/C\x1dz\xc2\xd5\x99Z\x8a\xd5\x94=\xe0\x05p7us\x01\xb3U\x9f\x8cs\xff\xf8\x0b\xb6\xafE\x14\xc5SCR\x00\x00\x00\x00IEND\xaeB`\x82'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
