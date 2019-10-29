'''
Created on 6 Jun 2019

@author: Scott Hurley
         scott.james.hurley.97@gmail.com
'''

'''
This class acts as the controller between the model(ground) and the 
view(main_window) as part of the Model View Controller design pattern.
'''

import Tkinter as tk
import ground as gnd
import ground_client as gndc
import threading as thd
import sys
import glob
import serial
import time
import tkMessageBox as tkm
import ast

class Controller(object):
    '''
    classdocs
    '''
                   
    #initialises the objects needed for the class
    def __init__(self, console):
        '''
        Constructor
        '''
        self.port_timeout = 0.2
        self.connIsOpen = False
        self.console = console 
        self.com = ""
        self.rate = ""
        self.downlink = 0
        self.todo = []
    
    #Returns true if s is an integer, else false
    def is_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False
     
    #Waits for the thread to end then closes the downlink   
    def closeConn(self):
        if self.downlink != 0:
            self.connIsOpen = False
            self.thread.join()
            self.downlink.close()
            self.downlink = 0
    
    #Gets packets and prints them to console      
    def writeConsoleThread(self):
        while(self.connIsOpen == True):
            (fromto, typ, pkrssi, data) = gnd.getpk()
            gnd.printpk(fromto, typ, data)
            while len(self.todo) > 0:                
                if len(self.todo[0]) == 2:                    
                    self.todo[0][0](self.todo[0][1])
                if len(self.todo[0]) == 3:
                    self.todo[0][0](self.todo[0][1], self.todo[0][2])                  
                del self.todo[0]           
     
    #Initialises the downlink with the selected serial port and starts the thread
    #to get packets
    def openConn(self):
        if self.com != "" and self.rate != "" and self.downlink == 0:
            self.downlink = gndc.port_init(self.com,self.rate, self.port_timeout)
            gnd.init(self.downlink, self.downlink, self.port_timeout, silent = 0) 
            self.connIsOpen = True
            
            self.thread = thd.Thread(target= self.writeConsoleThread)
            self.thread.setDaemon(True)
            self.thread.start()           
        elif self.downlink != 0:
            tkm.showerror("Connection Already Open", "Please close the previous connection")
        else:
            tkm.showerror("Invalid Connection Info", "Please provide valid connection information")
     
    #Returns a list of all open serial ports. Should work on Linux, MacOS and Windows   
    def getPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
        
        
    #these functions call their corresponding functions in the model 
    def customCommand(self, command):
        print command
        if(self.connIsOpen):
            self.todo += [[gnd.sendpk, gnd.to_unicorn['2B'], '!', command + '\0\r\n']]
          
    def showOrbitTM(self):
        if(self.connIsOpen):
            self.todo += [[gnd.cmd_get_tm_orbit, gnd.to_unicorn['2B']]]
                        
    def showPic(self):
        if(self.connIsOpen):
            #self.todo += [[gnd.cmd_get_pic_test(gnd.to_unicorn['2B'], False)]]
            1
                
    def send_tle(self, tle):
        if(self.connIsOpen):
            self.todo += [[gnd.cmd_send_tle, gnd.to_unicorn['2B'], tle]]
                
    def show_tm_health(self):
        if(self.connIsOpen):
            self.todo += [[gnd.cmd_get_tm_health, gnd.to_unicorn['2B']]]
            
    def show_tm_init(self):
        if(self.connIsOpen):
            self.todo += [[gnd.cmd_get_tm_init, gnd.to_unicorn['2B']]]
                
    def turn_adcs_off(self):
        if(self.connIsOpen):
            self.todo += [[gnd.cmd_adcs_off, gnd.to_unicorn['2B']]]
                
    def reset_adcs(self):
        if(self.connIsOpen):
            self.todo += [[gnd.cmd_adcs_reset, gnd.to_unicorn['2B']]]
                
    def radio_kill(self):
        if(self.connIsOpen):
            self.todo += [[gnd.cmd_radios_kill_all, gnd.to_unicorn['2B']]]
                
    def uhf_radio_kill(self):
        if(self.connIsOpen):
            self.todo += [[gnd.cmd_radio_uhf_kill, gnd.to_unicorn['2B']]]
                
    def radio_sband_kill(self):
        if(self.connIsOpen):
            self.todo += [[gnd.cmd_radio_sband_kill, gnd.to_unicorn['2B']]]
                
    def kill_payload(self):
        if(self.connIsOpen):
            self.todo += [[gnd.cmd_payload_kill, gnd.to_unicorn['2B']]]