from PyQt5.QtWidgets import QPushButton


class Square(QPushButton):
    def __init__(self, x_cord=None, y_cord=None, main_mosaic=None):
        super().__init__()
        self.cord = None
        self.main_mosaic = main_mosaic

    def set_cords(self, x, y):
        self.cords = [x, y]
