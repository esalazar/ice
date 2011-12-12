import zipfile
import urllib2
import os
import shutil
import json
import subprocess
import sys

# temporary directory to store current working extensions
tempDir = "extension_temp/"

# gets the extension from the file directory
def getExtension(fileDirectory):
    extension = open(fileDirectory)
    return extension

# unpacks the extension from the local directory
# or donwloads the extension first from the chrome
# web store and then unpacks it to the temporary
# working directory
def unpackExtension(eID, localFile=""):

    # if it is a local file then copy it
    if localFile != "" and os.path.exists(localFile):
        try:
            shutil.copytree(localFile, tempDir + eID + "/extract")
        except:
            shutil.rmtree(tempDir + eID + "/extract")
            shutil.copytree(localFile, tempDir + eID + "/extract")
    # else if the extension is online then download and unzip
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
        with open(tempDir + eID + "/" + eID + ".crx", "wb") as extensionFile:
            extensionFile.write(f.read())
            extensionFile.close()
            f.close()
        
        # extract crx file, which is basically a zip
        with open(tempDir + eID + "/" + eID + ".crx", "rb") as extensionFile:
            extension = zipfile.ZipFile(extensionFile)
            extension.extractall(tempDir + eID + "/extract")
            extension.close()

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

# gets the manifest file and converts it to a dictionary
def getManifest(eID):
    extensionDir = tempDir + eID + "/extract/"
    # load manifest
    with open(extensionDir + "manifest.json", 'r') as f:
        manifest = json.load(f)
    return manifest

# gets the content scripts that are specified in the manifest
def getContentScripts(eID):
    extensionDir = tempDir + eID + "/extract/"
    # load manifest
    manifest = getManifest(eID)
    js = []
    for script in manifest['content_scripts']:
        for files in script["js"]:
            js.append(extensionDir + str(files))
    return js

# gets a list of paths to any file of that type
def getFileTypes(eID, fileType):
    listFiles = []
    for r,d,f in os.walk(tempDir + eID + "/extract/"):
        for files in f:
            if files.lower().endswith(fileType):
                listFiles.append(r + "/" + files)
    return listFiles

# gets a list of permissions used
def getPermissions(eID):
    extensionDir = tempDir + eID + "/extract/"
    # load manifest
    manifest = getManifest(eID)
    perms = []
    for perm in manifest['permissions']:
        perms.append(str(perm))
    return perms

# gets the title of the extension
def getTitle(eID):
    extensionDir = tempDir + eID + "/extract/"
    # load manifest
    manifest = getManifest(eID)
    title = str(manifest["name"])
    return title

#gets the iced title
def icedTitle(eID):
    extensionDir = tempDir + eID + "/extract/"
    # load manifest
    manifest = getManifest(eID)
    manifest['description'] = "A sandboxed version of %s" % (manifest['name'])
    manifest['name'] = "Iced %s" % (manifest['name'])

    with open(extensionDir + "manifest.json", 'w') as f:
        f.write(json.dumps(manifest, indent=2))

# adds a permission to the manifest
def addPermission(eID, url):
    extensionDir = tempDir + eID + "/extract/"
    # load manifest
    manifest = getManifest(eID)
    manifest['permissions'].append(url)

    with open(extensionDir + "manifest.json", 'w') as f:
        f.write(json.dumps(manifest, indent=2))

# removes a permission from the manifest
def removePermission(eID, url):
    extensionDir = tempDir + eID + "/extract/"
    # load manifest
    manifest = getManifest(eID)
    perms = []
    for perm in manifest['permissions']:
        if url not in str(perm):
            perms.append(perm)
    manifest['permissions'] = perms

    with open(extensionDir + "manifest.json", 'w') as f:
        f.write(json.dumps(manifest, indent=2))

# removes all temporary directories and files
def cleanup():
    try:
        shutil.rmtree(tempDir)
    except:
        pass
    try:
        os.unlink("extract.pem")
    except:
        pass

