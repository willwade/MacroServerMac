Layouts and Grids
=================

Find here some example MindExpress pages.

##Download##

The [keyboard_mac.jmm file](http://macroservermac.s3.amazonaws.com/keyboard_mac.jmm) is the jmm (MindExpress document) that you can use. 

You will also need the font ["VAG Rounded Light"](http://www.fonts101.com/fonts/view/Uncategorized/39723/VAGRoundedLightSSi) for this package to look how it was meant to!

Note that the [keyboard\_mac.xml](keyboard_mac.xml) for this is in this repo if you want to tweak it - or compare changes. 

##Running:##

* Make sure you set your mac's IP address by editing the very first page's "On" button.
* Run the server:
    
        python MacroServerMac.py 
    
    or if you want to debug it:

        python MacroServerMac.py --loglevel DEBUG

    And follow the log file that is created in the same directory as the Server. 

##Notes:##

* You will need to keep track of whether the shift/control/command/alt(opt) key has been selected as there is no way of showing this on the MindExpress keyboard. This is a little easier if you run the server with the Growl notifier set to True e.g.
    
        python MacroServerMac.py --usegrowl True


!['Screenshot of the first keyboard made'](ScreenShotMacMindExpress1.png)

