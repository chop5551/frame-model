from PyQt5 import QtCore, QtGui, QtWidgets
import MainWindowDesign # Это наш конвертированный файл дизайна
# import Settings
from frame import Slot, Frame
from select_job.frame_types import Job, Parameter
from select_job.procedures import Procedures

scheme_string = 'Поиск работы.'
param_string = 'Требования'
job_string = 'Вакансия'

# Имена системных слотов
NONDELETE_FRAMES = (scheme_string, param_string, job_string)

class FrameApp(QtWidgets.QWidget, MainWindowDesign.Ui_Form):
	def __init__(self):
		# Это здесь нужно для доступа к переменным, методам
		# и т.д. в файле design.py
		super().__init__()
		self.setupUi(self)  # Это нужно для инициализации нашего дизайна

		self._frames = {}
		self._scheme = Frame.loadFromDb()
		self._params = self._scheme._children_[param_string]
		self._profs = self._scheme._children_[job_string]
		
		# Загрузить список фреймов
		self.getAll()
		self.get_all_btn.clicked.connect(self.getAll)
		self.frame_table.itemSelectionChanged.connect(self.printSlots)
		self.slot_table.itemDoubleClicked.connect(self.updateSlot)

		self.add_alg_btn.clicked.connect(self.addFrame)
		self.del_alg_btn.clicked.connect(self.removeFrame)

		self.set_slot_btn.clicked.connect(self.editSlot)
		
		self.search_name_btn.clicked.connect(self.searchName)
		self.search_slot_btn.clicked.connect(self.searchSlot)

	def getParams(self):
		return self._params._children_

	def getProfs(self):
		return self._profs._children_

	def getAll(self):
		main_item = QtWidgets.QTreeWidgetItem([self._scheme._name_])
		self.showFrame(self._scheme, main_item)
		self.frame_table.clear()
		self.frame_table.addTopLevelItem(main_item)

	def printSlots(self):
		if (self.frame_table.selectedItems()):
			frame_item = self.frame_table.selectedItems()[0]
			
			if (frame_item.text(0) in self._frames):
				frame = self._frames[frame_item.text(0)]
				self.slot_table.clear()
				self.slot_table.setRowCount(0)
				i = 0
				for slot in frame._slots_.values():
					self.slot_table.setRowCount(i+1)
					new_slot = QtWidgets.QTableWidgetItem(slot._name)
					new_slot.setFlags( 
						QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
					self.slot_table.setItem(i, 0, new_slot)
					new_item = QtWidgets.QTableWidgetItem(str(slot._value))
					if slot.has_daemon:
						new_item.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
					else:
						new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled )
					self.slot_table.setItem(i, 1, QtWidgets.QTableWidgetItem(new_item))
					
					# Для масштабирования виджета таблицы
					header = self.slot_table.horizontalHeader()       
					header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
					header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
					i+=1

	def updateSlot(self, item):
		if(item.column() == 1):
			slot_name = self.slot_table.item(item.row(), 0).text()
			if (self.frame_table.selectedItems()):
				frame_item = self.frame_table.selectedItems()[0]
				if (frame_item.text(0) in self._frames):
					frame = self._frames[frame_item.text(0)]
					slot = frame._slots_[slot_name]
					if(slot.has_daemon):
						method = Procedures.getDaemon(slot.daemon)
						if(method):
							method(self, frame, slot)
	
	def editSlot(self):
		for row in range(self.slot_table.rowCount()):
			item = self.slot_table.item(row,1)
			if (item):
				value = item.text()
				slot_name = self.slot_table.item(row, 0).text()
				if (self.frame_table.selectedItems()):
					frame_item = self.frame_table.selectedItems()[0]
					if frame_item.text(0) in self._frames:
						frame = self._frames[frame_item.text(0)]
						slot = frame._slots_[slot_name]
						if (not slot.has_daemon):
							slot.value = value
							self.updateChildren(frame)
		self._scheme.saveToDb()
		self.printSlots()

	def updateChildren(self, frame):
		frame.collectSlots()
		for child in frame._children_.values():
			self.updateChildren(child)

	def searchSlot(self):
		slot_name = self.slot_name_line.text().lower()
		slot_name = slot_name[0].upper() + slot_name[1:]
		slot_value = self.slot_value_line.text().lower()
		res = self._scheme.findList(slot_value, slot_name)
		self.frame_table.clear()
		for frame in res:
			self.showResult(frame)
		else:
			self.showMessage("Ошибка!", "Не удается найти заданный фрейм по слоту!")
			

	
	def showFrame(self, frame, item):
		self._frames[item.text(0)] = frame
		Procedures.attach(self._scheme, frame, item)
		for child in frame._children_.values():
			new_item = QtWidgets.QTreeWidgetItem([child._name_])
			item.addChild(new_item)
			self.showFrame(child, new_item)

	def addFrame(self):
		name = self.name_line.text()
		if not self._scheme.find(name):
			frame = {}
			if self.alg_radio.isChecked():
				frame = Parameter(self._params, name)
				self._params.addChildren(frame)
				parent_item = self.frame_table.findItems(param_string, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
			
			elif self.task_radio.isChecked():
				frame = Job(self._profs, name)
				self._profs.addChildren(frame)
				parent_item = self.frame_table.findItems(job_string, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
			else:
				return
			
			if parent_item:
				new_item = QtWidgets.QTreeWidgetItem([frame.name])
				parent_item[0].addChild(new_item)
				self._frames[name] = frame
			self._scheme.saveToDb()
	
	def removeFrame(self):
		if self.frame_table.selectedItems():
			frame_item = self.frame_table.selectedItems()[0]
			
			if frame_item.text(0) in self._frames:
				frame = self._frames[frame_item.text(0)]
				frame.remove()
				root = self.frame_table.invisibleRootItem()
				(frame_item.parent() or root).removeChild(frame_item)
		self._scheme.saveToDb()
	
	def searchName(self):
		name = self.search_name_slot_line.text()
		name = name[0].upper() + name[1:]
		frame = self._scheme.find(name)
		self.frame_table.clear()
		self.showResult(frame)

	def showResult(self, frame):
		if frame:
			item = QtWidgets.QTreeWidgetItem([frame.name])
			self.showFrame(frame, item)
			self.frame_table.addTopLevelItem(item)
		else:
			self.showMessage("Ошибка!", "Не удается найти заданный фрейм по названию!")

	def showMessage(self, title, info):
		"""
		Выведение сообщения на экран
		"""
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle(title)
		msg.setText(info)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		msg.exec_()