import packer

allPermissions = {"bookmarks": False,
                  "clipboardRead": False,
                  "clipboardWrite": False,
                  "cookies": False,
                  "geolocation": False,
                  "history": False,
                  "idle": False,
                  "management": False}

def main():
    # ask for chrome id
    eID = raw_input("ID of Chrome Extension: ")
    packer.unpackExtension(eID)

    #ask for user to choose permissions
    for permission in packer.getPermissions(eID):
        print permission
        while 1:
            if "://" in permission and not permission == "chrome://favicon/": # must be a url
                allowUrl = raw_input("Allow " + packer.getTitle(eID) + " to access " + permission + "? [y/n]: ")
                if allowUrl in ('y','yes','Y', 'YES'):
                    break
                if allowUrl in ('n','no','N', 'NO'):
                    packer.removeUrlPermissions(eID, permission)
                    break
            elif "<all_urls>" in permission:
                allowUrl = raw_input("Allow " + packer.getTitle(eID) + " to access all websites? [y/n]: ")
                if allowUrl in ('y','yes','Y', 'YES'):
                    break
                if allowUrl in ('n','no','N', 'NO'):
                    packer.removeUrlPermissions(eID, permission)
                    urlAllowList = raw_input("Please list the sites to allow seperated by commas, if none then press Enter: ")
                    for url in urlAllowList:
                        packer.addUrlPermissions(eID, url)
                    break
            elif permission in allPermissions: # must be an important permission
                allow = raw_input("Allow " + packer.getTitle(eID) + " to use " + permission + "? [y/n]: ")
                if allow in ('y','yes','Y', 'YES'):
                    allPermissions[permission] = True
                    break
                if allow in ('n','no','N', 'NO'):
                    allPermissions[permission] = False
                    break
            else: # must be an unimportant permission
                break
    print allPermissions
    
    #cleanup
    packer.packExtension(eID)
    
    
