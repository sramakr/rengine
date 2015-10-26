import yaml,json,requests,logging
from brain import Brain
import dataset
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from jvm import JAVA

logging.basicConfig()
logger = logging.getLogger()
logger.getChild("brain").setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)
sched = BlockingScheduler()
db = dataset.connect('sqlite:///:memory:')

with open("conf/rule2.yaml", 'r') as stream:
    config=yaml.load(stream)


def action():
	print "hello world"
	actions=config.get('then').get('actions')
	for action in actions:
		brain=Brain(action.get('args'))
		brain.action(action.get('name'))

@sched.scheduled_job('interval', seconds=10)
def input():
	actionflg=True
	inputs=config.get('if').keys()
	for input in inputs:
		logger.debug(input)
		brain=Brain(config)
		brain.action(input)
		if not brain.outflag:
			actionflg=False
			break
	if actionflg:
		action()

#Initialize JVM if jmx metrics are being checked
if 'jmx' in config.get('if').keys():
	JAVA()
sched.start()
