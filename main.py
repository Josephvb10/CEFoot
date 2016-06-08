from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from design import *
from about import *
from teams import *
from players_data import *
import sys
import time
import serial

# Inicializa la conexión a Arduno
arduino = None
try:
    arduino = serial.Serial("COM5", 9600)
except:
    pass



def confirmaSalir(self, event, porSalir=False):
    if porSalir:
        event.accept
        return

    quit_msg = "Are you sure you want to exit?"
    reply = QtWidgets.QMessageBox.question(
        self, 'Exit', quit_msg, QtWidgets.QMessageBox.Yes,
        QtWidgets.QMessageBox.No)

    if reply == QtWidgets.QMessageBox.Yes:
        event.accept()
    else:
        event.ignore()


class VentanaTitulo(QtWidgets.QMainWindow, Ui_VentanaTitulo):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.play.clicked.connect(self.jugar)
        self.exit.clicked.connect(self.salir)
        self.buttonNextsong.clicked.connect(self.nextsong)
        self.botonAbout.clicked.connect(self.abreAbout)

    def jugar(self):
        global arduino
        try:
            arduino = serial.Serial("COM5", 9600)
        except:
            pass
        if not arduino:
            QtWidgets.QMessageBox.critical(
                self, 'Error',
                "Can't stablish a connection with the gaming device.",
                QtWidgets.QMessageBox.Ok)
            self.abreSelectorEquipos()
        else:
            # Otro comentario por acá
            arduino.write(b'9')

    def reproduceMusica(self):
        self.musica2 = QtCore.QUrl.fromLocalFile("./audio/title2.mp3")
        self.musica1 = QtCore.QUrl.fromLocalFile("./audio/title.mp3")
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.playlist.addMedia(QtMultimedia.QMediaContent(self.musica2))
        self.playlist.addMedia(QtMultimedia.QMediaContent(self.musica1))
        self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.playlist.setCurrentIndex(1)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.setVolume(100)
        self.player.play()

    def salir(self):
        sys.exit()

    def nextsong(self):
        self.playlist.next()

    def abreAbout(self):
        self.aboutUi = VentanaAbout()
        self.aboutUi.show()

    def closeEvent(self, event):
        confirmaSalir(self, event)

    def abreSelectorEquipos(self):
        self.selectorUi = VentanaSelector()
        self.selectorUi.show()
        self.hide()


class VentanaAbout(QtWidgets.QMainWindow, Ui_VentanaAbout):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class VentanaSelector(QtWidgets.QMainWindow, Ui_VentanaSelector):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.continuar.clicked.connect(self.siguiente)
        self.back.clicked.connect(self.anterior)
        self.porSalir = False
        self.locales = [self.L1, self.L2, self.L3, self.L4, self.L5, self.L6]
        self.visitantes = [self.L1_2, self.L2_2,
                           self.L3_2, self.L4_2, self.L5_2, self.L6_2]

        self.L1.clicked.connect(lambda: self.seleccion("L1"))
        self.L2.clicked.connect(lambda: self.seleccion("L2"))
        self.L3.clicked.connect(lambda: self.seleccion("L3"))
        self.L4.clicked.connect(lambda: self.seleccion("L4"))
        self.L5.clicked.connect(lambda: self.seleccion("L5"))
        self.L6.clicked.connect(lambda: self.seleccion("L6"))

        self.L1_2.clicked.connect(lambda: self.seleccion("L1_2", 1))
        self.L2_2.clicked.connect(lambda: self.seleccion("L2_2", 1))
        self.L3_2.clicked.connect(lambda: self.seleccion("L3_2", 1))
        self.L4_2.clicked.connect(lambda: self.seleccion("L4_2", 1))
        self.L5_2.clicked.connect(lambda: self.seleccion("L5_2", 1))
        self.L6_2.clicked.connect(lambda: self.seleccion("L6_2", 1))

    def closeEvent(self, event):
        confirmaSalir(self, event, self.porSalir)

    def anterior(self):
        juego.show()
        self.porSalir = True
        juego.selectorUi.close()
        juego.selectorUi = None

    def seleccion(self, this, visitante=0):
        if visitante:
            juego.visitante = this

            for btn in self.locales:
                btn.setDisabled(False)

            contrario = getattr(self, this[:-2])
            contrario.setDisabled(True)

            for btn in self.visitantes:
                if this == btn.objectName():
                    btn.setChecked(True)
                    pass
                else:
                    btn.setChecked(False)
        else:
            juego.local = this

            for btn in self.visitantes:
                btn.setDisabled(False)

            contrario = getattr(self, this + "_2")
            contrario.setDisabled(True)

            for btn in self.locales:
                if this == btn.objectName():
                    btn.setChecked(True)
                    pass
                else:
                    btn.setChecked(False)

    def siguiente(self):
        return

# Inicializa el programa
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    splash_pic = QtGui.QPixmap('./images/loading.png')
    splash = QtWidgets.QSplashScreen(
        splash_pic, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pic.mask())
    splash.show()

    juego = VentanaTitulo()
    juego.reproduceMusica()
    juego.show()

    splash.finish(juego)

    sys.exit(app.exec_())
