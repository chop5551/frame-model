from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from frame import Slot, Frame
from select_job.frame_types import Job, Parameter
from select_job import DialogSetParamDesign

class ParamSetter(QtWidgets.QDialog, DialogSetParamDesign.Ui_ParamDialog):
    def __init__(self, frameApp, frame, slot):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.main_window = frameApp
        self.frame = frame
        self.slot = slot
        frameApp.setEnabled(False)
        self.model = QtGui.QStandardItemModel(self.param_list)
        items = {}
        for par in frameApp.getParams().values():
            item = QtGui.QStandardItem()
            item.setText(par.name)
            item.setCheckable(True)
            items[par.name] = item
            self.model.appendRow(item)

        for par_name in slot.value:
            if par_name in items:
                items[par_name].setCheckState(QtCore.Qt.Checked)
            
        self.param_list.setModel(self.model)

    def quit(self):
        self.main_window.setEnabled(True)
        self.hide()
        self.setEnabled(False)
        self.close()

    def accept(self):
        print("accept")
        checked = []
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            if(item.checkState()):
                checked.append(item.text())
            
        self.slot.value = checked
        self.main_window._scheme.saveToDb()
        self.main_window.printSlots()
        if(self.main_window.frame_table.selectedItems()):
            item = self.main_window.frame_table.selectedItems()[0]
            for i in reversed(range(item.childCount())):
                item.removeChild(item.child(i))
            self.main_window.showFrame(self.frame, item)
        self.quit()

    def reject(self):
        print("reject")
        self.quit()