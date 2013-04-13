(MindExpress) MacroServer/Client for Mac
===========

A server, and set of modules for listening to a [MindExpress](http://www.jabbla.com/products.asp?itemID=9) client and controlling a mac.


How to get started
------------------

##Server##

Run the server in the terminal (on the Mac):

    python MacroServerMac.py

It will now listen for any calls in on the MindExpress port. Please make sure the sending machine has the correct settings in the firewall configuration. For help running the command run..

    python MacroServer/MacroServerMac.py --help

NB: at present it won't allow multiple IP address' despite it saying so!

##Client##

[Find here an example MindExpress-For-Mac jmm file](Layouts/README.md) that I do know works(!). 


If you don't have/don't know what MindExpress is and just want to test what MindExpress sends you can use the Client. You can also use this for applications other than MindExpress by sending the string to call the executable in a shell e.g.:

    python MacroClient/Client.py -cmd mouse -scmd 'subcommandid:change_location|value:100|direction:0|click:0'
    
to move the mouse. or to send a keystroke, something like:
    
    python MacroClient/Client.py --host 192.168.1.121 -cmd send_key -scmd "normalkey:k|modifier:0"
    
NB: With this you don't need MindExpress. It will control your mac over the air through the commandline! 

If you don't have Python and want to experiment with this you can download a binary for Windows and Mac.

* [Windows Binary - That runs in a command prompt interface](https://s3-eu-west-1.amazonaws.com/app-macro/Client.exe.zip)
* [Windows Binary - That can be called by other programs and doesn't open a Window](https://s3-eu-west-1.amazonaws.com/app-macro/ClientW.exe.zip) (NB: any errors that occur you won't be notified using this approach)
* [Mac Binary (64Bit)](https://s3-eu-west-1.amazonaws.com/app-macro/ClientMacOSX64.zip)

For correct syntax see:

    python MacroClient/Client.py --help

or 

    Client.exe --help
    
In your windows command prompt

Problems/To-Do
------------------

* Some of the key-mapping is wrong. Please fix the KeyCodes.csv for the correct mapping
* Implement some better exception code - you will need to keep an eye on the terminal for any exceptions caused as well as the log file
* Speed it up. My guess is the slowness is in the 3/4 regex's that are done when extracting the data from the pseudo-xml. It could be done in one.
* Multi-platform code (will need combining with [PyUserInput](https://github.com/SavinaRoja/PyUserInput) when that project is working nicely with keyboards)
* Allow from IP/Range (You can specify the ip address in the line command - I just havent written the code to allow multiple address')
* Window control code (It can launch applications. Just not control the window placement. Reason for this is it's not a very Mac thing to do/care about.. I'm not sure this will see the light of day..)
* Turn it into a nice user friendly binary 
* Develop some nice Keyboards
* Somehow send a start moving and stop moving mouse command

Fun(?!) asides
------------------

If you are looking to convert Windows Keyboard/Mouse commands look at AppleUIEvents.py. There are probably better ways in the long run, for example this code should really make use of [PyUserInput](https://github.com/SavinaRoja/PyUserInput)

Why??!
------------------

Well because if you want to control a computer, send text to another computer, its not the easiest if you use an alternative input method for a PC. TeamViewer (and others) are OK but they don't convert the Mac Keycodes reliably.


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

Many thanks to
--------------

* [Mark Rowland](http://www.youtube.com/watch?v=_Ox94YrYtGo) who is the reason this thing is written. 
* Ian from [Techcess](http://techcess.co.uk)
* [Jabbla](http://www.jabbla.com)

