ICE (Interposing on Chrome Extensions)
======================================

This project is for wrapping chrome extensions and limiing their permissions.

The problem with chrome permissions is that they are too damn high. Installing
an extension is an all or nothing affair. Users either accept an extension, or
they don't install it.

ICE works by rewriting extension javascript to point `chrome.*` APIs to wrapper
functions. During the extension rewriting process, users are prompted to approve
individual permissions. If the user chooses, they can "revoke" a permission. The
Spoofer extension will supply fake data for any revoked APIs.

Dependencies
============

The ICE rewriter is written in python and requires the `slimit` and `lxml`
packages. To install these:

* `sudo easy_install slimit`
* `sudo easy_install lxml`

ICE uses [crxmake](https://github.com/Constellation/crxmake) to package the
newly rewritten extension. To install:

* `gem install crxmake`

