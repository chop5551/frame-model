from frame import Slot, Frame
__all__ = (
	'Job','Parameter'
)

class Job(Frame):
	"""
	Работа
	"""
	def __init__(self, parent=None, name=None, **slot_values):
		super().__init__(parent, name, **slot_values)
		self._slots_.update( {
			'Требования':    Slot('Требования', [], Slot.UNIQUE, "setPars"),
			'Оклад':    Slot('Оклад', '', Slot.UNIQUE)
		} )

class Parameter(Frame):
	"""
	Параметр
	"""
	def __init__(self, parent=None, name=None, **slot_values):
		super().__init__(parent, name, **slot_values)
		self._slots_.update( {
			'Навык':    Slot('Навык', '', Slot.UNIQUE),
			'Оценка':   Slot('Оценка', '', Slot.UNIQUE),
			'Стаж': Slot('Стаж', '', Slot.UNIQUE),
			'Примечание':   Slot('Примечание', '', Slot.UNIQUE)
		} )