""" I needed a ppm image viewer for this C++ Ray Tracing toturial:
    (https://raytracing.github.io/books/RayTracingInOneWeekend.html#overview), 
    but I couldn't find any decent one so I created this one using PyQt6...
    It's really simple, and it only supports showing images at 
    the moment with no intention of higher level functions like
    scaling, etc. """

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
QPushButton, QLabel, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap, QFont


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.main_layout = QVBoxLayout()
        self.stackedScreen = QStackedWidget()
        self.main_layout.addWidget(self.stackedScreen)

        self.selection_page = Page1()
        self.stackedScreen.addWidget(self.selection_page)

        self.selection_page.view_requested.connect(self.show_image)


        self.image_page = Page2()
        self.stackedScreen.addWidget(self.image_page)

        self.image_page.back.connect(self.going_back)

        self.container.setLayout(self.main_layout)

    @pyqtSlot(str)
    def show_image(self, image_path: str):
        if self.image_page.set_image(image_path):
            self.stackedScreen.setCurrentIndex(1)
    @pyqtSlot()
    def going_back(self):
        self.image_page.set_image('')
        self.stackedScreen.setCurrentIndex(0)
        self.resize(self.baseSize())


class Page2(QWidget):
    back = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super(Page2, self).__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        header_layout = QHBoxLayout()

        self.return_button = QPushButton('<')
        header_layout.addWidget(self.return_button, 0)
        header_layout.addWidget(QLabel('Image Viewing App!', self), 1)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.return_button.clicked.connect(self.back.emit)
        layout.addLayout(header_layout, 0)
        self.image = QLabel('IMAGE')
        layout.addWidget(self.image, 1)

        self.setLayout(layout)
    
    def set_image(self, image_path: str) -> bool:
        if image_path == '':
            self.image.setText('IMAGE')
            return True
        
        image = QImage(image_path)
        if image == None:
            QMessageBox.critical(self, 'Invalid Image', 'Cannot Load This Image')
            return False
        
        if image.size().height() > 720:
            image = image.scaledToHeight(720)
        if image.size().width() > 1280:
            image = image.scaledToWidth(720)

        self.image.setPixmap(QPixmap().fromImage(image))
        return True
        

            
class Page1(QWidget):
    view_requested = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super(Page1, self).__init__(parent)
        layout = QVBoxLayout()

        title = QLabel('Image Viewing App!')
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        button = QPushButton('Select Photo')
        button.clicked.connect(self.handle_photo_selection)

        layout.addWidget(title, 0)
        layout.addWidget(button, 1)
        self.setLayout(layout)
        

    def handle_photo_selection(self):
        path, _ = QFileDialog(self).getOpenFileName(filter='Images (*.bmp *.gif *.jpg *.png *.pbm *.pgm *.ppm *.xbm *xpm)')
        if path:
            self.view_requested.emit(path)


if __name__ == '__main__':
    from sys import argv, exit
    app = QApplication(argv)

    window = MainWindow()
    window.setFont(QFont('Helvetica', 16))

    window.show()

    exit(app.exec())
