import yaml,json,requests,logging,uuid,os,subprocess,uuid
from vault import Vault
import git
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def getSSHKey(config):
	try:
		vault=Vault(token=config.get('vault').get('token'),type=config.get('vault').get('type'),vault_url=config.get('vault').get('url'))
		vault.auth()
		out=vault.get(config.get('vault').get('keypath'))
		pemfile='/tmp/'+str(uuid.uuid4())
		print pemfile
		fp=open(pemfile,'w')
		for line in out.get('data').get('pem').split('\n'):
			fp.write(line+'\n')
		fp.close()
		os.system('chmod 600 '+pemfile)
		return pemfile
	except Exception,e:
		logger.info(e)
	
	

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
		hostsfile='/tmp/'+str(uuid.uuid4())
		fp=open(hostsfile,'w')
		fp.write(ipaddress)
		fp.close()
		logger.debug(hostsfile)
		pemfile=getSSHKey(config)
		logger.info(pemfile)
		os.system('ansible-playbook -b --become-method=sudo -i '+hostsfile+' --private-key='+pemfile+' '+configpath+'/'+config.get('playbook'))
	except Exception,e:
		logger.error(e)
