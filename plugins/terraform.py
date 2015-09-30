import yaml,json,requests,logging,uuid,os
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



def handle(config):
	try:
		logger.info('Starting Terraform')	
		reload_config=True  if not config.get('git').has_key('reload') else config.get('git').get('reload')
		configpath='./conf/terraform/'+config.get('git').get('repo')
		if reload_config:	
			logger.debug('Removing old config files')
			os.system('/bin/rm -r '+configpath+' > /dev/null 2>&1')
			sourceurl=config.get('git').get('url')
			if not sourceurl:
				raise Exception('source url not found')
		# init terraform
		os.system('./lib/terraform/terraform init '+sourceurl+' '+configpath)
		logger.info('Terraform config files pulled from git')
		tf_params=[]
                for k,v in config.get('params').iteritems():
                        tf_params.append('-var '+k+'='+repr(str(v)))
		tf_parms_string=' '.join(tf_params)
		logger.info(tf_parms_string) 
		logger.info('Applying Terraform recipes')
		print './lib/terraform/terraform apply '+tf_parms_string+' '+configpath
		os.system('./lib/terraform/terraform apply '+tf_parms_string+' '+configpath)
	except Exception,e:
		logger.error(e)
