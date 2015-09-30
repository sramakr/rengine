import yaml,json,requests,logging,uuid,os,subprocess
import git
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def handle(config):
	try:
		logger.info('Starting Ansible')	
		reload_config=True  if not config.get('git').has_key('reload') else config.get('git').get('reload')
		configpath='./conf/ansible/'+config.get('git').get('repo')
		if reload_config:	
			logger.debug('Removing old config files')
			os.system('/bin/rm -r '+configpath+' > /dev/null 2>&1')
			sourceurl=config.get('git').get('url')
			if not sourceurl:
				raise Exception('source url not found')
		# init terraform
		repo=git.Repo.clone_from(sourceurl,configpath,branch='master')
		logger.debug('checking if ip address is provided in the config file')
		if config.get('params').has_key('ipaddress'):
			ipaddress=config.get('params').get('ipaddress')
		else:
			logger.debug('get the ipaddress from terraform tfstate')
			ipaddress=subprocess.check_output('./lib/terraform/terraform output ip',shell=True).strip('\n')
		logger.debug(ipaddress)
		logger.debug('printing ipaddress '+ repr(ipaddress))
	except Exception,e:
		logger.error(e)
