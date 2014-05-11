
The Client Code
------------------

([Find here an example MindExpress-For-Mac jmm file](Layouts/README.md) that I do know works(!))

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