import sys
import certifi
import pendulum
import pyowm
import ssl
from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtGui import *
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

w, h = 300, 400
locator = Nominatim(user_agent='KhWeather', ssl_context=ssl.create_default_context(cafile=certifi.where()), timeout=None)
tf = TimezoneFinder()
owm = pyowm.OWM('2d8a07b2a95f38ce2b337e8146f7b609')

class RotateMe(QtWidgets.QLabel):
	def __init__(self, *args, **kwargs):
		super(RotateMe, self).__init__(*args, **kwargs)
		self._pixmap = QPixmap()
		self._animation = QtCore.QVariantAnimation(
			self,
			startValue=0.0,
			endValue=360.0,
			duration=20000,
			loopCount=-1,
			valueChanged=self.on_valueChanged
		)

	def set_pixmap(self, pixmap):
		self._pixmap = pixmap
		self.setPixmap(self._pixmap)

	@QtCore.pyqtSlot(QtCore.QVariant)
	def on_valueChanged(self, value):
		t = QTransform()
		t.rotate(value)
		self.setPixmap(self._pixmap.transformed(t))

class MainWindow:
	def __init__(self):
		self.app = QtWidgets.QApplication(sys.argv)
		self.window = QtWidgets.QMainWindow()
		self.gw, self.gh = self.app.primaryScreen().size().width(), self.app.primaryScreen().size().height()
		self._before = ''

		self.initGui()
		self.window.setWindowTitle('KhWeather')
		self.window.setFixedSize(w, h)
		self.window.move(int(self.gw / 2 - w / 2), int(self.gh / 2 - h / 2))
		self.window.setStyleSheet(open('stylesheet.css').read())
		self.window.setFont(QFont('Times'))
		self.window.show()
		sys.exit(self.app.exec_())

	def initGui(self):
		self.frameShadow = QtWidgets.QGraphicsDropShadowEffect()
		self.frameShadow.setBlurRadius(40)
		self.frameShadow.setXOffset(9)
		self.frameShadow.setYOffset(7)
		self.frameShadow.setColor(QColor(0, 0, 0, 63))

		self.sun = RotateMe(self.window, alignment=QtCore.Qt.AlignCenter)
		self.sun.setGeometry(-165, -83, 629, 626)
		self.sun.set_pixmap(QPixmap('img/sun.png'))
		self.sun.hide()

		self.cityInput = QtWidgets.QLineEdit(self.window)
		self.cityInput.setGeometry(20, 20, w - 40, 40)
		self.cityInput.setPlaceholderText('Insert your city')
		self.cityInput.editingFinished.connect(self.iChange)
		self.cityInput.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)

		self.informationFrame = QtWidgets.QFrame(self.window)
		self.informationFrame.setGeometry(20, 80, w - 40, 300)
		self.informationFrame.setGraphicsEffect(self.frameShadow)
		self.informationFrame.setObjectName('information')

		self.cloud3 = QtWidgets.QFrame(self.informationFrame)
		self.cloud3.setGeometry(-520, 0, 780, 165)
		self.cloud3.setStyleSheet('background: url(img/cloud3.png);')
		self.cloud3.hide()
		self.animCloud3 = QtCore.QPropertyAnimation(self.cloud3, b"geometry")
		self.animCloud3.setDuration(90000)
		self.animCloud3.setLoopCount(-1)
		self.animCloud3.setStartValue(QtCore.QRect(-520, 0, 780, 165))
		self.animCloud3.setEndValue(QtCore.QRect(0, 0, 780, 165))

		self.cloud2 = QtWidgets.QFrame(self.informationFrame)
		self.cloud2.setGeometry(-520, 0, 780, 140)
		self.cloud2.setStyleSheet('background: url(img/cloud2.png);')
		self.cloud2.hide()
		self.animCloud2 = QtCore.QPropertyAnimation(self.cloud2, b"geometry")
		self.animCloud2.setDuration(60000)
		self.animCloud2.setLoopCount(-1)
		self.animCloud2.setStartValue(QtCore.QRect(-520, 0, 780, 140))
		self.animCloud2.setEndValue(QtCore.QRect(0, 0, 780, 140))

		self.cloud1 = QtWidgets.QFrame(self.informationFrame)
		self.cloud1.setGeometry(-520, 0, 780, 127)
		self.cloud1.setStyleSheet('background: url(img/cloud1.png);')
		self.cloud1.hide()
		self.animCloud1 = QtCore.QPropertyAnimation(self.cloud1, b"geometry")
		self.animCloud1.setDuration(30000)
		self.animCloud1.setLoopCount(-1)
		self.animCloud1.setStartValue(QtCore.QRect(-520, 0, 780, 127))
		self.animCloud1.setEndValue(QtCore.QRect(0, 0, 780, 127))

		self.temp = QtWidgets.QLabel(self.informationFrame)
		self.temp.setGeometry(20, 6, 110, 56)
		self.temp.setObjectName('temp')
		self.temp.setAttribute(Qt.Qt.WA_TranslucentBackground, True)

		self.timeLabel = QtWidgets.QLabel(self.informationFrame)
		self.timeLabel.setGeometry(110, 16, 130, 14)
		self.timeLabel.setObjectName('time')
		self.timeLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.timeLabel.setAlignment(Qt.Qt.AlignRight)
		self.timeLabel.setAttribute(Qt.Qt.WA_TranslucentBackground, True)

		self.status = QtWidgets.QLabel(self.informationFrame)
		self.status.setGeometry(130, 42, 110, 20)
		self.status.setObjectName('status')
		self.status.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.status.setAlignment(Qt.Qt.AlignRight)
		self.status.setAttribute(Qt.Qt.WA_TranslucentBackground, True)
	def iChange(self):
		self.place = self.cityInput.text()
		reg = owm.city_id_registry()
		if not reg.ids_for(self.place):
			self.cityInput.setText('')
			self.cityInput.setPlaceholderText('No matches')
		elif self._before != self.place:
			self.observation = owm.weather_at_place(self.place)
			self.weather = self.observation.get_weather()
			self.time = self.weather.get_reference_time('date')
			self.st = self.weather.get_status()
			self.weatherBg()

			self.temp.setText(str(int(self.weather.get_temperature('celsius')['temp'])) + '<span style="font-size: 16px;">c</span>')

			self.location = locator.geocode(self.place)
			self.dt = pendulum.now(tf.timezone_at(lat=self.location.latitude, lng=self.location.longitude))
			self.timeLabel.setText(self.dt.strftime('%a, %d %b %H:%M'))
			self.status.setText(self.st)

			self._before = self.place

	def weatherBg(self):
		self.cloud3.hide()
		self.cloud2.hide()
		self.cloud1.hide()
		self.animCloud3.stop()
		self.animCloud2.stop()
		self.animCloud1.stop()
		self.sun.hide()
		self.sun._animation.stop()
		if self.st == 'Clear':
			self.informationFrame.setStyleSheet('background: url(img/clear.png);')
			self.sun.show()
			self.sun._animation.start()
		elif self.st == 'Mist' or self.st == 'Fog' or self.st == 'Drizzle':
			self.informationFrame.setStyleSheet('background: url(img/rain.png);')
		elif self.st == 'Rain' or 'Clouds' or 'Snow':
			self.cloud3.show()
			self.cloud2.show()
			self.cloud1.show()
			self.animCloud3.start()
			self.animCloud2.start()
			self.animCloud1.start()
			if self.st == 'Rain':
				self.informationFrame.setStyleSheet('background: url(img/rain.png);')
			else:
				self.informationFrame.setStyleSheet('background: url(img/wind.png);')
main = MainWindow()