# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# this module is responsible for rewriting chrome javascript source files.
# Modifcations it makes are:
# * All chrome identifiers are replaced with wrapped_chrome
# * geolocation identifiers are replaced with wrapped_geolocation
# * disallow access to __proto__ and function constructor
# * rewrites all array accesses to arrayAccess(array, subscript)

# TODO: disallow eval

# safe pystdlib imports
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

permsToModulesMap = {}
permsToModulesMap["bookmarks"] = "bookmarks"
permsToModulesMap["cookies"] = "cookies"
permsToModulesMap["history"] = "history"
permsToModulesMap["management"] = "management"
permsToModulesMap["geolocation"] = "geolocation"


processedFiles = []

def rewriteJs(sourceFiles, perms):
    for js in sourceFiles:
        name = js.rsplit("/", 1)[1] # get filename
        # don't process this file if we've seen it already
        if name in processedFiles:
            continue

        # refuse to rewrite extensions with remote script inclusion
        if "http://" in js or "https://" in js:
            print "This extension tries to load a script from the internet " + \
                  "and cannot be trusted. We refuse to rewrite it."
            sys.exit(-1)

        # read in js source
        with open(js, "r") as f:
            source = f.readlines()
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
            # write trusted lib
            f.write(trustedLib)
            f.write("\n")
            f.write(filteredSource)
        processedFiles.append(name)

def rewriteHtml(sourceFiles, perms):
    for html in sourceFiles:
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
                    txt += trustedLib + "\n"
            
                    el.text = txt + filter_js(el.text)
                for a in el.attrib:
                    if a == "src":
                        rewriteJs([html.rsplit("/", 1)[0] + "/" + el.attrib[a]], perms)
        filteredSource = lxml.html.tostring(doc, method="html")

        with open(html, "w") as f:
            f.write(filteredSource)

def filter_js(s):
    jsParser = parser.Parser()
    tree = jsParser.parse(s)
    visitor = jsvisitor.IceVisitor()
    return visitor.visit(tree)

# this is a trusted javascript lib that contains methods used by
# the rewriter to ensure safe runtime execution
trustedLib = """
// This function could be used in the future to check strings of
// array accesses.
// For now, it does nothing
function arrayAccess(array, subscript) {
    return array[bracket_check(subscript)];
}

// Prevents dangerous properties from being accessed
function bracket_check(input) {
    if (typeof(input) === "number") {
        return input;
    }

    var dangerous = ["__proto__", "prototype", "constructor", "__defineGetter__", "__defineSetter__"];
    var copied_input = "";
    var len = input.length;
    for (var j = 0; j < len; j++) {
        copied_input += input.charAt(j);
    }
    for (var i = 0; i < dangerous.length; i++) {
        if (dangerous[i] == copied_input) {
            throw Error("Illegal array subscript");
        }
    }
    return copied_input;
}
"""

