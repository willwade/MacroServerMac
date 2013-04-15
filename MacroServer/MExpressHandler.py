#!/usr/bin/env python
# The main server code for the Mind Express Server
# NB:  could be multi-platform
# Date: April 2013

# Re used to analyse the packet recieved 
import re
# Platform may be excluded - would allow us to map to windows/mac/linux
import os, platform
# to do the waiting
import time
# For debug
import logging
# To map the key codes
import csv
# The Mac Mouse Event
from AppleUIEvents import AppleMouseEvents
# The Mac Keyboard Event
from AppleUIEvents import AppleKeyboardEvents

class MExpressHandler(object):
    
    def __init__(self,request,meowi,notifier):
        self.data = ''
        self.pluginid = ''
        self.mexinfo = ''
        self.isMex = self.parseRequest(request);
        self.enablePause = True
        #self.meowi is the keystate
        self.meowi = meowi
        #growl
        self.notifier = notifier
         
    def parseRequest(self,request):
        # first take the first {} as plug-in id
        # NB: this is a little unpleasant to look at but works so deal with it
        try:
            p = re.compile('{([a-z0-9-]+)}')
            self.pluginid = p.findall(request)[0]
        except:
            # No pluginid found
            logging.debug('No pluginid found')
            return False
        # lets get the command
        p = re.compile('<([\w]+)="([^"]+)"')
        self.data =  dict(p.findall(request))
        p = re.compile('<X_([a-zA-Z]+)"([^"]+)"')
        self.mexinfo = dict(p.findall(request))
        # not essential but for completeness:
        if (self.data.has_key('X_STAVersion')):
            self.mexinfo['X_STAVersion'] = self.data['X_STAVersion']
            self.data.pop('X_STAVersion', None)
        logging.debug('Data all parsed')
        return True
                
    def doCommand(self):
        # the following could allow this library to be multiplatform..
        pform = platform.system()
        # this is like doing a switch
        func_name = 'control_'+str(self.data['command'])
        # if doing multi-platform    
        #func_name = 'control_'+pform+'_'++str(self.data['command'])
        logging.debug('About to call..'+func_name)      
        func = getattr(self,func_name)
        return func()
    
    def replace_all(self, text, dic):
      for i, j in dic.iteritems():
        text = text.replace(i, j)
      return text
       
    def control_send_key(self):
        #add in the modifier key. 
        # this may not be correct if two modifier keys set
        cmdappend = ''
        if((int(self.data['modifier'])>0) or (any(self.meowi.sticky.itervalues()))):
            cmdappend += ' using {'
            for mods in self.meowi.sticky.iterkeys():
                if (self.meowi.sticky[mods]):
                    cmdappend += mods+' down, '
            if (self.data['modifier'] == '1'):
                cmdappend += 'shift down, '
            if (self.data['modifier'] == '2'):
                cmdappend += 'control down, '
            if (self.data['modifier'] == '3'):
                cmdappend += 'option down, '   
            if (self.data['modifier'] == '4'):
                cmdappend += 'command down, '
            cmdappend = cmdappend[:-len(', ')]+'}'
                                  
        # Now do something with the normal/specialkey 
        if (self.data.has_key('normalkey')):
            logging.debug('normal send_key:'+self.data['normalkey'])
            escape = {'\\':'\\\\', '"':'\"',"'":"\'"}
            dataforos = self.replace_all(self.data['normalkey'],escape)
            cmd = "osascript -e 'tell application \"System Events\" to keystroke \""+dataforos+"\""+cmdappend+"'"
            os.system(cmd)
        elif (self.data.has_key('specialkey')):
            logging.debug('special send_key:'+self.data['specialkey'])
            k = AppleKeyboardEvents()
            specialcode = k.convertWintoMacCode(self.data['specialkey'])
            logging.debug('converted to:'+str(specialcode))
            cmd = "osascript -e 'tell application \"System Events\" to key code "+specialcode+cmdappend+"'"
            os.system(cmd)
        
        logging.debug('system call:'+cmd)
        logging.debug('sticky:'+str(self.meowi.sticky))
        
    def control_sticky_key(self):
        if(self.data.has_key('modifier')):
            if (self.data['modifier'] == '1'):
                self.meowi.sticky_toggle('shift')
                self.notifier.sendMessage('shift',self.meowi.sticky['shift'])
                logging.debug('shift set')
            elif (self.data['modifier'] == '2'):
                self.meowi.sticky_toggle('control')
                self.notifier.sendMessage('control',self.meowi.sticky['control'])
                logging.debug('ctrl set')
            elif (self.data['modifier'] == '3'):
                self.meowi.sticky_toggle('option')
                self.notifier.sendMessage('option',self.meowi.sticky['option'])
                logging.debug('option set')
            elif (self.data['modifier'] == '4'):
                self.meowi.sticky_toggle('command')
                self.notifier.sendMessage('command',self.meowi.sticky['command'])
                logging.debug('cmd set')
        return True
        
    def control_pause(self):
        if(self.data.has_key('value')):
            # sleep is in seconds. pause command is in ms
            time.sleep(self.data['value']/1000)
        return True
    
    def control_window_control(self):
        """
        I'm not too keen on all this for OSX but for completeness I think we should use:
        http://www.sirver.net/blog/2012/01/04/move-window-done-right/
        
      <SubCommandId=1><Type=min>
        SubCommandID = 1, Type= Min - Minimise active
        SubCommandID = 1, Type= Max - Maximise active
        SubCommandID = 1, Type= Res - Restore active
       <SubCommandId=[subcomid]><Value=[val]><Direction=[d
irection]><GotoCorner=[gtc]>
       [val] the amount of pixels to move/resize/...
       [direction] direction (0 = up,  90 = left, 180 = down...)
       [gtc] should be 0 (if 1, instead of moving an amount ofpixels, move it to a corner)
       [subcomid] the subcommand ID, a number
               0       Change Location
               1       Resize Window
               2       Dock window
               3       Tile window
               4       Select Next Window
        """
        if (self.data['subcommandid'] == 'select_next_app'):
            cmd = "osascript -e 'tell application \""+self.data['text']+"\" to activate'"
            os.system(cmd)
        return True
    
    def control_mouse(self):
        """
        <SubCommandId=0><Value=val><Direction=directionval><click=0
               [val] the amount of pixels to move the mouse
               [direction] direction that the mouse is moved (0 = up,90 = left, 180 = down ...)
               [subcomid] the subcommand ID, a number
               5       Single Left Click ( [click] will be 0, [direction] will be 90 )
               8       Double Left Click ( [click] will be 1, [direction] will be 90 )
               9       Single Right Click ( [click] will be 0, [direction] will be 270 )
               10      Toggle Left Dragging ( [click] will be 2, [direction] will be 90 )
        """
        m = AppleMouseEvents()
        pos = m.currentPos()
        val = float(self.data['value'])
        logging.debug('Mouse movement')
      
        if (self.data['subcommandid']=='change_location'):
            # get currentPos
            if (self.data['direction']=='0'):
                # Up
                if (self.meowi.leftdrag):
                    logging.debug('leftdrag, up')
                    m.mousedrag(pos.x,pos.y-val)                      
                else:
                    logging.debug('up')
                    m.mousemove(pos.x,pos.y-val)      
            elif (self.data['direction']=='90'):
                # Left
                if (self.meowi.leftdrag):
                    logging.debug('leftdrag, left')
                    m.mousedrag(pos.x-val,pos.y)
                else:   
                    logging.debug('left')
                    m.mousemove(pos.x-val,pos.y)      
            elif (self.data['direction']=='270'):
                # Right
                if (self.meowi.leftdrag):
                    logging.debug('leftdrag, right')
                    m.mousedrag(pos.x+val,pos.y)                 
                else:
                    logging.debug('right')
                    m.mousemove(pos.x+val,pos.y) 
            elif (self.data['direction']=='180'):
                # Down
                if (self.meowi.leftdrag):
                    logging.debug('leftdrag, down')
                    m.mousedrag(pos.x,pos.y+val)      
                else:
                    logging.debug('down')
                    m.mousemove(pos.x,pos.y+val)      
        elif (self.data['subcommandid']=='click'):
            if(self.data['click']=='0' and self.data['direction']=='90'):
                 logging.debug('click')
                 m.mousesingleclick(pos.x,pos.y)
            elif(self.data['click']=='1' and self.data['direction']=='90'):
                 logging.debug('dbl-click')
                 m.mousedblclick(pos.x,pos.y)
            elif(self.data['click']=='0' and self.data['direction']=='270'):
                 logging.debug('r-click')
                 m.mouserclick(pos.x,pos.y)
            elif(self.data['click']=='2' and self.data['direction']=='90'):
                # not sure how this works
                 logging.debug('drag lock on')
                 self.meowi.leftdrag = True 
        return True
    
    
    def control_exit(self):
        """
        <SubCommandId=[subcomid]>
           [subcomid] the subcommand ID, a number
                   6       closes Mind Express (These commands don't need to do anything in the remote client)
                   7       power down the computer

        """
        # only val 7 should do something - shut down the computer
        return True
    
    # The rest of the commands do nothing
    def control_send_letter(self):
        return True
    
    def control_sendonoff(self):
        return True
    
    def control_alwaysontop(self):
        return True
    
    def control_me_control(self):
        return True
     