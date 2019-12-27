from setuptools import setup

DATA_FILES = ['img/bg.png', 'img/clear.png', 'stylesheet.css']
OPTIONS = {
    'iconfile': 'img/tornado.icns',
}

setup(
    name='KhWeather',
    version='1.0.0',
    app=['KhWeather.py'],
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)