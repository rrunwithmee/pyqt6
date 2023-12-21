import sys
import random
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit


class DiceRollSimulator(QWidget):
    def __init__(self):
        super().__init__()


        self.title = "Million Dice Roll Statistics Simulator"
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.input_label = QLabel("Сколько кубиков?")
        layout.addWidget(self.input_label)
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        self.label_input2 = QLabel('Сколько бросков?')
        layout.addWidget(self.label_input2)
        self.label_input2 = QLineEdit()
        layout.addWidget(self.label_input2)


        self.start_button = QPushButton("Старт")
        self.start_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_button)

        self.log_output = QTextEdit()
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def simulate_dice_rolls(self, number_of_dice):
        results = {}
        for i in range(number_of_dice, (number_of_dice * 6) + 1):
            results[i] = 0

        for i in range(1000000):
            total = sum(random.randint(1, 6) for _ in range(number_of_dice))
            results[total] += 1


        for i in range(number_of_dice, (number_of_dice * 6) + 1):
            roll = results[i]
            percentage = round(results[i] / 10000, 1)
            self.log_output.append(f"{i} - {roll} бросков - {percentage}%")

    def start_simulation(self):
        number_of_dice = int(self.input_field.text())
        self.log_output.append(f"Имитация 1,000,000 {number_of_dice} бросков...")
        self.simulate_dice_rolls(number_of_dice)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiceRollSimulator()
    window.show()
    sys.exit(app.exec())



