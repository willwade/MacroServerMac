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

    python MacroServerMac.py

It will now listen for any calls in on the MindExpress port. Please make sure the sending machine has the correct settings in the firewall configuration. For help running the command run..

    python MacroServerMac.py --help

NB: at present it won't allow multiple IP address' despite it saying so!

If you don't have/don't know what MindExpress is and just want to test what MindExpress sends try:

    python TestClient.py


Problems/To-Do
------------------

* Some of the key-mapping is wrong. Please fix the KeyCodes.csv for the correct mapping
* Multi-platform code (will need combining with [PyUserInput](https://github.com/SavinaRoja/PyUserInput) when that project is working nicely with keyboards)
* Allow from IP/Range (You can specify the ip address in the line command - I just havent written the code to allow multiple address')
* Window control code
* Turn it into a nice user friendly binary 

Fun(?!) asides
------------------

If you are looking to convert Windows Keyboard/Mouse commands look at AppleUIEvents.py. There are probably better ways in the long run, for example this code should really make use of [PyUserInput](https://github.com/SavinaRoja/PyUserInput)

What are all the files? (/How does this work?)
--------------
When MacroServerMac.py is run a number of things happen:

* A socket server listening to 12000 is run (METCPServer)
* METCPServer sets up a class called MEUIState which initiates key states for the modifiers (all set to false) and the left drag 
* METCPServer is redefined TCPSserver to hold this Object and the debug variable
* A key is pressed in MindExpress. This opens up a TCP connection on 12000 to a machine and then squirts a small chunk of xml-ish data. 
* METCPServer calls METCPHandler which in turn calls MExpressHandler (in MExpressHandler.py). 
* MExpressHandler really deals with most of the logic from MindExpress. If you want to work out what is sent by MindExpress read this file. It imports AppleUIEvents which in turn opens up QuartzCoreGraphics (and takes an age on my machine). NB: Up to this point the code is pretty multi-platform. 
* MExpressHandler works out what kind of command is being sent and then calls on AppleUIEvents if it needs to do any key mapping
* MExpressHandler loads in the MEUIState (meowi) object when called to look/set the sticky key state of the keys
* MExpressHandler sets keys using applescript and mouse commands using Quartz. 

Many thanks to
--------------

* [Mark Rowland](http://www.youtube.com/watch?v=_Ox94YrYtGo) who is the reason this thing is written. 
* Ian from [Techcess](http://techcess.co.uk)
* [Jabbla](http://www.jabbla.com)

