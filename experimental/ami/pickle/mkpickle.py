import pickle
def mk():
	'''Makes a list of names from comma separated names in items.csv'''
	try:
		with open("../txt/items.csv",'rU') as f:
			items = f.read().split('\n')
			del items[items.index("")]
			items = [i.split(',') for i in items]
	except:
		pass
	try:
		with open('equipment.pickle','wb') as f:
			print items
			pickle.dump(items,f)
	except:
		pass
