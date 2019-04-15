# noaareport

A library used to read NOAA's solar and geophysical event reports.

It uses pandas to store the data into a dataframe making it easy to manipulate.

## Installation

### Python package

```bash
pip install noaareport
```

### CLI tool

There is a very basic cli tool that can be used once the package is installed.

```bash
python -m noaareport ~/reports/2005_events 2005 03 10
```

You can use the grabit.sh script to download all the files from 1998 to 2018.
