import sys
import certifi
import pendulum
import pyowm
import ssl
from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

locator = Nominatim(user_agent='KhWeather', ssl_context=ssl.create_default_context(cafile=certifi.where()))
tf = TimezoneFinder()
w = 300
h = 400
owm = pyowm.OWM('2d8a07b2a95f38ce2b337e8146f7b609')

class MainWindow:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.gw = self.app.primaryScreen().size().width()
        self.gh = self.app.primaryScreen().size().height()
        self.frameShadow = QtWidgets.QGraphicsDropShadowEffect()
        self.frameShadow.setBlurRadius(40)
        self.frameShadow.setXOffset(9)
        self.frameShadow.setYOffset(7)
        self.frameShadow.setColor(QtGui.QColor(0, 0, 0, 63))

        self.initGui()
        self.window.setWindowTitle('KhWeather')
        self.window.setFixedSize(w, h)
        self.window.move(int(self.gw / 2 - w / 2), int(self.gh / 2 - h / 2))
        self.window.setStyleSheet(open('stylesheet.css').read())
        self.window.setFont(QtGui.QFont('Arial'))
        self.window.show()
        sys.exit(self.app.exec_())

    def initGui(self):
        self.cityInput = QtWidgets.QLineEdit(self.window)
        self.cityInput.setGeometry(20, 20, w - 40, 40)
        self.cityInput.setPlaceholderText('Insert your city')
        self.cityInput.editingFinished.connect(self.iChange)
        self.cityInput.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)

        self.informationFrame = QtWidgets.QFrame(self.window)
        self.informationFrame.setGeometry(20, 80, w - 40, 300)
        self.informationFrame.setGraphicsEffect(self.frameShadow)

        self.temp = QtWidgets.QLabel(self.informationFrame)
        self.temp.setGeometry(20, 6, 110, 56)
        self.temp.setObjectName('temp')

        self.timeLabel = QtWidgets.QLabel(self.informationFrame)
        self.timeLabel.setGeometry(110, 16, 130, 14)
        self.timeLabel.setObjectName('time')
        self.timeLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.timeLabel.setAlignment(Qt.Qt.AlignRight)

        self.status = QtWidgets.QLabel(self.informationFrame)
        self.status.setGeometry(130, 42, 110, 20)
        self.status.setObjectName('status')
        self.status.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.status.setAlignment(Qt.Qt.AlignRight)

    def iChange(self):
        self.place = self.cityInput.text()
        reg = owm.city_id_registry()
        if not reg.ids_for(self.place):
            self.cityInput.setText('')
            self.cityInput.setPlaceholderText('No matches')
        else:
            self.observation = owm.weather_at_place(self.place)
            self.weather = self.observation.get_weather()
            self.time = self.weather.get_reference_time('date')

            self.temp.setText(str(int(self.weather.get_temperature('celsius')['temp'])) +
                              '<span style="font-size: 16px;">c</span>')

            self.location = locator.geocode(self.place)
            self.dt = pendulum.now(tf.timezone_at(lat=self.location.latitude, lng=self.location.longitude))
            self.timeLabel.setText(self.dt.strftime('%a, %d %b %H:%M'))

            self.status.setText(self.weather.get_status())
            self.informationFrame.setStyleSheet('background: ' + str({
                'Clear':   'url(clear.png)',
                'Rain':    '#9FA4AD; color: #dddddd',
                'Mist':    '#efefef',
                'Fog':     '#9FA4AD; color: #dddddd',
                'Drizzle': '#D5D5D5'
            }.get(self.weather.get_status(), '#dae3fd')) + ';')

main = MainWindow()