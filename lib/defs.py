class Test:
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)
		self.questions = None

class Struct:
	def __init__(self, **kwargs): self.__dict__.update(kwargs)
	def __str__(self):
		return str(self.__dict__)
	__repr__ = __str__