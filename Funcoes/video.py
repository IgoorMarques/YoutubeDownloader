from pytube import YouTube as yt
from urllib.request import urlretrieve as baixar_img
from PyQt5 import QtCore


class tratar_video(QtCore.QThread):
    valor_baixado = QtCore.pyqtSignal(int)
    baixando = QtCore.pyqtSignal(str)

    def buscar(self, link):
        try:
            self.video = yt(link, on_progress_callback=self.on_progress)
        except:
            return False
        else:
            self.title = self.video.title
            return self.video, self.title, self.video.thumbnail_url

    def baixarmp4(self, video):
        video.streams.get_by_itag(22).download('./Downloads/Mp4')

    def baixarmp3(self, video):
        video.streams.get_audio_only().download('./Downloads/Mp3')

    def imgVideo(self, link):
        baixar_img(link, 'imgTeste.png')

    def on_progress(self, stream, chunk, bytes_remaining):
        """Callback function"""
        self.baixando.emit(' Baixando...')
        self.total_size = stream.filesize
        self.bytes_downloaded = self.total_size - bytes_remaining
        self.pct_completed = int(self.bytes_downloaded / self.total_size * 100)
        self.valor_baixado.emit(self.pct_completed)
        print(f"Status: {round(self.pct_completed, 2)} %")

