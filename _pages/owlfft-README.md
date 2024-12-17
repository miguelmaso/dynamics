This package implements a simple GUI to calculate real positive Fourier transforms from data stored in a plain text file, e.g., the recording data of an accelerometer. It aims to be an educational resource for the structural dynamics course at the [Barcelona School of Civil Engineering](https://camins.upc.edu/en).

## Installation
The recommended installation is via [pip](https://pypi.org/project/owlfft/):
```sh
pip install -u owlfft
```

## Usage
The package can be called as a module from any location, like
```sh
python -m owlfft
```

Alternatively, you can create a python launcher (e.g., `fft.pyw`) to run it without opening the commandline. The file should contain the following lines:
```py
import owlfft
owlfft.main()
```

## Example
![](https://github.com/miguelmaso/dynamics/raw/main/tools/docs/main_window.png)

The above window will be opened. It allows to select a `.csv` or `.txt` file and to specify how to read it (custom delimiter, columns where to read data, etc.). There are also two range sliders to trim the time and the frequency domains. Finally, a cursor is added to the FFT spectrum plot.

## Why an owl?
Because the python project must be unique, because the author likes birds and because the name is short.

## Thanks
The author gratefully acknoledge [Flaticon](https://www.flaticon.com/free-icons/owl) for the design of the icon.
