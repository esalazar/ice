import zipfile
import urllib2
import os
import shutil
import json
import subprocess
import sys

tempDir = "extension_temp/"

def getExtension(fileDirectory):
    extension = open(fileDirectory)
    return extension

def unpackExtension(eID, localFile=""):
    if localFile != "" and os.path.exists(localFile):
        shutil.copytree(localFile, tempDir + eID + "/extract")
    else:
        extensionURL = "https://clients2.google.com/service/update2/crx?response=redirect&x=id%3D" + eID + "%26uc"
        try:
            f = urllib2.urlopen(extensionURL)
        except:
            print "Unable to download extension due to invalid extension id"
            sys.exit(1)

        # make temp dir
        try:
            os.makedirs(tempDir + eID + "/extract")
        except:
            shutil.rmtree(tempDir + eID)
            os.makedirs(tempDir + eID + "/extract")
       
        # write extension to a local file
        extensionFile = open(tempDir + eID + "/" + eID + ".crx", "wb")
        extensionFile.write(f.read())
        extensionFile.close()
        f.close()
        
        # extract crx file, which is basically a zip
        extensionFile = open(tempDir + eID + "/" + eID + ".crx", "rb")
        extension = zipfile.ZipFile(extensionFile)
        extension.extractall(tempDir + eID + "/extract")
        extension.close()
        extensionFile.close()

# make use of the ruby gem `crxmake` to repack the extension
def packExtension(eID):    
    try: 
        subprocess.call(["crxmake", "--pack-extension=%s" % (tempDir + eID + "/extract"), "--extension-output=%s.crx" % (eID)])
    except:
        print "You need to install crxmake to pack chrome extensions."
        print "crxmake is a ruby gem. To use, install ruby and then execute:"
        print "    $ gem install crxmake"
        sys.exit(1)
    finally:
        shutil.rmtree(tempDir)
        os.unlink("extract.pem")

def getContentScripts(eID):
    extensionDir = tempDir + eID + "/extract/"
    f = open(extensionDir + "manifest.json", 'r')
    manifest = json.load(f)
    js = []
    for script in manifest['content_scripts']:
        for files in script["js"]:
            js.append(extensionDir + str(files))
    f.close()
    return js

def getFileTypes(eID, fileType):
    listFiles = []
    for r,d,f in os.walk(tempDir + eID + "/extract/"):
        for files in f:
            if files.lower().endswith(fileType):
                listFiles.append(r + "/" + files)
    return listFiles

def getPermissions(eID):
    extensionDir = tempDir + eID + "/extract/"
    f = open(extensionDir + "manifest.json", 'r')
    manifest = json.load(f)
    perms = []
    for perm in manifest['permissions']:
        perms.append(str(perm))
    f.close()
    return perms

def getTitle(eID):
    extensionDir = tempDir + eID + "/extract/"
    f = open(extensionDir + "manifest.json", 'r')
    manifest = json.load(f)
    title = str(manifest["name"])
    f.close()
    return title

def addPermission(eID, url):
    extensionDir = tempDir + eID + "/extract/"
    f = open(extensionDir + "manifest.json", 'r')
    manifest = json.load(f)
    manifest['permissions'].append(url)
    f.close()

    f = open(extensionDir + "manifest.json", 'w')
    f.write(json.dumps(manifest, indent=2))
    f.close()

def removePermission(eID, url):
    extensionDir = tempDir + eID + "/extract/"
    f = open(extensionDir + "manifest.json", 'r')
    manifest = json.load(f)
    perms = []
    for perm in manifest['permissions']:
        if url not in str(perm):
            perms.append(perm)
    manifest['permissions'] = perms
    f.close()

    f = open(extensionDir + "manifest.json", 'w')
    f.write(json.dumps(manifest, indent=2))
    f.close()

def cleanup():
    try:
        shutil.rmtree(tempDir)
    except:
        pass
    try:
        os.unlink("extract.pem")
    except:
        pass

