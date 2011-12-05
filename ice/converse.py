import packer

allPermissions = {"bookmarks": False,
                  "clipboardRead": False,
                  "clipboardWrite": False,
                  "cookies": False,
                  "geolocation": False,
                  "history": False,
                  "idle": False,
                  "management": False}

def whitelistAdd(extension, url):
    pass

def whitelistRemove(extension, url):
    pass

def blacklistAdd(extension, url):
    pass

def blacklistRemove(extension, url):
    pass

def readBlacklist(extension):
    pass

def readWhitelist(extension):
    pass

def main():
    # ask 
    eID = raw_input("ID of Chrome Extension: ")
    packer.unpackExtension(eID)
    
    
