# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import collections

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
        function randomString(string_length) {
	    var chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
	    var randomstring = '';
	    for (var i=0; i<string_length; i++) {
	    	var rnum = Math.floor(Math.random() * chars.length);
	    	randomstring += chars.substring(rnum,rnum+1);
	    }
            return randomstring;
        }
        var transitions = ["link", "typed", "auto_bookmark", "auto_subframe",
                           "manual_subframe", "generated", "start_page", "form_submit",
                           "reload", "keyword", "keyword_generated"];
        var url = details.url;
        var result = {
            id : randomString(15),
            visitId : randomString(15),
            referringVisitId : randomString(15),
            transition : transitions[Math.floor(Math.random()*transitions.length)]
        }
        callback([result]);

        # or should we do callback([]) ?
    },
    search : function(query, callback) {
        callback([]);
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

