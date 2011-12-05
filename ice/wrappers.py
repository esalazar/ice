# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import collections

# helper module. Provides a method for communicating with the spoofer
# extension.
iced_coffee = """
iced_coffee = {
    id : "icedcoffee",
    passMessage : function(params, callback) {
        chrome.extension.sendRequest(iced_coffee.id, params, callback);
    },
}
"""

# chrome api wrappers are stored in a doubly nested hash with
# keys: api name, and a string that is either "wrapped" or
# "passthrough"
wrappers = collections.defaultdict({})

wrappers["history"]["wrapped"] = """
wrapped_chrome.history = {
    addUrl : function(details) {
        # ignored
    },
    deleteAll : function(callback) {
        callback();
    },
    deleteRange : function(range, callback) {
        callback();
    },
    deleteURL : function(details) {
        # ignored
    },
    getVisits : function(details, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.history.getVisits', 'input' : [details] }, callback);
    },
    search : function(query, callback) {
        iced_coffee.passMessage({ 'type' : 'chrome.history.search', 'input' : [query] }, callback);
    },
    onVisitRemoved : {
        addListener : function(callback) {
            # do nothing
        }
    },
    onVisited : {
        addListener : function(callback) {
            # do nothing
        }
    }
}
"""

wrapped["history"]["passthrough"] = """
wrapped_chrome.history = {
    addUrl : function(details) {
        chrome.history.addUrl(details);
    },
    deleteAll : function(callback) {
        chrome.history.deleteAll(callback);
    },
    deleteRange : function(range, callback) {
        chrome.history.deleteRange(range, callback);
    },
    deleteURL : function(details) {
        chrome.history.deleteURL(details);
    },
    getVisits : function(details, callback) {
        chrome.history.getVisits(details, callback);
    },
    search : function(query, callback) {
        chrome.history.search(query, callback);
    },
    onVisitRemoved : {
        addListener : function(callback) {
            chrome.history.onVisitRemoved.addListener(callback);
        }
    },
    onVisited : {
        addListener : function(callback) {
            chrome.history.onVisited.addListener(callback);
        }
    }
}
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
            # do nothing
        }
    },
    onChildrenReordered : {
        addListener : function(callback) {
            # do nothing
        }
    },
    onCreated : {
        addListener : function(callback) {
            # do nothing
        }
    },
    onImportBegin : {
        addListener : function(callback) {
            # do nothing
        }
    },
    onMoved : {
        addListener : function(callback) {
            # do nothing
        }
    },
    onRemoved : {
        addListener : function(callback) {
            # do nothing
        }
    },

}
"""

wrappers["bookmarks"]["passthrough"] = """
wrapped_chrome.bookmarks = {
    create : function(bookmark, callback) {
        chrome.bookmarks.create(bookmark, callback);
    },
    get : function(idOrIdList, callback) {
        chrome.bookmarks.get(idOrIdList, callback);
    },
    getChildren : function(id, callback) {
        chrome.bookmarks.getChildren(id, callback);
    },
    getRecent : function(numberOfItems, callback) {
        chrome.bookmarks.getRecent(numberOfItems, callback);
    },
    getSubTree : function(id, callback) {
        chrome.bookmarks.getSubTree(id, callback);
    },
    getTree : function(callback) {
        chrome.bookmarks.getTree(callback);
    },
    move : function(id, destination, callback) {
        chrome.bookmarks.move(id, destination, callback);
    },
    remove : function(id, callback) {
        chrome.bookmarks.remove(id, callback);
    },
    removeTree : function(id, callback) {
        chrome.bookmarks.removeTree(id, callback);
    },
    search : function(query, callback) {
        chrome.bookmarks.search(query, callback);
    },
    update : function(id, changes, callback) {
        chrome.bookmarks.update(id, changes, callback);
    },
    onChanged : {
        addListener : function(callback) {
            chrome.bookmarks.onChanged.addListener(callback);
        }
    },
    onChildrenReordered : {
        addListener : function(callback) {
            chrome.bookmarks.onChildrenReordered.addListener(callback);
        }
    },
    onCreated : {
        addListener : function(callback) {
            chrome.bookmarks.onCreated.addListener(callback);
        }
    },
    onImportBegin : {
        addListener : function(callback) {
            chrome.bookmarks.onImportBegin.addListener(callback);
        }
    },
    onMoved : {
        addListener : function(callback) {
            chrome.bookmarks.onMoved.addListener(callback);
        }
    },
    onRemoved : {
        addListener : function(callback) {
            chrome.bookmarks.onRemoved.addListener(callback);
        }
    },

}
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
            # do nothing
        }
    },
}
"""

wrappers["cookies"]["passthrough"] = """
wrapped_chrome.cookies = {
    get : function(details, callback) {
        chrome.cookies.get(details, callback);
    },
    getAll : function(details, callback) {
        chrome.cookies.getAll(details, callback);
    },
    getAllCookieStores : function(callback) {
        chrome.cookies.getAllCookieStores(callback);
    },
    remove : function(details, callback) {
        chrome.cookies.remove(details, callback);
    },
    set : function(details, callback) {
        chrome.cookies.set(details, callback);
    },
    onChanged : {
        addListener : function(callback) {
            chrome.cookies.onChanged.addListener(callback);
        }
    },
}
"""

