(MindExpress) MacroServer for Mac
===========

A server, and set of modules for listening to a [MindExpress](http://www.jabbla.com/products.asp?itemID=9) client and controlling a mac.


Dependencies
------------

Depending on your platform, you will need the following python modules for this to function:

  * Mac - Quartz

How to get started
------------------

Run the server in the terminal:

    ./MacroServerMac.py

It will now listen for any calls in on the MindExpress port. Please make sure the sending machine has the correct settings in the firewall configuration. 

Problems/To-Do
------------------

* Some of the key-mapping is wrong. Please fix the KeyCodes.csv for the correct mapping
* Multi-platform code (will need combining with [PyUserInput](https://github.com/SavinaRoja/PyUserInput) when that project is working nicely with keyboards)
* Allow from IP/Range
* Sticky_key functionality (having a mind block here)
* Window control code
* Turn it into a nice user friendly binary 

Many thanks to
--------------

* [Mark Rowland](http://www.youtube.com/watch?v=_Ox94YrYtGo) who is the reason this thing is written. 
* Ian from [Techcess](http://techcess.co.uk)
* [Jabbla](http://www.jabbla.com)

