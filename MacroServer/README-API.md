MindExpress Macro API Details
=============================

NB: This information is with thanks from [Jabbla](http://www.jabbla.com) 

#How is something sent?#

We open a socket at the given I.P. address and create a connection at port 12000. Then we send a list   of bytes, and then we close the socket

#What is sent?#

The list of bytes has a size of 'N'+2 and is defined as followed:

    First byte: 'N' divided by 256, rounded down
    Second byte: 'N' modulo 256
    'N' bytes: the command (written in the system default Windows ANSI code page).

#The remote command#

For example: 

    {e7ca10ca-4f8d-47ed-8902178849c7a1d5}
    <command="send_key"\>
    <specialkey="32"\>
    <modifier="0"\>
    <X_MEUser"@user1-4874-305132@"\>
    <X_MELng"9"\>
    <X_STAVersion="1.1.1.1261"\>

##prefix: plug-in ID##

The First part of a command starts with a '{' and ends with a '}' The number indicates the ID of the add on that send the command {e7ca10ca-4f8d-47ed-8902178849c7a1d5}   the Windows Control add on (currently the only plug-in that uses the remote program)

##postfix: Mind Express Data##

    <X_MEUser"@user1-4874-305132@"\>
    <X_MELng"9"\>
    <X_STAVersion="1.1.1.1261"\>

###X_MEUser###

contains the ID of the user logged into mind express that sends this command

###X_MELng###

contains the language of mind express. 

###X_STAVersion###

the version of the plug-in used to send this message

##the middle: the mind express command##

The mind express command starts with <command="..."\> Dependant on the command the following arguments Might differ

###send_key###


       <NormalKey="[text]"\><Modifier="[mod]"\>


Or

       <SpecialKey="[keyID]"\><Modifier="[mod]"\>

####[text]####

is the text the user gave in the mind express editor (this can be 1 character, or a bunch)

####[keyID]####

the number windows gives to a the key (known as a VK code). Currenlty the codes being send are: VK\_SPACE,VK\_ESCAPE,VK\_INSERT,VK\_HOME,VK\_PRIOR (this is page up),VK\_NEXT (this is page down),VK\_DELETE,VK\_END,VK\_TAB,VK\_RETURN,VK\_BACK (this is backspace),VK\_UP,VK\_LEFT,VK\_DOWN, VK\_RIGHT,VK\_F1,VK\_F2, ...,VK\_F11,VK\_F12,VK\_NUMPAD0,VK\_NUMPAD1, ... ,VK\_NUMPAD8, VK\_NUMPAD9,VK\_DECIMAL,VK\_SNAPSHOT,VK\_CAPITAL (caps lock key),VK\_NUMLOCK, VK\_MENU (the alt key),VK\_SHIFT,VK\_CONTROL,VK\_LWIN (the windows key)

the actual value can be found on-line (for example, [here](http://cherrytree.at/misc/vk.htm))

####[mod]####

is a mask of modifiers used during the command:

       1       shift
       2       ctrl
       3       alt
       4       the windows key


###sticky_key###

       <Modifier="[mod]"\>

####[mod]####

is the ID of the modifier:

       1       shift
       2       ctrl
       3       alt
       4       the windows key

###pause###

       <Value="[val]"\>

   [val] the time in ms to wait


###window_control###

       <SubCommandId="1"><Type="min">

   Minimize the active window

       <SubCommandId="1"><Type="max">

   Maximize the active window

       <SubCommandId="1"><Type="res">

   Restore the active window

       <SubCommandId="[subcomid]"><Value="[val]"><Direction="[direction]"\><GotoCorner="[gtc]"\>

####[val]####

 the amount of pixels to move/resize/...

####[direction]####

 direction (0 = up,  90 = left, 180 = down...)

####[gtc]####

 should be 0 (if 1, instead of moving an amount of pixels, move it to a corner)

####[subcomid]####

 the subcommand ID, a number
 
       0       Change Location
       1       Resize Window
       2       Dock window
       3       Tile window
       4       Select Next Window


###mouse###

       <SubCommandId="0"\><Value="[val]"\><Direction="[direction]"\><Click="0"\>

####[val]####

the amount of pixels to move the mouse

####[direction]####

direction that the mouse is moved (0 = up, 90 = left, 180 = down ...)

        <SubCommandId="[subcomid]"\><Value="[val]"\><Direction="[direction]"\><Click="[click]"\>

####[subcomid]####

the subcommand ID, a number

       5       Single Left Click ( [click] will be 0, [direction] will be 90 )
       8       Double Left Click ( [click] will be 1, [direction] will be 90 )
       9       Single Right Click ( [click] will be 0, [direction] will be 270 )
       10      Toggle Left Dragging ( [click] will be 2, [direction] will be 90 )


###exit###

       <SubCommandId="[subcomid]"\>

####[subcomid]####

 the subcommand ID, a number
 
       6       closes Mind Express (These commands don't need to do anything in the remote client)
       7       power down the computer


###sendletter###

Sends the Letter of Mind Express. These commands don't need to do anything in the remote client.

###sendonoff###

Change if Mind Express sends commands. These commands don't need to do anything in the remote client.

###alwaysontop###

Makes sure that mind express doesn't go to the background if the user presses an other window. These commands don't need to do anything in the remote client.

###me_control###

Alters the Mind Express window. These commands don't need to do anything in the remote client.
