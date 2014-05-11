####Server####

There are some binaries available to download:

- [MacroServer - Standard](http://macroservermac.s3.amazonaws.com/MacroServerMac.zip). Use this one for first testing it all works.
- [MacroServer - Debug](http://macroservermac.s3.amazonaws.com/MacroServerMacDebug.zip). If you want to know whats not working try this. 
- [MacroServer - No Output & backgrounded](http://macroservermac.s3.amazonaws.com/MacroServerMacService.zip) (for running as a service)

Run the server in the terminal (on the Mac):

    python MacroServerMac.py

It will now listen for any calls in on the MindExpress port. Please make sure the sending machine has the correct settings in the firewall configuration. For help running the command run..

    python MacroServer/MacroServerMac.py --help

NB: at present it won't allow multiple IP address' despite it saying so!

#####Dependencies#####

If you want fancy notifications of which modifier key has been set by MindExpress install the Growl Notfication plug-in. Don't fret its easy - and the results are neat. [See the information here for installation](https://github.com/kfdm/gntp#installation). Once installed you will probably want to run it like this:

    python MacroServerMac.py --loglevel DEBUG --usegrowl True
    
NB: This isn't in the standard install due to the need to compile in the Growl application. I wish it was a bit easier because growl is far nicer than the standard notification view. 

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

For information on the API from MindExpress [read the README-API.md documentation](README-API.md)

Compiling it
------------------
The line command has been compiled with [Platypus](http://sveinbjorn.org/platypus). Simply put all of the code from the MacroServer (this) directory in the Platypus build - PLUS - [docopt.py (0.6.1)](https://github.com/docopt/docopt/blob/0.6.1/docopt.py) and  [pyNotificationCenter.py](https://github.com/maranas/pyNotificationCenter/blob/master/pyNotificationCenter.py). Alter your line command settings appropriately. This is the commands for the different releases:

###MacroSeverMac - Standalone###

    --loglevel=error --logtype=stdout --notifier=Notifier

(Also set the Output to "Text Window") 

###MacroSeverMac - Debug###

    --loglevel=info --logtype=stdout --notifier=Notifier

(Also set the Output to "Text Window") 

###MacroSeverMac - Service###

    --loglevel=warn --logtype=file --notifier=Notifier --logfile=~/Library/Logs/MacroServerMac.log
    
(Also set the "Run in background" flag and Output to "None")

Fun(?!) asides
------------------

If you are looking to convert Windows Keyboard/Mouse commands look at AppleUIEvents.py. There are probably better ways in the long run, for example this code should really make use of [PyUserInput](https://github.com/SavinaRoja/PyUserInput)


Problems/To-Do
------------------

* Some of the key-mapping is a bit wrong. I'm relying on users telling me whats not correct
* Implement some better exception code - you will need to keep an eye on the terminal for any exceptions caused as well as the log file
* Speed it up. My guess is the slowness is in the 3/4 regex's that are done when extracting the data from the pseudo-xml. It could be done in one. Also the csv file is re-read on each key. That could be put in memory since its small enough. 
* Multi-platform code (will need combining with [PyUserInput](https://github.com/SavinaRoja/PyUserInput) when that project is working nicely with keyboards). Should be straightforward enough - particularly Windows (only reason I can think of doing this is making use of Growl notifier on Windows)
* Allow from IP/Range (You can specify the ip address in the line command - I just havent written the code to allow multiple address')
* Window control code (It can launch applications. Just not control the window placement. Reason for this is it's not a very Mac thing to do/care about.. I'm not sure this will see the light of day..)
* Somehow send a start moving and stop moving mouse command

