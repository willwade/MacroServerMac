(MindExpress) MacroServer for Mac
===========

This is a server, and set of modules for listening to a [MindExpress](http://www.jabbla.com/products.asp?itemID=9) client and controlling a mac. MindExpress is a Windows based application that is largely used to support individuals who require a communication (Text to speech) software package on their system with other features such as symbol support and alternative access. 

This, and other similar software is great as it allows sentences to be constructed into a message window - or piped out to another program on their computer. But what if they wanted that text to appear on another computer? Or even - control the mouse or applications on that other computer? Well MindExpress has a solution called "MacroServer". The idea is that a small little application runs on the computer you are sending the text to and it listens for commands from the MindExpress running PC. This is known as a MacroServer and Jabbla have only made a Windows based version of - this is the home of the Mac based one. 

There are a number of parts to this project. More detailed information can be found on the relevant pages below - or just read the "get started" section on just running this thing.

- [MacroServer (Mac)](MacroServer/#readme) - The server code. This is the majority of the project and probably why you are here. A quick guide on getting you up and running is below or click on the link for more detailed information. 
- [MacroClient](MacroClient/#readme) - Although you can use MindExpress as a 'client' this client code has been written to emulate MindExpress - useful for testing purposes or using within a different programme.
- [Layouts](Layouts/#readme) - Home of 1 (at the moment) keyboard layout for MindExpress that has been designed to specifically work with this Mac Server software.


Install with virtualenv
-----------------------

Using python packages with virtualenv is the best approach available with least friction. You may need to install virtualenv.  

```
# if virtualenv is not installed
# pip install virtualenv
cd path/to/MacroServerMac
virtualenv -p /usr/bin/python ./venv
. ./venv/bin/activate
pip install -r requirements.txt
```


How to get started
------------------

This is fairly straightforward - in short you make sure there is a piece of software on the Mac ready to listen to MindExpress on a PC. And on the PC you edit a grid to send output to "Windows Control". I'll try and take you through the steps in a bit more detail..

## On your Mac (the "Server")
If you are running this for the first time and running the latest Mac operating system you may run into problems with the security settings. If so you will need to turn-off Gatekeeper. If you aren't you can continue reading from "IP details". 

### Gatekeeper
So first off turn off Gatekeeper. Go to System Preferences and then open "Security & Privacy". Under the General pane you want to set "Allow apps downloaded from:" to be "Anywhere". (hint: if you aren't used to using a mac and are wondering why you can't change this - hit the lock button at the bottom left of the screen). 

<!--
#####Accessibility
Next you have to enable Mac OS X's accessibility frameworks in System Preferences.
Click on the "Accessibility" pane (formerly "Universal Access") in "System Preferences". At the bottom left of the pane is a checkbox setting called "Enable access for assistive devices". Click on the checkbox so the setting is enabled. Close out of System Preferences.
-->

### IP details
[Grab your IP address](http://osxdaily.com/2010/11/21/find-ip-address-mac/) - you will need this for the PC (hint: it is probably worth "fixing" your ip address in the long run if you want to use this frequently). 

### Run the app
Download [this zip file](http://macroservermac.s3.amazonaws.com/MacroServerMac.zip) containing the application. Double click it to run it. Thats it. Note there is very little in the way of an interface. The most useful thing about this front-end app is the ability to quit it if something goes wrong. NB: Don't run the app twice! 


## On your PC (the "Client") 
Next, go to your PC with MindExpress (make sure its a recent version) and open [this jmm file](http://macroservermac.s3.amazonaws.com/keyboard_mac.jmm).  

For the first time you run this you will need to tell MindExpress where to send the keystrokes too. This means editing the page - and in particular the "On" button at the bottom left. Press F2 (Edit mode). Double click on the bottom left "On" button. In the bottom left panel, select the second item down titled "Windows Control: Start Sending"  and write in your mac's IP address. ([Take a look at a screenshot of this which may help](http://i.imgur.com/q4HMJ5J.png)).  Press OK. Exit out of Edit mode (Press F2 again) and you should now be set! 

Hit the "On" button and you will see it move to non-greyed out set of buttons. Clicking on them will send text to the mac. Note the Mouse icon in the top right which also allows you to control the Mouse. 

## Running it as a service on a mac 
If you have carried out the above and its gone well you possibly want to make the application run all the time on the mac. This is simple enough - [follow the instructions here](http://support.apple.com/kb/HT2602). I do recommend using this [silent MacroServer version for this purpose which you can download here](http://macroservermac.s3.amazonaws.com/MacroServerMacService.zip). 

(Note that all log files for this version are stored in ~/Library/Logs/MacroServerMac.log The Library directory is hidden by default on Lion upwards. [Follow these steps](http://osxdaily.com/2011/07/22/access-user-library-folder-in-os-x-lion/) to open the directory required. Just double clicking on the .log file should open it in the console log viewer.)

## What if you are having problems?
Download [this](http://macroservermac.s3.amazonaws.com/MacroServerMacDebug.zip) - run it and send [me](http://willwa.de/) the output. Number one problem is that the application is running already - or you've tried to quit it and it won't die properly. In which case you will need to [kill all](http://osxdaily.com/2010/08/15/mac-task-manager/) running copies of the macroserver application. 


Why??!
------------------

Some people have asked why bother when there are other approaches (e.g. TeamViewer). Well the main one is that teamviewer requires a full window open on the client, does not make use of internal only IP's and is a pain as it doesn't send the correct Mac keystrokes from a PC. In the future this should be really software free - i.e. Bluetooth HID. If you would like to make something then please step forward.. 


Many thanks to
--------------

* [Mark Rowland](http://www.youtube.com/watch?v=_Ox94YrYtGo) who is the reason this thing is written. 
* Ian from [Techcess](http://techcess.co.uk)
* [Jabbla](http://www.jabbla.com)
* Gerard and the team at [RHN Putney](http://www.rhn.org.uk) for trying this all out for real

