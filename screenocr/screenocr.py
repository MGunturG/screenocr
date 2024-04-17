import sys
import time
import argparse

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from logs import log_text_copied, log_ocr_fail
from ocr_engine import check_tesseract_environment, get_ocr_result
from clipboard import copy_to_clipboard
from notification import show_notif


class SnippingTool(QtWidgets.QWidget):
    def __init__(self, parent, langs=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)

        self.setWindowTitle('ScreenOCR')
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog
        )

        self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        self._screen = QtWidgets.QApplication.screenAt(QtGui.QCursor.pos())

        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(self.getWindow()))
        self.setPalette(palette)

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        self.start, self.end = QtCore.QPoint(), QtCore.QPoint()
        self.langs = langs


    def getWindow(self):
        return self._screen.grabWindow(0)
    

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QtWidgets.QApplication.quit()

        return super().keyPressEvent(event)
    

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 100))
        painter.drawRect(0, 0, self.width(), self.height())

        if self.start == self.end:
            return super().paintEvent(event)
        
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 3))
        painter.setBrush(painter.background())
        painter.drawRect(QtCore.QRect(self.start, self.end))
        return super().paintEvent(event)
    

    def mousePressEvent(self, event):
        self.start = self.end = event.pos()
        self.update()
        return super().mousePressEvent(event)
    

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        return super().mouseMoveEvent(event)
    

    def ocrDrawRect(self):
        return get_ocr_result(
            self.getWindow().copy(
                min(self.start.x(), self.end.x()),
                min(self.start.y(), self.end.y()),
                abs(self.start.x() - self.end.x()),
                abs(self.start.y() - self.end.y()),
            ),
            self.langs,
        )
    

    def hide(self):
        super().hide()
        QtWidgets.QApplication.processEvents()


    def snipOcr(self):
        self.hide()
        ocr_result = self.ocrDrawRect()
        
        if ocr_result:
            return ocr_result
        else:
            log_ocr_fail()
        

class SingleSnip(SnippingTool):
    '''
    take single snip without delay or interval
    '''
    def mouseReleaseEvent(self, event):
        if self.start == self.end:
            return super().mouseReleaseEvent(event)
        
        ocr_result = self.snipOcr()
        if ocr_result:
            copy_to_clipboard(ocr_result)
            log_text_copied(ocr_result)
            show_notif(appid='ScreenOCR', title='Text copied!', message=ocr_result)
        else:
            log_ocr_fail()

        QtWidgets.QApplication.quit()


arg_parser = argparse.ArgumentParser(description=__doc__)
arg_parser.add_argument(
    "langs",
    nargs="?",
    default="eng",
    help="language to use, eg. eng to use english"
)
arg_parser.add_argument(
    "-i",
    "--interval",
    type=int,
    default=None,
    help="add delay before taking a screenshot in SECONDS",
)


def take_snipshot(langs, interval):
    check_tesseract_environment()

    QtCore.QCoreApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QMainWindow()

    if interval == None:
        snip = SingleSnip(window, langs)
        snip.show()
    else:
        time.sleep(interval)
        snip = SingleSnip(window, langs)
        snip.show()

    sys.exit(app.exec_())


def main():
    args = arg_parser.parse_args()
    take_snipshot(args.langs, args.interval)


if __name__ == "__main__":
    main()
