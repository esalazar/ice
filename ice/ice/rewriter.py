# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# this module is responsible for rewriting chrome javascript source files.
# Modifcations it makes are:
# * All chrome identifiers are replaced with wrapped_chrome
# * geolocation identifiers are replaced with wrapped_geolocation
# * disallow access to __proto__ and function constructor
# * rewrites all array accesses to arrayAccess(array, subscript)

# TODO: disallow eval

# safe pystdlib imports
import os.path
import sys

try:
    from slimit import parser
except ImportError:
    print """slimit is not installed. Please run

    $ sudo easy_install slimit
    """
    sys.exit(1)

try:
    import lxml.html
except ImportError:
    print """lxml is not installed. Please run

    $ sudo easy_install lxml
    """
    sys.exit(1)

# safe ice imports
import jsvisitor
import wrappers

# this is a mapping from permission names to the
# keys in wrappers.wrappers
permsToModulesMap = {}
permsToModulesMap["bookmarks"] = "bookmarks"
permsToModulesMap["cookies"] = "cookies"
permsToModulesMap["history"] = "history"
permsToModulesMap["management"] = "management"
permsToModulesMap["geolocation"] = "geolocation"

# a list of all js files we have processed already
processedFiles = []

def rewriteJs(sourceFiles, perms):
    for js in sourceFiles:
        path = os.path.normpath(os.path.abspath(js)) # get unique path
        # don't process this file if we've seen it already
        if path in processedFiles:
            print "Already processed %s. Skipping." % (path)
            continue 

        # read in js source
        with open(js, "r") as f:
            source = f.readlines()
            print path
            filteredSource = filter_js("\n".join(source))
        
        # rewrite js file in place
        with open(js, "w") as f:
            # add iced coffee
            f.write(wrappers.iced_coffee)
            # write wrapped chrome.* APIs
            for perm, value in perms.iteritems():
                wrappedState = "passthrough" if value else "wrapped"
                f.write(wrappers.wrappers[permsToModulesMap[perm]][wrappedState])
            # write untouched passthrough wrappers
            for untouched in wrappers.untouched:
                f.write(wrappers.wrappers[untouched]["wrapped"])
            f.write("\n")
            f.write(filteredSource)
        processedFiles.append(path)

def rewriteHtml(sourceFiles, perms):
    for html in sourceFiles:
        path = os.path.abspath(html) # get unique path
        # don't process this file if we've seen it already
        if path in processedFiles:
            print "Already processed %s. Skipping." % (path)
            continue

        with open(html, "r") as f:
            source = f.readlines()
            source = "\n".join(source)

        doc = lxml.html.fromstring(source)
        for el in doc.iter():
            if el.tag == 'script':
                if el.text is not None:
                    txt = ""
                    # add iced coffee
                    txt += wrappers.iced_coffee
                    # write wrapped chrome.* APIs
                    for perm, value in perms.iteritems():
                        wrappedState = "passthrough" if value else "wrapped"
                        txt += wrappers.wrappers[permsToModulesMap[perm]][wrappedState]
                    # write untouched passthrough wrappers
                    for untouched in wrappers.untouched:
                        txt += wrappers.wrappers[untouched]["wrapped"]
            
                    el.text = txt + filter_js(el.text)
                for a in el.attrib:
                    if a == "src":
                        # refuse to rewrite extensions with remote script inclusion
                        if "http://" in el.attrib[a] or "https://" in el.attrib[a]:
                            print "This extension tries to load a script from the internet " + \
                                  "and cannot be trusted. We refuse to rewrite it."
                            sys.exit(-1)
                        # no need to rewrite local js files encountered here because
                        # we already walk the extension dir to find all js files

        filteredSource = lxml.html.tostring(doc, method="html")

        with open(html, "w") as f:
            f.write(filteredSource)

def filter_js(s):
    jsParser = parser.Parser()
    tree = jsParser.parse(s)
    visitor = jsvisitor.IceVisitor()
    return visitor.visit(tree)

