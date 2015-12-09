registry = {}

def register(Class_):
	global registry
	print('Registering')
	registry[Class_.name] = Class_()
	return Class_
