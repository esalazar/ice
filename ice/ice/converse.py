import packer
import rewriter
import traceback
import sys

allPermissions = {"bookmarks": False,
                  "cookies": False,
                  "geolocation": False,
                  "history": False,
                  "management": False}

def main():
    try:
        # get user input to set perms
        eID, perms = ioloop()
        # rewrite extension source
        rewriter.rewriteJs(packer.getFileTypes(eID, ".js"), allPermissions)
        rewriter.rewriteHtml(packer.getFileTypes(eID, ".html"), allPermissions)
        # repack extension
        packer.icedTitle(eID)
        packer.packExtension(eID)
    except:
        print traceback.format_tb(sys.exc_info()[2])
    finally:
        packer.cleanup()

def ioloop():
    # ask for chrome id
    eID = raw_input("ID of Chrome Extension: ")
    localFile = raw_input("Local file directory of Chrome Extension (if none press enter): ")
    packer.unpackExtension(eID, localFile)

    #ask for user to choose permissions
    for permission in packer.getPermissions(eID):
        print permission
        while 1:
            if "://" in permission and not permission == "chrome://favicon/": # must be a url
                allowUrl = raw_input("Allow " + packer.getTitle(eID) + " to access " + permission + "? [y/n]: ")
                if allowUrl in ('y','yes','Y', 'YES'):
                    break
                if allowUrl in ('n','no','N', 'NO'):
                    packer.removePermission(eID, permission)
                    break
            elif "<all_urls>" in permission:
                allowUrl = raw_input("Allow " + packer.getTitle(eID) + " to access all websites? [y/n]: ")
                if allowUrl in ('y','yes','Y', 'YES'):
                    break
                if allowUrl in ('n','no','N', 'NO'):
                    packer.removePermission(eID, permission)
                    urlAllowList = raw_input("Please list the sites to allow seperated by commas (if none then press enter): ")
                    for url in urlAllowList.split(','):
                        packer.addPermissions(eID, url)
                    break
            elif permission in allPermissions: # must be an important permission
                allow = raw_input("Allow " + packer.getTitle(eID) + " to use " + permission + "? [y/n]: ")
                if allow in ('y','yes','Y', 'YES'):
                    allPermissions[permission] = True
                    break
                if allow in ('n','no','N', 'NO'):
                    allPermissions[permission] = False
                    packer.removePermission(eID, permission)
                    break
            else: # must be an unimportant permission
                break

    return (eID, allPermissions)
    
