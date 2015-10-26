import yaml,json,requests,logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def handle(config):
	try:
		flagcheck=True
		logger.info("calling influx metrics database query ")
		for k,v in config.get('if').get('influx').iteritems():
			resp=requests.get('http://localhost:8086/query?db=collectd',params={'q':'select mean(value) from '+k+' where time > now() - 10m and '+v})
			outs=resp.json()
			if not bool(outs.get('results')[0]):
				flagcheck=False
				break
		return flagcheck
	except Exception,e:
		logger.error(e)
		return False
