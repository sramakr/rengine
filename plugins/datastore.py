import dataset,logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
db = dataset.connect('sqlite:///mydatabase.db')
table=db['workflow']


class DataStore():

   def getbaseline(self,condition):
	try:
		#get the current value from simple database
		out=self.read(condition.get('object')+condition.get('attribute'))
		logger.debug(out)
		if not out or not bool(out):
			logger.debug('hello are you here')
			self.write(condition.get('object')+condition.get('attribute'),{'metric':condition.get('object')+condition.get('attribute'),'baseline':condition.get('threshold')})
			baseline=condition.get('threshold')
		else:
			baseline=out.get('baseline')
		logger.debug(baseline)
		return baseline
	except Exception,e:
		logger.debug(e)

   def setbaseline(self,current,baseline,condition):
	try:
		decrementby=0 if not condition.has_key('decrementby') else condition.get('decrementby')
		incrementby=0 if not condition.has_key('incrementby') else condition.get('incrementby')
		logger.debug('in setbaseline')
		if (baseline - decrementby > current):
			logger.debug('in scale down code')
			# metric value decreased
			# need to scale down
			# if the current value is less than baseline minus the decrement value
			# possibly initiate a scale down
			self.write(condition.get('object')+condition.get('attribute'),{'metric':condition.get('object')+condition.get('attribute'),'baseline':baseline - decrementby })
		elif (baseline + incrementby < current):
			logger.debug('in scale up code')
			self.write(condition.get('object')+condition.get('attribute'),{'metric':condition.get('object')+condition.get('attribute'),'baseline':current } )
	except Exception,e:
		logger.debug(e)


   def write(self,metric,data):
	try:
		if table.find_one(metric=metric) :
			table.update(data,['metric'])	
		else:
			table.insert(data)
	except Exception,e:
		print e

   def read(self,metric):
	try:
		return table.find_one(metric=metric)
	except Exception,e:
		print e
