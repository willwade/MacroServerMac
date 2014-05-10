(MindExpress) MacroServer for Mac
===========

A server, and set of modules for listening to a [MindExpress](http://www.jabbla.com/products.asp?itemID=9) client and controlling a mac.

For the server, there are three binaries created of the server for the Mac and a demonstration keyboard for MindExpress. 
- [Standard MacroServerMac](http://macroservermac.s3.amazonaws.com/MacroServerMac.zip) which outputs some nice messages to a screen when it recieves data from MindExpress
- [A debugging MacroServerMac](http://macroservermac.s3.amazonaws.com/MacroServerMacDebug.zip) - the same as the Standard version but a lot more data is outputted. 
- [Service MacroServerMac](http://macroservermac.s3.amazonaws.com/MacroServerMacService.zip). Useful for running as a background task on login. 
- [Mac Keyboard.jmm](http://macroservermac.s3.amazonaws.com/keyboard_mac.jmm). Open this in MindExpress. Note that for this to look nice you will need to install ["VAG Rounded Light"](http://www.fonts101.com/fonts/view/Uncategorized/39723/VAGRoundedLightSSi) on the PC (just download and double click!).

If you are at all unsure how to use this please read on!

How to get started (/How to use the binaries)
------------------

It may be worth spending a couple of lines explaining how this works. First you need MindExpress running on the PC. MindExpress has a feature which sends text to another computer - instead of its own message bar. For it to do that a small piece of software must run on the other computer (the "Server"). So to set this up you need to make sure both MindExpress is setup correctly and the Server - in this case a Mac. We will now try to cover both sides of this. 

####On your Mac (the "Server")####
If you are running this for the first time and running the latest Mac operating system you may run into problems with the security settings. If so you will need to turn-off Gatekeeper. If you aren't you can continue reading from "IP details". 

#####Gatekeeper
So first off turn off Gatekeeper. Go to System Preferences and then open "Security & Privacy". Under the General pane you want to set "Allow apps downloaded from:" to be "Anywhere". (hint: if you aren't used to using a mac and are wondering why you can't change this - hit the lock button at the bottom left of the screen). 

<!--
#####Accessibility
Next you have to enable Mac OS X's accessibility frameworks in System Preferences.
Click on the "Accessibility" pane (formerly "Universal Access") in "System Preferences". At the bottom left of the pane is a checkbox setting called "Enable access for assistive devices". Click on the checkbox so the setting is enabled. Close out of System Preferences.
-->

#####IP details
[Grab your IP address](http://osxdaily.com/2010/11/21/find-ip-address-mac/) - you will need this for the PC (hint: it is probably worth "fixing" your ip address in the long run if you want to use this frequently). 

#####Run the app
Download [this zip file](http://macroservermac.s3.amazonaws.com/MacroServerMac.zip) containing the application. Double click it to run it. Thats it. Note there is very little in the way of an interface. The most useful thing about this front-end app is the ability to quit it if something goes wrong. NB: Don't run the app twice! 


####On your PC (the "Client")####
Next, go to your PC with MindExpress (make sure its a recent version) and open [this jmm file](http://macroservermac.s3.amazonaws.com/keyboard_mac.jmm).  

For the first time you run this you will need to tell MindExpress where to send the keystrokes too. This means editing the page - and in particular the "On" button at the bottom left. Press F2 (Edit mode). Double click on the bottom left "On" button. In the bottom left panel, select the second item down titled "Windows Control: Start Sending"  and write in your mac's IP address. Press OK. Exit out of Edit mode (Press F2 again) and you should now be set! Hit the "On" button and you will see it move to non-greyed out set of buttons. Clicking on them will send text to the mac. Note the Mouse icon in the top right which also allows you to control the Mouse. 

### Running it as a service on a mac###
If you have carried out the above and its gone well you possibly want to make the application run all the time on the mac. This is simple enough - [follow the instructions here](http://support.apple.com/kb/HT2602). I do recommend using this [silent MacroServer version for this purpose which you can download here](http://macroservermac.s3.amazonaws.com/MacroServerMacService.zip). 

(Note that all log files for this version are stored in ~/Library/Logs/MacroServerMac.log The Library directory is hidden by default on Lion upwards. [Follow these steps](http://osxdaily.com/2011/07/22/access-user-library-folder-in-os-x-lion/) to open the directory required. Just double clicking on the .log file should open it in the console log viewer.)

###What if you are having problems?###
Download [this](http://macroservermac.s3.amazonaws.com/MacroServerMacDebug.zip) - run it and send me the output. Number one problem is that the application is running already - or you've tried to quit it and it won't die properly. In which case you will need to [kill all](http://osxdaily.com/2010/08/15/mac-task-manager/) running copies of the macroserver application. 

###The geekier but more powerful approach###

So read on if you want to know a little more and play with this/debug it all.. NB: For this I assume you know your round a mac a little bit..

####Server####

Run the server in the terminal (on the Mac):

    python MacroServerMac.py

It will now listen for any calls in on the MindExpress port. Please make sure the sending machine has the correct settings in the firewall configuration. For help running the command run..

    python MacroServer/MacroServerMac.py --help

NB: at present it won't allow multiple IP address' despite it saying so!

#####Dependencies#####

If you want fancy notifications of which modifier key has been set by MindExpress install the Growl Notfication plug-in. Don't fret its easy - and the results are neat. [See the information here for installation](https://github.com/kfdm/gntp#installation). Once installed you will probably want to run it like this:

    python MacroServerMac.py --loglevel DEBUG --usegrowl True
    
NB: This isn't in the standard install due to the need to compile in the Growl application. I wish it was a bit easier because growl is far nicer than the standard notification view. 

####Client####

[Find here an example MindExpress-For-Mac jmm file](Layouts/README.md) that I do know works(!). 

If you don't have/don't know what MindExpress is and just want to test what MindExpress sends you can use the Client. You can also use this for applications other than MindExpress by sending the string to call the executable in a shell e.g.:

    python MacroClient/Client.py -cmd mouse -scmd 'subcommandid:change_location|value:100|direction:0|click:0'
    
to move the mouse. or to send a keystroke, something like:
    
    python MacroClient/Client.py --host 192.168.1.121 -cmd send_key -scmd "normalkey:k|modifier:0"
    
NB: With this you don't need MindExpress. It will control your mac over the air through the commandline! 

If you don't have Python and want to experiment with this you can download a binary for Windows and Mac. It works exactly the same. e.g. 

    C:\Client.exe --host 192.168.1.121 -cmd send_key -scmd "normalkey:k|modifier:0"
    
* [Windows Binary - That runs in a command prompt interface](https://s3-eu-west-1.amazonaws.com/app-macro/Client.exe.zip)
* [Windows Binary - That can be called by other programs and doesn't open a Window](https://s3-eu-west-1.amazonaws.com/app-macro/ClientW.exe.zip) (NB: any errors that occur will go silently..)
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
* Speed it up. My guess is the slowness is in the 3/4 regex's that are done when extracting the data from the pseudo-xml. It could be done in one. Also the csv file is re-read on each key. That could be put in memory since its small enough. 
* Multi-platform code (will need combining with [PyUserInput](https://github.com/SavinaRoja/PyUserInput) when that project is working nicely with keyboards). Should be straightforward enough - particularly Windows (only reason I can think of doing this is making use of Growl notifier on Windows)
* Allow from IP/Range (You can specify the ip address in the line command - I just havent written the code to allow multiple address')
* Window control code (It can launch applications. Just not control the window placement. Reason for this is it's not a very Mac thing to do/care about.. I'm not sure this will see the light of day..)
* Turn it into a nice user friendly binary 
* Develop some tabs for the keyboard demo, demonstrating various Mac application shortcuts
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
* Gerard and the team at [RHN Putney](http://www.rhn.org.uk) for trying this all out for real

