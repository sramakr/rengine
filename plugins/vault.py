import logging,requests,json
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Vault():

	def __init__(self,**kwargs):
		self.profile=dict()	
		self.client_token=None
		for key, value in kwargs.iteritems():
			self.profile.update({key: value})
	
	def auth(self):
		print self.profile	
		try:
			if not self.profile.has_key('vault_url'):
				raise Exception('vault url manadatory')
			if not self.profile.has_key('token'):
				raise Exception('token manadatory')
			if self.profile.get('type')=='github':
				auth=requests.post(self.profile.get('vault_url')+'/auth/github/login',data=json.dumps({'token': self.profile.get('token')}))
			self.client_token=auth.json().get('auth').get('client_token')
		except Exception,e:
			logger.info(e)

	def get(self,path):
		try:
			out=requests.get(self.profile.get('vault_url')+path,headers={'X-Vault-Token': self.client_token})
			return out.json()
		except Exception,e:
			logger.info(e)	
