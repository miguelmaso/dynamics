import numpy as np


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
