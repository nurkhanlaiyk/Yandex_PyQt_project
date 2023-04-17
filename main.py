import sys

import csv
import time
import datetime
from random import randint
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QDialog, QTableWidgetItem
from PyQt5.QtCore import Qt, QEvent, QTimer
from main_view import Ui_MainWindow
from dialogues import Ui_SaveDialog
#    scoreboard_dialogues.py
from scoreboard_dialogues import Ui_Scoreboard
from squares import Square


class Numbers(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Numbers, self).__init__(parent=parent)
        self.setupUi(self)
        self.squares = [[None for _ in range(4)] for _ in range(4)]
        # self.pushButton.isEnabled()
        for i in range(4):
            for j in range(4):
                button_num = 4 * i + j + 1
                button_name = 'pushButton' + ('_' + str(button_num) if button_num > 1 else '')
                qt_button = getattr(self, button_name)
                qt_button.__class__ = Square
                qt_button.set_cords(i, j)
                qt_button.clicked.connect(self.square_click)
                self.squares[i][j] = qt_button
        self.pushButton_17.clicked.connect(self.new_game)
        self.space_cords = [3, 3]
        self.squares[3][3].setVisible(False)
        self.start_time = None
        self.end_time = None
        self.timer = None
        self.time_cnt = 0
        self.pushButton_19.clicked.connect(self.scoreboard)
        self.pushButton_18.clicked.connect(self.reset_game)
        qApp.installEventFilter(self)

    def move(self, square):
        val = square.text()
        if square.cords[1] == self.space_cords[1] or square.cords[0] == self.space_cords[0]:
            cord = 0 if square.cords[1] == self.space_cords[1] else 1
            direc = 1 if self.space_cords[cord] > square.cords[cord] else -1
            for i in range(square.cords[cord], self.space_cords[cord], direc):
                if cord == 0:
                    temp_val = self.squares[i + direc][square.cords[1]].text()
                    self.squares[i + direc][square.cords[1]].setText(val)
                else:
                    temp_val = self.squares[square.cords[0]][i + direc].text()
                    self.squares[square.cords[0]][i + direc].setText(val)
                val = temp_val
            self.squares[self.space_cords[0]][self.space_cords[1]].setEnabled(True)
            self.squares[self.space_cords[0]][self.space_cords[1]].setVisible(True)
            square.setEnabled(False)
            square.setText('space')
            square.setVisible(False)
            self.space_cords[0] = square.cords[0]
            self.space_cords[1] = square.cords[1]

    def square_click(self):
        self.move(self.sender())
        self.check_end()

    def new_game(self):
        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()
        self.shuffle()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)
        self.start_time = time.time()
        self.time_cnt = 0
        self.label.setText("Time passed (sec): " + str(self.time_cnt))

    def shuffle(self):
        for t in range(16*10):
            if t % 2:
                possible_cords = [i for i in range(4) if i != self.space_cords[0]]
                rnd_cord = possible_cords[randint(0, 2)]
                self.move(self.squares[rnd_cord][self.space_cords[1]])
            else:
                possible_cords = [j for j in range(4) if j != self.space_cords[1]]
                rnd_cord = possible_cords[randint(0, 2)]
                self.move(self.squares[self.space_cords[1]][rnd_cord])

    def check_end(self):
        if self.start_time is not None and self.check_mosaic():
            self.end_game()

    def end_game(self):
        if self.start_time is not None:
            time_data = time.time() - self.start_time
            self.start_time = None
            self.label.setText("Your time (sec): " + str(round(time_data, 2)))
        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None
        self.time_cnt = 0
        save_dialog = SaveDialog(self, score=round(time_data, 2))
        if save_dialog.exec():
            with open('scoreboard.txt', 'a+', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter='$')
                writer.writerow([save_dialog.lineEdit.text(), save_dialog.label_5.text(), save_dialog.label_4.text()])
        self.label.setText('Press "New Game" to start new game')

    def reset_game(self):
        self.start_time = None
        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None
        self.label.setText('Press "New Game" to start new game')
        for i in range(4):
            for j in range(4):
                button_num = 4 * i + j + 1
                if button_num < 16:
                    self.squares[i][j].setText(str(button_num))
                    if not self.squares[i][j].isEnabled():
                        self.squares[i][j].setVisible(True)
                        self.squares[i][j].setEnabled(True)
        self.squares[3][3].setVisible(False)
        self.squares[3][3].setEnabled(False)
        self.squares[3][3].setText('space')
        self.space_cords = [3, 3]

    def check_mosaic(self):
        for i in range(4):
            for j in range(4):
                button_num = 4 * i + j + 1
                if button_num < 16 and self.squares[i][j].text() != str(button_num):
                    return False
        return True

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Up and self.space_cords[0] + 1 < 4:
                self.move(self.squares[self.space_cords[0] + 1][self.space_cords[1]])
            elif event.key() == Qt.Key_Down and self.space_cords[0] - 1 >= 0:
                self.move(self.squares[self.space_cords[0] - 1][self.space_cords[1]])
            elif event.key() == Qt.Key_Right and self.space_cords[1] - 1 >= 0:
                self.move(self.squares[self.space_cords[0]][self.space_cords[1] - 1])
            elif event.key() == Qt.Key_Left and self.space_cords[1] + 1 < 4:
                self.move(self.squares[self.space_cords[0]][self.space_cords[1] + 1])
            else:
                return super(Numbers, self).eventFilter(source, event)
            self.check_end()
            return True
        return super(Numbers, self).eventFilter(source, event)

    def tick(self):
        self.time_cnt += 1
        self.label.setText("Time passed (sec): " + str(self.time_cnt))

    def scoreboard(self):
        scoreBoard = ScoreboardDialog(self)
        scoreBoard.exec()


class SaveDialog(QDialog, Ui_SaveDialog):
    def __init__(self, *args, score=0.0):
        super().__init__(*args)
        self.setupUi(self)
        self.label_4.setText(str(score))
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)
        self.label_5.setText(str(datetime.datetime.now()))


class ScoreboardDialog(QDialog, Ui_Scoreboard):
    def __init__(self, *args, score=0.0):
        super().__init__(*args)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)
        with open('scoreboard.txt', 'r', encoding='utf-8') as csv_file:
            rows = list(csv.reader(csv_file, delimiter='$'))
            for id, row in enumerate(rows):
                self.tableWidget.insertRow(id)
                for col_id, col in enumerate(row):
                    self.tableWidget.setItem(id, col_id, QTableWidgetItem(col))


def main():
    app = QApplication(sys.argv)
    wind = Numbers()
    wind.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
