import sqlite3
import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QInputDialog, QLineEdit, QWidget
import sys

class BasementUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('пропуска')
        self.setGeometry(500, 500, 500, 500)
        self.name_label = QLabel('фамилия:')
        self.name_input = QLineEdit()
        self.surname_label = QLabel('имя:')
        self.surname_input = QLineEdit()
        self.patronymic_label = QLabel('отчество:')
        self.patronymic_input = QLineEdit()
        self.birthdate_label = QLabel('дата рождения:')
        self.birthdate_input = QLineEdit()
        self.pass_label = QLabel('номер пропуска:')
        self.pass_input = QLineEdit()
        self.check_button = QPushButton('пройти на работу')
        self.check_button.clicked.connect(self.vhod_pass)
        self.check_result = QLabel('')
        self.check_button1 = QPushButton('уйти с работы')
        self.check_button1.clicked.connect(self.exit)
        self.vremya = QPushButton('войти по временному пропуску')
        self.vremya.clicked.connect(self.temp_pass_vhod)
        self.exit_vremya = QPushButton('выйти по временному пропуску')
        self.exit_vremya.clicked.connect(self.temp_exit)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.surname_label)
        self.layout.addWidget(self.surname_input)
        self.layout.addWidget(self.patronymic_label)
        self.layout.addWidget(self.patronymic_input)
        self.layout.addWidget(self.birthdate_label)
        self.layout.addWidget(self.birthdate_input)
        self.layout.addWidget(self.pass_label)
        self.layout.addWidget(self.pass_input)
        self.layout.addWidget(self.check_result)
        self.layout.addWidget(self.check_button)
        self.layout.addWidget(self.vremya)
        self.layout.addWidget(self.check_button1)
        self.layout.addWidget(self.exit_vremya)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def vhod_pass(self):
        surname = self.surname_input.text()
        name = self.name_input.text()
        patronymic = self.patronymic_input.text()
        birthdate = self.birthdate_input.text()
        pass_numbers = self.pass_input.text()
        if surname and name and patronymic and birthdate and pass_numbers:
            db_connection = sqlite3.connect('base.db')
            cur = db_connection.cursor()
            cur.execute("SELECT * FROM base WHERE surname = ? AND name = ? AND patronymic = ? AND birthdate = ? AND pass = ?",(surname, name, patronymic, birthdate, pass_numbers))
            base = cur.fetchone()
            if base:
                self.check_result.setText('валидация проведена успешно.')
                time = datetime.datetime.now()
                cur.execute("UPDATE base SET time_i = ? WHERE surname = ? AND name = ? AND patronymic = ? AND birthdate = ? AND pass = ?",(time, surname, name, patronymic, birthdate, pass_numbers))
                db_connection.commit()
            else:
                self.check_result.setText('возникла ошибка, проверьте данные.')
            db_connection.close()
        else:
            self.check_result.setText('введите все данные.')

    def exit(self):
        surname = self.surname_input.text()
        name = self.name_input.text()
        patronymic = self.patronymic_input.text()
        birthdate = self.birthdate_input.text()
        pass_numbers = self.pass_input.text()
        if surname and name and patronymic and birthdate and pass_numbers:
            db_connection = sqlite3.connect('base.db')
            cur = db_connection.cursor()
            cur.execute(
                "SELECT * FROM base WHERE surname = ? AND name = ? AND patronymic = ? AND birthdate = ? AND pass = ?",
                (surname, name, patronymic, birthdate, pass_numbers))
            basement = cur.fetchone()
            if basement:
                self.check_result.setText('валидация прошла успешно.')
                time_out = datetime.datetime.now()
                cur.execute("UPDATE base SET time_o = ? WHERE surname = ? AND name = ? AND patronymic = ? AND birthdate = ? AND pass = ?",(time_out, surname, name, patronymic, birthdate, pass_numbers))
                db_connection.commit()
            else:
                self.check_result.setText('возникла ошибка, проверьте данные.')
            db_connection.close()
        else:
            self.check_result.setText('введите все данные.')

    def temp_pass_vhod(self):
        surname = self.surname_input.text()
        name = self.name_input.text()
        patronymic = self.patronymic_input.text()
        birthdate = self.birthdate_input.text()
        if surname and name and patronymic and birthdate:
            db_connection = sqlite3.connect('base.db')
            cur = db_connection.cursor()
            entry = datetime.datetime.now()
            valid, ok = QInputDialog.getInt(self, 'временный пропуск','введите количество минут для пропуска:')
            if ok:
                expiration = entry + datetime.timedelta(minutes=valid)
                cur.execute("INSERT INTO temp_passes (surname, name, patronymic, birthdate, entry, valid, expiration) VALUES (?, ?, ?, ?, ?, ?, ?)",(surname, name, patronymic, birthdate, entry, valid, expiration))
                db_connection.commit()
                self.check_result.setText('выдан пропуск до: ' + str(expiration))
            else:
                self.check_result.setText('отменили действия.')
        else:
            self.check_result.setText('введите все данные.')

    def temp_exit(self):
        surname = self.surname_input.text()
        name = self.name_input.text()
        birthdate = self.birthdate_input.text()
        patronymic = self.patronymic_input.text()
        db_connection = sqlite3.connect('base.db')
        cur = db_connection.cursor()
        cur.execute("SELECT * FROM temp_passes WHERE surname = ? AND name = ? AND birthdate = ? and patronymic = ? ",
                    (surname, name, birthdate, patronymic))
        visitor = cur.fetchone()
        if visitor:
            self.check_result.setText('Посетитель успешно вышел по временному пропуску.')
        else:
            self.check_result.setText('Пропуск не действителен. Обратитесь к старшему охраннику.')
        db_connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    basement_ui = BasementUI()
    basement_ui.show()
    sys.exit(app.exec())