from PyQt6 import QtWidgets
from mendeleev import Ui_MainWindow
import csv

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.ui.tableWidget.horizontalHeader().setDefaultSectionSize(53)
        self.ui.pushButton.clicked.connect(self.on_clicked)

    def on_clicked(self):
        self.ui.textEdit.clear()
        self.ui.textEdit.clear()
        with open('periodictable.csv') as file:
            reader = csv.reader(file)
            element = list(reader)

        columns = ['Номер', 'Символ', 'Элемент', 'Название', 'Группа', 'Период', 'Вес',
                   'Плотность', 'Температура плавления', 'Температура кипения', 'Электроотрицательность',
                   'Распространенность']
        element_data = {}
        for i in element:
            element = {'Номер': i[0], 'Символ': i[1], 'Элемент': i[2], 'Название': i[3], 'Группа': i[4],
                       'Период': i[5], 'Вес': i[6], 'Плотность': i[7], 'Температура плавления': i[8], 'Температура кипения': i[9], 'Электроотрицательность': i[11], 'Распространенность': i[12]}

            element_data[i[0]] = element
            element_data[i[1]] = element

        user_input = self.ui.lineEdit.text()
        self.ui.lineEdit.clear()

        if user_input in element_data:
            for column in columns:
                true = column.rjust(max(map(len, columns)))
                self.ui.textEdit.append(true + ': ' + element_data[user_input][column])

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.resize(1050, 800)
    window.show()
    sys.exit(app.exec())
