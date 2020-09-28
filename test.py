import os
import urllib2
from distutils.version import LooseVersion

if 'steamid64' in os.environ:
  print "steamid64:", os.environ['steamid64']
else:
  print "steamid64 was not found"

if 'modbrowserpassphrase' in os.environ:
  print "modbrowserpassphrase:", os.environ['modbrowserpassphrase']
else:
  print "modbrowserpassphrase was not found"
  
modBrowserVersionString = urllib2.urlopen("http://javid.ddns.net/tModLoader/tools/latestmodversionsimple.php?modname=BossChecklist").read().decode('utf-8')
modBrowserVersion = LooseVersion(modBrowserVersionString[1:]) # v1.0
print "Mod Browser version: " + str(modBrowserVersion)
with open("build.txt") as fh:
  for line in fh:
      if line.startswith("version"):  # version = 1.0
          buildVersion = line[line.index('=') + 1:].strip()
          print line
print "build.txt version: " + str(buildVersion)
print "Comparing versions: " + str(modBrowserVersion) + " < " + str(buildVersion)
if modBrowserVersion < buildVersion:
    print "build.txt version newer. Update needed"
    
    print "::set-env name=publishneeded::yes"
    
    open("buildneeded.txt", 'a').close()
    #not working for some reason, need to make file
    #os.environ['PUBLISHNEEDED'] = 'Yes'
    #exit(0)
else:
    print "Mod Browser up-to-date. No need to update."
    print "::set-env name=publishneeded::no"
    #os.environ['PUBLISHNEEDED'] = 'No'
    #exit(1)