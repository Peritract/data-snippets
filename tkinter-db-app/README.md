# Tkinter-db-app

This folder contains a minimal example of a TKinter GUI app that connects to a database.

## Development

There are two key files:

1. `app.py`, which contains all the Python code
2. `database.db`, which stores data

If you don't have a database.db file, running the app will create it for you.

## Running

Running `python app.py` in the command line will launch the app.

## Conversion to .exe

Running `pyinstaller -w -F --add-data "./database.db:." app.py` in the command line will convert the app to a single `.exe` file.
