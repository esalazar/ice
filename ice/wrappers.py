# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import collections

# helper module. Provides a method for communicating with the spoofer
# extension.
iced_coffee = """
iced_coffee = {
    id : "pffbmilkmcdkfijnablbnmlckadbggca",
    passMessage : function(params, callback) {
        chrome.extension.sendRequest(iced_coffee.id, params, callback);
    },
}
wrapped_chrome = {}
"""

# chrome api wrappers are stored in a doubly nested hash with
# keys: api name, and a string that is either "wrapped" or
# "passthrough"
wrappers = collections.defaultdict(dict)

wrappers["history"]["wrapped"] = """
wrapped_chrome.history = {
    addUrl : function(details) {
        // ignored
    },
    deleteAll : function(callback) {
        callback();
    },
    deleteRange : function(range, callback) {
        callback();
    },
    deleteURL : function(details) {
        // ignored
    },
    getVisits : function(details, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.history.getVisits', 'input' : [details] }, callback);
    },
    search : function(query, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.history.search', 'input' : [query] }, callback);
    },
    onVisitRemoved : {
        addListener : function(callback) {
            // do nothing
        }
    },
    onVisited : {
        addListener : function(callback) {
            // do nothing
        }
    }
}
"""

wrappers["history"]["passthrough"] = """
wrapped_chrome.history = chrome.history
"""

wrappers["bookmarks"]["wrapped"] = """
wrapped_chrome.bookmarks = {
    create : function(bookmark, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.bookmarks.create', 'input' : [bookmark] }, callback);        
    },
    get : function(idOrIdList, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.bookmarks.get', 'input' : [idOrIdList] }, callback);
    },
    getChildren : function(id, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.bookmarks.getChildren', 'input' : [id] }, callback);
    },
    getRecent : function(numberOfItems, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.bookmarks.getRecent', 'input' : [numberOfItems] }, callback);
    },
    getSubTree : function(id, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.bookmarks.getSubTree', 'input' : [id] }, callback);
    },
    getTree : function(callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.bookmarks.getTree', 'input' : [] }, callback);
    },
    move : function(id, destination, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.bookmarks.move', 'input' : [id, destination] }, callback);
    },
    remove : function(id, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.bookmarks.remove', 'input' : [id] }, callback);
    },
    removeTree : function(id, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.bookmarks.removeTree', 'input' : [id] }, callback);
    },
    search : function(query, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.bookmarks.query', 'input' : [query] }, callback);
    },
    update : function(id, changes, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.bookmarks.update', 'input' : [id, changes] }, callback);
    },
    onChanged : {
        addListener : function(callback) {
            // do nothing
        }
    },
    onChildrenReordered : {
        addListener : function(callback) {
            // do nothing
        }
    },
    onCreated : {
        addListener : function(callback) {
            // do nothing
        }
    },
    onImportBegin : {
        addListener : function(callback) {
            // do nothing
        }
    },
    onMoved : {
        addListener : function(callback) {
            // do nothing
        }
    },
    onRemoved : {
        addListener : function(callback) {
            // do nothing
        }
    },

}
"""

wrappers["bookmarks"]["passthrough"] = """
wrapped_chrome.bookmarks = chrome.bookmarks
"""

wrappers["cookies"]["wrapped"] = """
wrapped_chrome.cookies = {
    get : function(details, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.cookies.get', 'input' : [details] }, callback);
    },
    getAll : function(details, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.cookies.getAll', 'input' : [details] }, callback);
    },
    getAllCookieStores : function(callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.cookies.getAllCookieStores', 'input' : [] }, callback);
    },
    remove : function(details, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.cookies.remove', 'input' : [details] }, callback);
    },
    set : function(details, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.cookies.set', 'input' : [details] }, callback);
    },
    onChanged : {
        addListener : function(callback) {
            // do nothing
        }
    },
}
"""

wrappers["cookies"]["passthrough"] = """
wrapped_chrome.cookies = chrome.cookies
"""

wrappers["management"]["wrapped"] = """
wrapped_chrome.management = {
    get : function(id, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.management.get', 'input' : [id] }, callback);
    },
    getAll : function(callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.management.getAll', 'input' : [] }, callback);
    },
    getPermissionWarningsById : function(id, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.management.getPermissionWarningsById', 'input' : [id] }, callback);
    },
    getPermissionWarningsByManifest : function(id, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.management.getPermissionWarningsByManifest', 'input' : [id] }, callback);
    },
    launchApp : function(id, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.management.launchApp', 'input' : [id] }, callback);
    },
    setEnabled : function(id, enabled, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.management.setEnabled', 'input' : [id, enabled] }, callback);
    },
    uninstall : function(id, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.management.uninstall', 'input' : [id] }, callback);
    },
    onDisabled : {
        addListener : function(callback) {
            // do nothing
        }
    },
    onEnabled : {
        addListener : function(callback) {
            // do nothing
        }
    },
    onInstalled : {
        addListener : function(callback) {
            // do nothing
        }
    },
    onUninstalled : {
        addListener : function(callback) {
            // do nothing
        }
    },
}
"""

wrappers["management"]["passthrough"] = """
wrapped_chrome.management = chrome.management
"""

untouched = ["browserAction", "contextMenus", "extension", "fileBrowserHandler", "i18n",
        "idle", "omnibox", "pageAction", "proxy", "tabs", "tts", "ttsEngine",
        "types", "windows"]

# passthrough for untouched libs
for lib in untouched:
    wrappers[lib]["wrapped"] = wrappers[lib]["passthrough"] = "wrapped_chrome.%s = chrome.%s\n" %(lib, lib)

wrappers["none"]["wrapped"] = wrappers["none"]["passthrough"] = "// do nothing\n"

