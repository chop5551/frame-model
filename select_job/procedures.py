from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from frame import Slot, Frame
from select_job.param_setter import ParamSetter


class Procedures:
	@staticmethod
	def paramsToChildren(scheme, frame, item):
		if('Требования' in frame._slots_ and frame._slots_['Требования'].value):
			for child_name in frame._slots_['Требования'].value:
				child = scheme.find(child_name)
				if(child):
					new_item = QtWidgets.QTreeWidgetItem([child._name_])
					item.addChild(new_item)

	_dialog = None

	@staticmethod
	def setPars(frame_app, frame, slot):
		Procedures._dialog = ParamSetter(frame_app, frame, slot)
		Procedures._dialog.show()


	@staticmethod
	def attach(scheme, frame, item):
		if('Процедура' in frame._slots_ and 
			frame._slots_['Процедура'].value in _attached):
				method = _attached[frame._slots_['Процедура'].value]
				method(scheme, frame, item)

	@staticmethod
	def getDaemon(daemon_name):
		if(daemon_name in _daemons):
			return _daemons[daemon_name]
		return None

_attached = {'paramsToChildren': Procedures.paramsToChildren}
_daemons = {'setPars': Procedures.setPars}
