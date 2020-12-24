import os
from os import environ
import sys
from urllib.request import urlopen
from distutils.version import LooseVersion

if not environ.get('INPUT_STEAMID64'):
  sys.exit("INPUT_STEAMID64 not found")
if not environ.get('INPUT_MODBROWSERPASSPHRASE'):
  sys.exit("INPUT_MODBROWSERPASSPHRASE not found")
if not environ.get('INPUT_MODNAME'):
  sys.exit("INPUT_MODNAME not found")

# TODO: Maybe allow publishing new mods too.
modBrowserVersionString = urlopen("http://javid.ddns.net/tModLoader/tools/latestmodversionsimple.php?modname=" + environ.get('INPUT_MODNAME')).read().decode('utf-8')
if not modBrowserVersionString:
  sys.exit(environ.get('INPUT_MODNAME') + " not found on the Mod Browser, are you sure you have published this mod?")

modBrowserVersion = LooseVersion(modBrowserVersionString[1:]) # v1.0
print("Mod Browser version: " + str(modBrowserVersion))
with open("build.txt") as fh:
  for line in fh:
      if line.startswith("version"):  # version = 1.0
          buildVersion = line[line.index('=') + 1:].strip()
          print(line)
print("build.txt version: " + str(buildVersion))
print("Comparing versions: " + str(modBrowserVersion) + " < " + str(buildVersion))
if modBrowserVersion < buildVersion:
    print("build.txt version newer. Update needed")
    with open(environ.get('GITHUB_ENV'), 'a') as file1: 
        file1.write("PUBLISH_NEEDED=yes") 
    #print "::set-env name=PUBLISH_NEEDED::yes"
else:
    print("Mod Browser up-to-date. No need to update.")
    with open(environ.get('GITHUB_ENV'), 'a') as file1: 
        file1.write("PUBLISH_NEEDED=no") 
    #print "::set-env name=PUBLISH_NEEDED::no"
