import sys
import numpy as np
from scipy.fft import fft, fftfreq

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QFileDialog,
    QGridLayout, QHBoxLayout, QFormLayout, QLabel, QPushButton, QLineEdit, QStyle)
from PyQt5.QtCore import Qt
from qtrangeslider import QRangeSlider

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        fig = Figure(figsize=(10, 6), dpi=100, facecolor='gray')
        fig.patch.set_alpha(0.12)
        self.ax0 = fig.add_subplot(211)
        self.ax0.set_xlabel('Time (units from data)')
        self.ax0.set_ylabel('Acc (units from data)')
        self.ax1 = fig.add_subplot(212)
        self.ax1.set_xlabel('Cyclic frequency (units from data)')
        self.ax1.set_ylabel('Fourier transform')
        self.vline = self.ax1.axvline(color='k', lw=0.8)
        self.text = self.ax1.text(0,0,s='')
        fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        fig.tight_layout()
        super().__init__(fig)

    def on_mouse_move(self, event):
        if event.inaxes:
            self.vline.set_xdata([event.xdata])
            self.text.set_text(f'{event.xdata:.2f}')
            self.text.set(x=event.xdata, y=event.ydata)
            self.ax1.figure.canvas.draw()


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fft = FFTCalculator()
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.setWindowTitle("Fourier transform")
        self.setMinimumWidth(500)

        layout = QFormLayout()
        widget = QWidget()
        widget.setLayout(layout)
        
        self.settings = SettingsWidget(self)
        self.file_label = QLineEdit()
        self.file_button = QPushButton('...')
        self.settings_button = QPushButton('>_')
        self.file_button.clicked.connect(self.UpdateFilename)
        self.settings_button.clicked.connect(self.settings.show)

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
        filename = QFileDialog.getOpenFileName(self, 'Open file', filter='csv files (*.csv)')[0]
        self.file_label.setText(filename)
        self.InitializeFFT()

    def InitializeFFT(self):
        self.fft.ReadData(self.file_label.text())
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
        self.canvas.vline = self.canvas.ax1.axvline(self.fft.frequencies[0], color='k', lw=0.8)
        self.canvas.text = self.canvas.ax1.text(self.fft.frequencies[0],0,s='')
        self.canvas.draw()


class SettingsWidget(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.setWindowTitle("File settings")
        
        layout = QGridLayout()
        self.setLayout(layout)

        delim_label = QLabel('Delimiter')
        self.delim = QLineEdit(self.parent.fft.delimiter)
        self.delim.setToolTip('The character used to separate the values.')
        time_col_label = QLabel('Time at column')
        self.time_col = QLineEdit(str(self.parent.fft.time_col))
        self.time_col.setToolTip('Zero-based index.')
        acc_col_label = QLabel('Acceleration at column')
        self.acc_col = QLineEdit(str(self.parent.fft.acc_col))
        self.acc_col.setToolTip('Zero-based index.')
        comments_label = QLabel('Comments')
        self.comments = QLineEdit(self.parent.fft.comments)
        self.comments.setToolTip('Character or list of characters.')
        skiprows_label = QLabel('Skiprows')
        self.skiprows = QLineEdit(str(self.parent.fft.skiprows))
        self.skiprows.setToolTip('Skip the first lines, including comments.')
        button = QPushButton('Accept')
        button.clicked.connect(self.applySettings)
        layout.addWidget(delim_label, 0, 0)
        layout.addWidget(self.delim, 0, 1)
        layout.addWidget(time_col_label, 1, 0)
        layout.addWidget(self.time_col, 1, 1)
        layout.addWidget(acc_col_label, 2, 0)
        layout.addWidget(self.acc_col, 2, 1)
        layout.addWidget(comments_label, 3, 0)
        layout.addWidget(self.comments, 3, 1)
        layout.addWidget(skiprows_label, 4, 0)
        layout.addWidget(self.skiprows, 4, 1)
        layout.addWidget(button, 5, 1)

    def applySettings(self):
        try:
            self.parent.fft.delimiter = str(self.delim.text())
            self.parent.fft.time_col = int(self.time_col.text())
            self.parent.fft.acc_col = int(self.acc_col.text())
            self.parent.fft.comments = str(self.comments.text())
            self.parent.fft.skiprows = int(self.skiprows.text())
        except Exception as e:
            print(e)
        self.hide()
        if self.parent.file_label.text():
            self.parent.InitializeFFT()


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
            self._time, self._acc = np.loadtxt(filename, delimiter=self.delimiter, usecols=(self.time_col, self.acc_col), unpack=True)
            self._time -= self._time[0]
            self.time = self._time
            self.acc = self._acc
            self.is_initialized = True
        except Exception as e:
            print(e)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
