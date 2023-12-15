import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
import random

class GuessNumberGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Угадай число")
        self.setGeometry(200, 200, 400, 300)

        self.secret_number = random.randint(1, 100)
        self.attempts = 5

        self.label = QLabel("Введите число от 1 до 100:", self)
        self.label.setGeometry(10, 30, 360, 40)

        self.input_box = QLineEdit(self)
        self.input_box.setGeometry(20, 60, 260, 50)
        self.submit_button = QPushButton("Проверить", self)
        self.submit_button.setGeometry(20, 100, 260, 30)
        self.submit_button.clicked.connect(self.check_number)

    def check_number(self):
        guess = int(self.input_box.text())
        self.attempts -= 1

        if guess == self.secret_number:
            self.show_message("Вы угадали число!")
            self.restart_game()
        elif self.attempts == 0:
            self.show_message(f"Вы не угадали число. Загаданное число было: {self.secret_number}")
            self.restart_game()
        elif guess < self.secret_number:
            self.show_message("Загаданное число больше")
        else:
            self.show_message("Загаданное число меньше")

        self.input_box.clear()

    def show_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setText(message)
        msg_box.setWindowTitle("Результат")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def restart_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 5

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = GuessNumberGame()
    game.show()
    sys.exit(app.exec())