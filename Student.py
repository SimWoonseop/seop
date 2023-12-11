import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class MyDialog(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
		self.total = {}

	def initUI(self):
		self.label_id = QLabel('ID', self)
		self.label_id.move(100, 140)
		self.label_id.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		self.label_name = QLabel('이름', self)
		self.label_name.move(90, 220)
		self.label_name.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		self.lineEdit_id = QLineEdit(self)
		self.lineEdit_id.move(150, 140)
                         
		self.lineEdit_name = QLineEdit(self)
		self.lineEdit_name.move(150, 220)

		self.btn_save = QPushButton('저장', self)
		self.btn_save.move(600,140)
		self.btn_save.clicked.connect(self.Button_Save)

		self.btn_delete = QPushButton('삭제', self)
		self.btn_delete.move(600,220)
		self.btn_delete.clicked.connect(self.Button_Delete)

		self.btn_change = QPushButton('수정', self)
		self.btn_change.move(600,300)
		self.btn_change.clicked.connect(self.Button_Change)

		self.btn_printAll = QPushButton('전체리스트', self)
		self.btn_printAll.move(600,540)
		self.btn_printAll.clicked.connect(self.Print_All)

		

		self.tableWidget = QTableWidget(self)
		self.tableWidget.setGeometry(100,340,450,280)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(["ID", "이름"])

		self.setWindowTitle('Student')
		self.setGeometry(300,300,800,640)


		# Delete Dlg 
		self.DeleteDlg = QDialog(self)

		self.DeleteDlg_label_id = QLabel('삭제ID', self.DeleteDlg)
		self.DeleteDlg_label_id.move(100, 50)
		self.DeleteDlg_label_id.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		self.DeleteDlg_lineEdit_id = QLineEdit(self.DeleteDlg)
		self.DeleteDlg_lineEdit_id.move(150, 50)
		self.DeleteDlg_lineEdit_id.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		self.DeleteDlg_btn_Delete = QPushButton('삭제', self.DeleteDlg)
		self.DeleteDlg_btn_Delete.move(300,50)
		self.DeleteDlg_btn_Delete.clicked.connect(self.DeleteDlg_Button_Delete)

		self.DeleteDlg_btn_Close = QPushButton('확인', self.DeleteDlg)
		self.DeleteDlg_btn_Close.move(100,100)
		self.DeleteDlg_btn_Close.clicked.connect(self.DeleteDlg.close)


		# Change Dlg 
		self.ChangeDlg = QDialog(self)

		self.ChangeDlg_label_id = QLabel('수정ID', self.ChangeDlg)
		self.ChangeDlg_label_id.move(100, 50)
		self.ChangeDlg_label_id.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		self.ChangeDlg_label = QLabel('변경 할 내용 작성', self.ChangeDlg)
		self.ChangeDlg_label.move(100, 110)
		self.ChangeDlg_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		self.ChangeDlg_label_name = QLabel('이름', self.ChangeDlg)
		self.ChangeDlg_label_name.move(100, 130)
		self.ChangeDlg_label_name.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		self.ChangeDlg_lineEdit_id = QLineEdit(self.ChangeDlg)
		self.ChangeDlg_lineEdit_id.move(150, 50)
		self.ChangeDlg_lineEdit_id.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		self.ChangeDlg_lineEdit_name = QLineEdit(self.ChangeDlg)
		self.ChangeDlg_lineEdit_name.move(150, 130)
		self.ChangeDlg_lineEdit_name.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
		self.ChangeDlg_lineEdit_name.setEnabled(False)

		self.ChangeDlg_btn_Change = QPushButton('수정', self.ChangeDlg)
		self.ChangeDlg_btn_Change.move(300,50)
		self.ChangeDlg_btn_Change.clicked.connect(self.ChangeDlg_Button_Change)

	

	# Change Dlg
	def ChangeDlg_show(self):
		self.ChangeDlg.setWindowTitle('Change')
		self.ChangeDlg.setGeometry(1200,800,600,240)
		self.ChangeDlg.show()

	def ChangeDlg_Button_Change(self):
		change_id = self.ChangeDlg_lineEdit_id.text()
		if change_id in self.total.keys():
			message = QMessageBox.question(self,'Change', f'Do you want to change the information of ID {change_id}?', QMessageBox.Yes | QMessageBox.No)
			if message == QMessageBox.Yes:
				self.ChangeDlg_lineEdit_name.setEnabled(True)
				change_name = self.ChangeDlg_lineEdit_name.text()
				self.total[change_id] = [change_name]
		else:
			QMessageBox.warning(self,'Change', f'ID {change_id} does not exist!')

	# Main Dlg----------------------------------------------------------------------------------------------------------------------------------------------------
	def Button_Save(self):
		id = self.lineEdit_id.text()
		name = self.lineEdit_name.text()
		self.total[id] = [name]


	def Button_Delete(self):
		self.DeleteDlg_show()


	def Button_Change(self):
		self.ChangeDlg_show()


	def Print_All(self):
		self.tableWidget.setRowCount(len(self.total))
		for i, key in enumerate(self.total.keys()):
			self.tableWidget.setItem(i, 0, QTableWidgetItem(str(key)))
			for j, value in enumerate(self.total.get(key)):
				self.tableWidget.setItem(i, j + 1, QTableWidgetItem(str(value)))




	# Delete Dlg----------------------------------------------------------------------------------------------------------------------------------------------------
	def DeleteDlg_show(self):
		self.DeleteDlg.setWindowTitle('Delete')
		self.DeleteDlg.setGeometry(1200,800,600,240)
		self.DeleteDlg.show()

	def DeleteDlg_Button_Delete(self):
		delete_id = self.DeleteDlg_lineEdit_id.text()
		if delete_id in self.total.keys():
			message = QMessageBox.question(self,'Delete', f'Are you want to Delete ID {delete_id}?', QMessageBox.Yes | QMessageBox.No)
			if message == QMessageBox.Yes:
				del self.total[delete_id]


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyDialog()
   ex.show()
   sys.exit(app.exec_())