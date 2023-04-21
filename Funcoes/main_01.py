import os
from PyQt5 import QtGui, QtWidgets
from ui_mainwindow import Ui_MainWindow
import threading
import video


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    old_link = ''
    cod_video = "0"
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.task = video.tratar_video(self)
        self.setupUi(self)
        self.bt_baixar.clicked.connect(self.baixarvideothread)
        self.bt_pesquisar.clicked.connect(self.carregarlinkthread)
        self.bt_renomear.clicked.connect(self.renomear)
        self.bt_ver_downloads.clicked.connect(self.verDownloads)
        self.task.valor_baixado.connect(self.barra_progresso.setValue)
        self.task.baixando.connect(self.lb_choose_format.setText)
        self.task.start()

    def baixarvideothread(self):
        self.executartarefa = threading.Thread(target=self.baixar)
        self.executartarefa.start()

    def carregarlinkthread(self):
        self.carregarLink = threading.Thread(target=self.pesquisar_link)
        self.carregarLink.start()

    def pesquisar_link(self):
        self.barra_progresso.setValue(0)
        if len(self.txt_link_video.text()) > 5:
            self.lb_choose_format.setText(' Escolha o formato desejado para o arquivo: ')
            self.link = self.txt_link_video.text()
            self.achar_video = self.task.buscar(self.link)
            if self.achar_video:
                try:
                    self.txt_title_video.setText(self.achar_video.title)
                    self.task.imgVideo(self.achar_video.thumbnail_url)
                except:
                    try:
                        self.cod_video = self.nome_opcional()
                    except FileNotFoundError:
                        self.definir_nome_opcional(self.cod_video)
                        self.cod_video = self.nome_opcional()
                    self.txt_title_video.setText(f"Download-{self.cod_video}")

                self.bt_renomear.setEnabled(True)
                self.atualizarImgCentral()
                self.bt_baixar.setEnabled(True)
            else:
                self.txt_link_video.setText("Link inválido")
        elif self.txt_link_video.text() == "":
            self.txt_link_video.setText("Informe um link")
        else:
            self.txt_link_video.setText("Link inválido")

    def renomear(self):
        self.txt_title_video.setEnabled(True)
        self.txt_title_video.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "font: 8pt \"Yu Gothic UI\";")

    def atualizarImgCentral(self):
        try:
            pixmap = QtGui.QPixmap('imgTeste.png')
            img_adjusted = pixmap.scaled(531, 301)
            self.lb_img_central.setPixmap(QtGui.QPixmap(img_adjusted))
        except:
            self.txt_link_video.setText("img error")

    def baixar(self):
        self.bt_baixar.setEnabled(False)
        self.lb_choose_format.setText(' Preparando Download...')
        if self.opcao_mp4.isChecked():
            self.task.baixarmp4(self.achar_video)
        else:
            self.task.baixarmp3(self.achar_video)
        self.definir_nome_opcional(str(int(self.cod_video) + 1))
        self.lb_choose_format.setText(' Download concluído!')

    def verDownloads(self):
        os.startfile('Downloads')

    def nome_opcional(self):
        with open("cod.txt", "r") as arquivo:
            self.nome = arquivo.read()
        return self.nome

    def definir_nome_opcional(self, valor):
        with open("cod.txt", "w") as arquivo:
            arquivo.write(valor)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

