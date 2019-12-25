from setuptools import setup

APP = ['KhWeather.py']
DATA_FILES = ['bg.png', 'clear.png', 'stylesheet.css']
OPTIONS = {
    'iconfile': 'tornado.icns',
    'argv_emulation': True,
    'packages': ['PyQt5']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['PyQt5', 'certifi', 'pendulum', 'pyowm', 'geopy', 'timezonefinder']
)