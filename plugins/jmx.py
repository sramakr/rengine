import re,logging
import sys
import jpype
from datastore import DataStore
from jpype import java
from jpype import javax
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class Connect_Error(Error):
    """jmx no connection """
    pass

class Attr_Error(Error):
    """jmx do not have attr """
    pass

class JMX():
    """jmx monitor class"""

    def __init__(self, host='127.0.0.1', port=8080, user='',
                 passwd=''):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.url = "service:jmx:rmi:///jndi/rmi://%s:%d/jmxrmi" % (self.host, self.port)
        self.connection = self._connect()

    def __del__(self):
        self.jmxsoc.close()

    def _connect(self):
        """make jmx connection"""
        jhash = java.util.HashMap()
        jarray = jpype.JArray(java.lang.String)([self.user,self.passwd])
        jhash.put (javax.management.remote.JMXConnector.CREDENTIALS, jarray);
        jmxurl = javax.management.remote.JMXServiceURL(self.url)
        try:
            self.jmxsoc = javax.management.remote.JMXConnectorFactory.connect(jmxurl,jhash)
            connection = self.jmxsoc.getMBeanServerConnection();
        except:
            raise Connect_Error()
        return connection

    def get_attr(self,object,type,attribute):
        """get parameter process memory ..."""
        try:
            attr = self.connection.getAttribute(javax.management.ObjectName(object), attribute)
        except Exception,e:
	    print "in attribute exception"
	    print e
            raise Attr_Error()

        return attr


def handle(config):
	try:
                flagcheck=True
                logger.info("calling jmx for metrics")
		#check for jmx hosts file
		#TODO add code for handling metrics from multiple JMX hosts	
		#
		#JAVA(libjvm='./lib/jmx/libjvm.so')
		#JAVA()
		jpype.attachThreadToJVM()
		jmx=JMX(host='96.119.153.107',port=9999)
		DS=DataStore()
                for condition in config.get('if').get('jmx'):
			baseline=DS.getbaseline(condition)
    			current=jmx.get_attr(condition.get('object'),condition.get('type'),condition.get('attribute'))
			logger.debug(current)
			logger.debug(str(current) + condition.get('operator') + repr(baseline))
			out=eval(str(current) + condition.get('operator') + repr(baseline))
			if not bool(out):
                                flagcheck=False
                                break
			DS.setbaseline(current.floatValue(),baseline,condition)
    		del jmx
                return flagcheck
        except Exception,e:
		print "in exception"
		print e
                logger.error(e)
                return False

