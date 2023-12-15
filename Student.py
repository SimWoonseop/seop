import sys

from PyQt5.QtGui import QCloseEvent
import sqltest
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt

mainDlg = uic.loadUiType("student_main.ui")[0]
deleteDlg = uic.loadUiType("student_delete.ui")[0]
changeDlg = uic.loadUiType("student_change.ui")[0]


# Change Dlg -------------------------------------------------------------------------------------------------------------------------------------------
class CChangeDlg(QDialog, changeDlg):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.show()
		global total
		self.change_id = 0


		self.ChangeDlg_lineEdit_name.setEnabled(False)
		self.ChangeDlg_btn_Fine.clicked.connect(self.ChangeDlg_Button_Find)
		self.ChangeDlg_btn_Change.clicked.connect(self.ChangeDlg_Button_Change)
		self.ChangeDlg_btn_Close.clicked.connect(self.close)


# Change Dlg Function-------------------------------------------------------------------------------------------------------------------------------
	# ID 찾기
	def ChangeDlg_Button_Find(self):
		self.change_id = self.ChangeDlg_lineEdit_id.text()
		if self.change_id in total.keys():
			message = QMessageBox.question(self,'Change', f'Do you want to change the information of ID {self.change_id}?', QMessageBox.Yes | QMessageBox.No)
			if message == QMessageBox.Yes:
				self.ChangeDlg_lineEdit_name.setEnabled(True)
		else:
			QMessageBox.warning(self,'Change', f'ID {self.change_id} does not exist!')

	# 내용 수정
	def ChangeDlg_Button_Change(self):
		change_name = self.ChangeDlg_lineEdit_name.text()
		message = QMessageBox.question(self,'Change', f'Do you want to change the information {change_name}?', QMessageBox.Yes | QMessageBox.No)
		if message == QMessageBox.Yes:
			total[self.change_id] = change_name
			sqltest.changeDB(change_name, self.change_id)
			

# Delete Dlg -------------------------------------------------------------------------------------------------------------------------------------------
class CDeleteDlg(QDialog, deleteDlg):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.show()

		global total

		self.DeleteDlg_btn_Delete.clicked.connect(self.DeleteDlg_Button_Delete)
		self.DeleteDlg_btn_Close.clicked.connect(self.close)

# Delete Dlg Function-------------------------------------------------------------------------------------------------------------------------------
	# 삭제
	def DeleteDlg_Button_Delete(self):
		delete_id = self.DeleteDlg_lineEdit_id.text()
		if delete_id in total.keys():
			message = QMessageBox.question(self,'Delete', f'Are you want to Delete ID {delete_id}?', QMessageBox.Yes | QMessageBox.No)
			if message == QMessageBox.Yes:
				del total[delete_id]
				sqltest.deleteDB(delete_id)
		else:
			QMessageBox.warning(self,'Delete', 'There are not ID to delete')
	

# Main Dlg -------------------------------------------------------------------------------------------------------------------------------------------
class MyDialog(QWidget, mainDlg):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		global total
		total = {}
		total = sqltest.openDB()
		self.id = 0

		self.btn_add.clicked.connect(self.Button_InformationAdd)
		self.btn_delete.clicked.connect(self.Button_DeleteDlg_Show)
		self.btn_change.clicked.connect(self.Button_ChangeDlg_Show)
		self.btn_printAll.clicked.connect(self.Print_All)
		self.btn_save.clicked.connect(self.Button_Save)
		self.btn_close.clicked.connect(self.Button_Close)

		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(["ID", "이름"])

# Main Dlg Function-------------------------------------------------------------------------------------------------------------------------------
	
	# 정보 추가
	def Button_InformationAdd(self):
		id = self.lineEdit_id.text()
		if id == '':
			QMessageBox.warning(self,'ID', 'ID를 입력해주세요')
		elif id in total.keys():
			QMessageBox.warning(self,'ID', '중복 된 ID 입니다. 다른 ID를 입력해주세요')

		name = self.lineEdit_name.text()
		if name == '':
			QMessageBox.warning(self,'이름', '이름을 입력해주세요')
		
		if id != '' and name != '':
			total[id] = name
			sqltest.intoDB(id, name)
	
	# 정보 저장
	def Button_Save(self):
		message = QMessageBox.question(self,'save', '저장하시겠습니까??', QMessageBox.Yes | QMessageBox.No)
		sqltest.saveDB(message)
		
	# 종료
	def Button_Close(self):
		result = sqltest.DB(total)
		if True == result:
			sqltest.closeDB()
			self.close()
		else:
			message = QMessageBox.question(self,'close', '변경 된 내용이 있습니다. 저장 후 종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No)
			if message == QMessageBox.Yes:
				sqltest.saveDB(message)
				sqltest.closeDB()
				self.close()
			else:
				sqltest.closeDB()
				self.close()

	# 우측상단 종료
	def closeEvent(self, a0: QCloseEvent):
		self.Button_Close()

	# 삭제 버튼 다이얼로그
	def Button_DeleteDlg_Show(self):
		deleteDlg = CDeleteDlg()
		deleteDlg.exec_()

	# 수정 버튼 다이얼로그
	def Button_ChangeDlg_Show(self):
		changeDlg = CChangeDlg()
		changeDlg.exec_()

	# 전체리스트 출력
	def Print_All(self):
		self.tableWidget.setRowCount(len(total))
		for i, key in enumerate(total.keys()):
			self.tableWidget.setItem(i, 0, QTableWidgetItem(str(key)))
			value = total.get(key)
			if isinstance(value, (list, tuple)):
				for j, v in enumerate(total.get(key)):
					self.tableWidget.setItem(i, j + 1, QTableWidgetItem(str(v)))
			else:
				self.tableWidget.setItem(i, 1, QTableWidgetItem(str(value)))


	
if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyDialog()
   ex.show()
   sys.exit(app.exec_())




   """
	def initUI(self):
		#main Dlg
		self.label_id = QLabel('ID', self)
		self.label_id.move(100, 80)
		self.label_id.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		self.label_name = QLabel('이름', self)
		self.label_name.move(90, 130)
		self.label_name.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

		self.lineEdit_id = QLineEdit(self)
		self.lineEdit_id.move(150, 140)
                         
		self.lineEdit_name = QLineEdit(self)
		self.lineEdit_name.move(150, 220)

		self.btn_add = QPushButton('추가', self)
		self.btn_add.move(600,140)
		self.btn_add.clicked.connect(self.Button_Save)

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
		self.ChangeDlg_btn_Change.move(300,80)
		self.ChangeDlg_btn_Change.clicked.connect(self.ChangeDlg_Button_Change)

		self.ChangeDlg_btn_Fine = QPushButton('확인', self.ChangeDlg)
		self.ChangeDlg_btn_Fine.move(300,50)
		self.ChangeDlg_btn_Fine.clicked.connect(self.ChangeDlg_Button_test)
"""