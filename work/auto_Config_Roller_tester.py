import ConfigParser

ConfigFile = 'C:\\Users\\ChilleeChillee\\git\\testrepo\\work\\path_config.ini'

open(ConfigFile) as dfc
config = ConfigParser.ConfigParser()
config.readfp(dfc)

for sec in config.sections():
    for opt in config.options(sec):
        varName = 'self.'+sec+'_'+opt
        eval('varName')
        eval('sec')
        eval('opt')
        #exec('%s=config.get(%s,%s)' % (eval('varName'), eval('sec'),eval('opt'))