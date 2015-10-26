import re,logging
import sys
import jpype
from jpype import java
from jpype import javax
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class JVM_Import_Error(Error):
    """JVM no impor. do find / | grep libjvm.so"""
    pass

class JAVA(object):
	"""start java"""
	def __init__(self,libjvm='/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.65-2.b17.el7_1.x86_64/jre/lib/amd64/server/libjvm.so'):
		try:
            		logger.debug(libjvm)
            		jpype.startJVM(libjvm)
        	except RuntimeError, e:
            		logger.error(e)
            		raise JVM_Import_Error()
