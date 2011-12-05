import zipfile
import urllib2
import os
import json

tempDir = "extension_temp/"

def getExtension(fileDirectory):
    extension = open(fileDirectory)
    return extension

def unpackExtension(eID):
    extensionURL = "https://clients2.google.com/service/update2/crx?response=redirect&x=id%3D" + eID + "%26uc"
    f = urllib2.urlopen(extensionURL)
    try:
        os.mkdir(tempDir)
        os.mkdir(tempDir + eID)
        os.mkdir(tempDir + eID + "/extract")
    except:
        pass
    extensionFile = open(tempDir + eID + "/" + eID + ".crx", "wb")
    extensionFile.write(f.read())
    extensionFile.close()
    f.close()
    
    extensionFile = open(tempDir + eID + "/" + eID + ".crx", "rb")
    extension = zipfile.ZipFile(extensionFile)
    extension.extractall(tempDir + eID + "/extract")
    extensionFile.close()

def packExtension(eID):
    pass

def getScripts(eID):
    extensionDir = tempDir + eID + "/extract/"
    f = open(extensionDir + "manifest.json", 'r')
    manifest = json.load(f)
    js = []
    for script in manifest['content_scripts']:
        for files in script["js"]:
            js.append(extensionDir + str(files))
    f.close()
    return js

def getPermissions(eID):
    extensionDir = tempDir + eID + "/extract/"
    f = open(extensionDir + "manifest.json", 'r')
    manifest = json.load(f)
    perms = []
    for perm in manifest['permissions']:
        perms.append(str(perm))
    f.close()
    return perms
