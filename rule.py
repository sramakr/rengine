import yaml,json,requests,logging
from brain import Brain
logging.basicConfig()
logger = logging.getLogger()
logger.getChild("brain").setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

with open("conf/rule2.yaml", 'r') as stream:
    config=yaml.load(stream)


def action(config):
	actions=config.get('then').get('actions')
	for action in actions:
		brain=Brain(action.get('args'))
		brain.action(action.get('name'))

def input(config):
	inputs=config.get('if').keys()
	for input in inputs:
		print input
		brain=Brain(config)
		brain.action(input)

if not input(config):
	action(config)
