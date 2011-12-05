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

Installing
==========

ICE uses setuptools to install itself and create the ice executable.

To install:

* `git clone git://github.com/lopopolo/ice.git`
* `cd ice/ice`
* `python setup.py install`

Dependencies
============

If you choose to go the manual route ...

The ICE rewriter is written in python and requires the `slimit` and `lxml`
packages. To install these:

* `sudo easy_install slimit`
* `sudo easy_install lxml`

ICE uses [crxmake](https://github.com/Constellation/crxmake) to package the
newly rewritten extension. To install:

* `gem install crxmake`

Use
===

`$ ice`

`ice` is an interactive program that can wrap extensions from the chrome web
store or local unpacked extensions.

The id `ice` prompts the user for is the long alphabetic identifier used by
the chrome web store. For local extensions, this string can be anything.

`ice` then asks the user to approve/deny all permissions the extension
requests.

`ice` outputs the wrapped extension as a crx file in the working directory. To
use the new extension, the user must install the spoofer extension, located at
`$REPO_ROOT/extensions/spoofer.crx` and the output crx file.

