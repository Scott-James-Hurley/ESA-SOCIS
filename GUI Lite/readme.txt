# Ground Station GUI

## Introduction

## Features

- Issue preset commands
- Issue custom commands
- Set downlink(uplink will be the same)

## Built With

Tkinter
pyserial

## Getting Started

## Prerequitsites

A Python development evironment eg: [LiClipse](https://www.liclipse.com/download.html)
[Python 2.7](https://www.python.org/downloads/)
[pyserial](https://pypi.org/project/pyserial/#files)

## Installation

### Install pyserial

Using pip, execute the following command:
```<path_to_python>\python27\python.exe -m pip install pyserial```

Alternatively, download pyserial from the website, unzip the downloaded file and 
within the unzipped directory execute the following command:
```python setup.py install```

### Install GUI

Clone the Git repository using the command ```git clone https://github.com/Scott-James-Hurley/ESA-SOCIS.git```
Run the file 'main.py' either through your chosen IDE or the terminal
To run the GUI using Liclipse, launch Liclipse and select the GUI folder as your
workspace.
To run the GUI through the command line, open a command line and enter
```python <path_to_projects_main.py>```

## How To Use

To use the GUI, run main.py

First, uplink and downlink connections must be established. To do this, select 
ports you want to use for both the uplink and downlink using the drop-down menu
labelled "COM"  and enter the uplink and downlink rates in the text field to the 
immediate right of the drop-down menu. Set the connection then open it. The 
connection must be closed before another can be established.

Use the buttons at the top of the window to issue commands. Custom commands
and TLE information can be sent using the text field labelled "Command". TLE information 
must have '\r\n' separating the two lines e.g. "1 25544U 97067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927\r\n2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"
Output is displayed in the console.

## Authors

[Bence Nagy](bence@pocketqubeshop.com)

[Scott Hurley](scott.james.hurley.97@gmail.com)

## License