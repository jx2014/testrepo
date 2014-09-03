import ConfigParser
import re

ConfigFile = 'C:\\Users\\ChilleeChillee\\git\\testrepo\\work\\path_config.ini'

dfc = open(ConfigFile)
config = ConfigParser.ConfigParser()
config.readfp(dfc)
all_var = {}


for i in config._sections:
    for o in config.options(i):
        print i, o, config.get(i, o)



# for sec in config.sections():
#     for opt in config.options(sec):
#         all_var.update({sec: {opt:config.get(sec,opt)}})

# for sec in config.sections():
#     for opt in config.options(sec):
#         varName = 'self_'+sec+'___'+opt
# #         eval('varName')
# #         eval('sec')
# #         eval('opt')
#         exec('%s=config.get(sec, opt)' % eval('varName'))
#         print '%s : %s' % (eval('varName'), eval(eval('varName')))
#         all_var.append(str(eval('varName')))
#
# for i in all_var:
#     print '{0:<50} : {1:<10}'.format(i, eval(i))
#
# def getSection(var):
#     varPattern = '(?=^self_).*(?=___.*)'
