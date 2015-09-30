# -*- coding: utf-8-*-
import logging
import pkgutil


class Brain(object):

    def __init__(self,  profile):
        """
        Instantiates a new Brain object, which cross-references user
        input with a list of modules. Note that the order of brain.modules
        matters, as the Brain will cease execution on the first module
        that accepts a given input.

        Arguments:
        profile -- contains information related to the rule
        """

        self.profile = profile
        self.modules = self.get_modules()
        self._logger = logging.getLogger(__name__)

    @classmethod
    def get_modules(cls):
        """
        Dynamically loads all the modules in the modules folder and sorts
        them by the PRIORITY key. If no PRIORITY is defined for a given
        module, a priority of 0 is assumed.
        """

        logger = logging.getLogger(__name__)
        locations = ["./plugins"]
        logger.debug("Looking for modules in: %s",
                     ', '.join(["'%s'" % location for location in locations]))
        modules = []
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except:
                logger.warning("Skipped module '%s' due to an error.", name,
                               exc_info=True)
            else:
	    	modules.append(mod)
        modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY')
                     else 0, reverse=True)
        return modules

    def action(self,plugin):
        """
        """
	NoActionModule=True
	for module in self.modules:
		if plugin == module.__name__:
			NoActionModule=False
	    		self._logger.debug("Calling action for for module %s", module.__name__)
			try:
				module.handle(self.profile)
			except:
				self._logger.error('Failed to execute module',
                                           exc_info=True)
	if NoActionModule:
        	self._logger.info("No action %r available ",plugin)
