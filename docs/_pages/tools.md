---
permalink: /tools
layout: page
title: Tools
---

**A. Jekyll include_relative**

{% include_relative owlfft-README.md %}


**B. Copy paste**

This package implements a simple GUI to calculate real positive Fourier transforms from data stored in a `.csv` file, e.g., the recording data of an accelerometer. It aimts to be an educational resource for the structural dynamics course at the [Barcelona School of Civil Engineering](https://camins.upc.edu/en).

## Installation
The recommended installation is via [pip](https://pypi.org/project/owlfft/):
```sh
pip install owlfft
```

## Usage
The package as a module from any location, like
```sh
python -m owlfft
```

Alternatively, you can create a python launcher (e.g., `fft.pyw`) to run it without opening the commandline.
```py
import owlfft
owlfft.main()
```

## Example
![](https://github.com/miguelmaso/dynamics/raw/main/tools/docs/main_window.png)

The above window will be opened. It allows to select a `.csv` file and to specify how to read it (custom delimiter, columns where to read data, etc.). There are also two range sliders to trim the time and the frequency domains. Finally, a cursor is added to the FFT spectrum plot.

## Why an owl?
Because the python project must be unique, because the author likes birds and because the name is short.

## Thanks
The author gratefully acknoledge [Flaticon](https://www.flaticon.com/free-icons/owl) for the design of the icon.


**C. xml zero-md**

<!-- This is an old try to include README.md into this page -->
<!-- https://stackoverflow.com/a/60363693 -->
<!-- Lightweight client-side loader that feature-detects and load polyfills only when necessary -->
<script src="https://cdn.jsdelivr.net/npm/@webcomponents/webcomponentsjs@2/webcomponents-loader.min.js"></script>

<!-- Load the zero-md element definition -->
<script type="module" src="https://cdn.jsdelivr.net/gh/zerodevx/zero-md@1/src/zero-md.min.js"></script>

<!-- Set the `src` attribute to the MD file -->
<zero-md src="owlfft-README.md"></zero-md>
