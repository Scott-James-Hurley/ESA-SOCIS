'''
Created on 6 Jun 2019

@author: Scott Hurley
         scott.james.hurley.97@gmail.com
'''

'''
This class acts as the controller between the model(ground) and the 
view(main_window) as part of the Model View Controller design pattern.
'''
import csv as csv
import Tkinter as tk
import ground as gnd
import ground_client as gndc
import threading as thd
import io
import base64
import sys
import glob
import serial
import time
from PIL import ImageTk,Image
import tkMessageBox as tkm
import ast
import struct
from cStringIO import StringIO

class Controller(object):
    '''
    classdocs
    '''
                
    '''Initialises the instance variables.
    '''
    def __init__(self, table, console, canvas, scrollBar, scrollBar2, root):
        '''
        Constructor
        '''
        self.port_timeout = 0.2
        self.connIsOpen = False
        self.table = table
        self.console = console 
        self.canvas = canvas 
        self.scrollBar = scrollBar
        self.scrollBar2 = scrollBar2 
        self.root = root
        self.pic_data = ""
        self.picture_data = None
        self.upCom = ""
        self.downCom = ""
        self.upRate = ""
        self.downRate = ""
        self.uplink = 0
        self.downlink = 0
        self.tableContents = tk.StringVar()
        self.tableContents.trace("w", self.write_table)
        self.display_image_from_disk("path")
        self.output = ""
        self.outputList = []
        self.tableList = []
        self.sendpkString = ""
        #command queue
        self.todo = []
        #keeps track of stdout length
        self.outputHistoryLen = 0
        #keeps original stdout value for printing to console
        self.old_stdout = sys.stdout
        #redirects stdout to string
        sys.stdout = self.mystdout = StringIO()
        
        self.console.after(0, self.updatePacketContents)  
    
    '''Returns true if input is an integer, else false.
    '''
    def is_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False
    
    '''If input is true, output is redirected to the GUI, else the console.
    '''   
    def switchOutput(self, switchValue):
        if switchValue:
            sys.stdout = self.mystdout
        else:
            sys.stdout = self.old_stdout
            
    '''Closes any opened ports.
    '''   
    def closeConn(self):
        if self.downlink != 0:
            self.connIsOpen = False
            self.thread.join()
            self.downlink.close()
            #if the uplink and the downlink aren't the same, close the uplink as well
            if self.upCom != self.downCom and self.upRate != self.downRate:
                self.uplink.close()
            self.downlink = 0
            self.uplink = 0
    
    '''Opens ports requested by user for uplink and downlink.
    '''    
    def openConn(self):
        #if user values are valid and there arent's any ports already opened
        if self.upCom != "" and self.upRate != "" and self.downlink == 0 and self.downCom != "" and self.downRate != "" and self.uplink == 0:
            #if the up and down ports are the same but the rates are different
            if self.upCom == self.downCom and self.upRate != self.downRate:
                tkm.showerror("Invalid Connection Configuration", "Please provide a valid connection configuration")
            else:
                self.downlink = gndc.port_init(self.downCom,self.downRate, self.port_timeout)
                #if the uplink and the downlink are the same
                if self.upCom == self.downCom and self.upRate == self.downRate:
                    gnd.init(self.downlink, self.downlink, self.port_timeout, silent = 0)
                else:
                    self.uplink = gndc.port_init(self.upCom,self.upRate, self.port_timeout)  
                    gnd.init(self.uplink, self.downlink, self.port_timeout, silent = 0)
                self.connIsOpen = True
                #starts the thread that listens for packets
                self.thread = thd.Thread(target= self.getPacket)
                self.thread.setDaemon(True)
                self.thread.start()
        elif self.downlink != 0 or self.uplink != 0:
            tkm.showerror("Connection Already Open", "Please close the previous connection")
        else:
            tkm.showerror("Invalid Connection Info", "Please provide valid connection information")
    
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """       
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
        
        
    '''Following functions call their corresponding functions in the model and print
       the results to the table.
    '''
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
     
    '''creates a table from data and writes it to disk as a CSV file 
    '''  
    def csv_write_to(self, file_name, labels_values):
        labels = labels_values[0]
        values = labels_values[1]
        
        with open(file_name + '.csv', mode='w') as file:
            i = 0
            file_writer = csv.writer(file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            
            while i < len(labels) and i < len(values):
                file_writer.writerow([labels[i], values[i]])
    
    '''Updates the GUI's console and table. Is inserted into Tkinter's mainloop
    '''            
    def updatePacketContents(self):
        if(self.connIsOpen == True):
            self.cullString()
            if len(self.tableList) > 0:
                if self.tableList[0] != [] and self.tableList[1] != []:
                    self.tableContents.set(str(self.tableList))
        
        self.console.after(100, self.updatePacketContents) 
    
    '''Runs on a separate thread and listens for packets from the satellite. Also
       executes any commands in the todo queue.
    '''
    def getPacket(self):
        while(self.connIsOpen == True):
            (fromto, typ, pkrssi, data) = gnd.getpk()
            (labels, values) = self.printpk(fromto, typ, data)
            self.tableList = [labels, values]
             
            while len(self.todo) > 0:                
                if len(self.todo[0]) == 2:                    
                    self.sendpkString = self.todo[0][0](self.todo[0][1])
                if len(self.todo[0]) == 3:
                    self.sendpkString = self.todo[0][0](self.todo[0][1], self.todo[0][2])                  
                del self.todo[0] 
                   
            time.sleep(0.25)
     
    '''Prints new values from stdout to the GUI's console
       Note: self.outputHistoryLen keeps track of length of stdout. This keeps updating the
       GUI console efficient as only new information is added instead of everything. 
    '''
    def cullString(self):
        consoleString = self.mystdout.getvalue()
        consoleOutput = consoleString.split('\n')
        for line in consoleOutput:
            line += "\n"
            
        if len(consoleOutput) > self.outputHistoryLen:
            self.outputList = consoleOutput[self.outputHistoryLen - 1:]
            self.write_console() 
         
        self.outputHistoryLen = len(consoleOutput)
    
    '''Prints output to the GUI's console. Also controls the console's scrollbar.
    '''     
    def write_console(self, *args):
        numlines = self.console.index('end - 1 line').split('.')[0]
        self.console.configure(state='normal')
            
        for line in self.outputList:
            self.console.insert(tk.END, line)
            self.console.insert(tk.END, '\n')
        self.console.configure(state='disabled')
        
        if int(numlines) > 100:
            diff = (int(numlines) - 100) + 1            
            self.console.delete(1.0, float(diff))
        
        if self.scrollBar.get()[1] > 0.9:
            self.console.yview_pickplace("end")
        
    '''Creates a table from data and displays it in the GUI.
    '''
    def write_table(self, *args):
        i = 0
        y = self.tableContents.get()
        if(y != "[]"):
            while i < len(y):
                if y[i] == ']':
                    i += 1
                    break
                i += 1
    
            list1Str = y[1:i]
            list2Str = y[i+2:-1]
            
            labels = ast.literal_eval(list1Str)
            
            values = ast.literal_eval(list2Str)
            
            i = 0
            table = ""
            tableList = []
            
            while i < len(labels) and i < len(values):
                table += labels[i] + "\t" + str(values[i]) + "\n"
                tableList.append(labels[i] + "\t" + str(values[i]) + "\n")
                i += 1

            self.table.configure(state='normal')
            self.table.delete(1.0,tk.END)
            for line in tableList:
                self.table.insert(tk.END, line)
            self.table.configure(state='disabled')

    '''Prints packets information. Identical to the function found in ground.py
       except it return lists for keys and values instead of a dictionary of them.
    '''
    def printpk(self, fromto, pktyp, pkdata):
        if pktyp == '~':
            gnd.printout(' beacon! ')
            gnd.printout(pkdata[:-1])

        if pktyp == '+':
            gnd.printout (' info = ' + pkdata[:-1])
          
        if pktyp == '#':
            gnd.printout(' adcs_telemetry packet len = ' + str(len(pkdata)) + '\r\n')
            ix = 0
            tmlen = 52
            # I:ui32 B:ui8 h:i16 b:i8 H:ui16
            adcs_tm = struct.unpack('I6B3h3b3bb8b3b3b3b10BbB',pkdata[:tmlen])
            gnd.printout(' adcs_tm ' + str(adcs_tm))
            gnd.printout(' \r\n')
            
            tm_adcs_keys = ['uptime_adcs', 
                         'rtc_adcs_year', 'rtc_adcs_month', 'rtc_adcs_day', 
                         'rtc_adcs_hour', 'rtc_adcs_minute', 'rtc_adcs_second', 
                         'sat_pos_x', 'sat_pos_y', 'sat_pos_z',
                         'mag_x', 'mag_y', 'mag_z', 
                         'gyro_x', 'gyro_y', 'gyro_z', 
                         'gyro_tempC',
                         
                         'sun1_x1', 'sun1_x2', 'sun1_y1', 'sun1_y2'
                         'sun2_x1', 'sun2_x2', 'sun2_y1', 'sun2_y2'
    
                         'rpm1', 'rpm2', 'rpm3',
                         'rwd1', 'rwd2', 'rwd3',
                         'mtq1', 'mtq2', 'mtq3',
                         
                         'adc_adcs_1', 'adc_adcs_2', 'adc_adcs_3', 'adc_adcs_4',
                         'adc_adcs_5', 'adc_adcs_6', 'adc_adcs_7', 'adc_adcs_8',
                         'adc_adcs_9', 'adc_adcs_10',
                         
                         'mode_adcs', 
                         'crc_adcs' ]
            
            gnd.printout('## uptime_adcs, ' + str(adcs_tm[ix]) + '\r\n' )
        
            ix += 1
            gnd.printout('   rtc_adcs,    ' + str(adcs_tm[ix:ix+6]) + '\r\n' )
            ix += 6
            gnd.printout('   sat_pos,     ' + str(adcs_tm[ix:ix+3]) + '\r\n' )
            ix += 3
            gnd.printout('   mag,         ' + str(adcs_tm[ix:ix+3]) + '\r\n' )
            ix+=3
            gnd.printout('   gyro,        ' + str(adcs_tm[ix:ix+3]) + '' )
            ix+=3
            gnd.printout('   gyro_tempC, ' + str(adcs_tm[ix]) + '\r\n' )
            ix+=1
            gnd.printout('   sun_raw,     ' + str(adcs_tm[ix:ix+8]) + '\r\n' )
            ix+=8
            gnd.printout('   rpm,         ' + str(adcs_tm[ix:ix+3]) + '\r\n' )
            ix+=3
            gnd.printout('   rwd,         ' + str(adcs_tm[ix:ix+3]) + '\r\n' )
            ix+=3
            gnd.printout('   mtq,         ' + str(adcs_tm[ix:ix+3]) + '\r\n' )
            ix+=3
            gnd.printout('   adc_adcs,    ' + str(adcs_tm[ix:ix+10]) + '\r\n' )
            ix+=10
            gnd.printout('   mode_adcs,   ' + str(adcs_tm[ix:ix+1]) + '\r\n' )
            ix+=1
            gnd.printout('   crc_adcs,    ' + hex(adcs_tm[ix]) + ' ?= ' + hex( gnd.getcrc(pkdata[:tmlen-1]) ) + '\r\n' )
            ix+=1
            gnd.printout (pkdata[tmlen:])
            
            adcs_tm_dic = dict(zip(tm_adcs_keys, adcs_tm))
            
            gnd.printout(str( adcs_tm_dic))
            
            return (tm_adcs_keys, adcs_tm)
    
        if pktyp == '?':
            gnd.printout(' obc_telemetry packet len = ' + str(len(pkdata)) + '\r\n')
            ix = 0
            tmlen = 45
            # I:ui32 B:ui8 h:i16 b:i8 H:ui16
            obc_tm = struct.unpack('I6BH3B8b3h9BHBBB',pkdata[:tmlen])
            gnd.printout('obc_tm ' + str(obc_tm))
            gnd.printout(' \r\n')
            
            tm_obc_keys = ['uptime_adcs', 
                         'rtc_adcs_year', 'rtc_adcs_month', 'rtc_adcs_day', 
                         'rtc_adcs_hour', 'rtc_adcs_minute', 'rtc_adcs_second', 
                         'sat_pos_x', 'sat_pos_y', 'sat_pos_z',
                         'mag_x', 'mag_y', 'mag_z', 
                         'gyro_x', 'gyro_y', 'gyro_z', 
                         'gyro_tempC',
                         
                         'sun1_x1', 'sun1_x2', 'sun1_y1', 'sun1_y2'
                         'sun2_x1', 'sun2_x2', 'sun2_y1', 'sun2_y2'
    
                         'rpm1', 'rpm2', 'rpm3',
                         'rwd1', 'rwd2', 'rwd3',
                         'mtq1', 'mtq2', 'mtq3',
                         
                         'adc_adcs_1', 'adc_adcs_2', 'adc_adcs_3', 'adc_adcs_4',
                         'adc_adcs_5', 'adc_adcs_6', 'adc_adcs_7', 'adc_adcs_8',
                         'adc_adcs_9', 'adc_adcs_10',
                         
                         'mode_adcs', 
                         'crc_adcs' ]
            
            gnd.printout('?? uptime_obc,    ' + str(obc_tm[ix]) + '\r\n' )
            ix+=1
           
            gnd.printout('   rtc_obc,       ' + str(obc_tm[ix:ix+6]) + '\r\n' )
            ix+=6
            gnd.printout('   eps,           ' + str(obc_tm[ix]) + '\r\n' )
            ix+=1
    
            gnd.printout('   rssi,          ' + str(obc_tm[ix:ix+3]) + '\r\n' )
            ix+=3
    
            gnd.printout('   sol_t_all,     ' + str(obc_tm[ix:ix+8]) + '\r\n' )
            ix+=8
            gnd.printout('   bat_v_i_t,     ' + str(obc_tm[ix:ix+3]) + ' <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< \r\n' )
            ix+=3
            gnd.printout('   adc_obc,       ' + str(obc_tm[ix:ix+9]) + '\r\n' )
            gnd.printout('                   (solar_i, payload_i, 3v3_i, 3v3_v, 8v4_i, 8v4_v, uhf_5v_i, sband_5v_i, radio_3v3_i) \r\n')
            ix+=9
            gnd.printout('   reset_cnt,     ' + str(obc_tm[ix]) + '\r\n')
            ix+=1
            gnd.printout('   tle_crc,       ' + str(hex(obc_tm[ix])) + '\r\n')
            ix+=1
            gnd.printout('   isl,           ' + str(hex(obc_tm[ix])) + '\r\n')
            ix+=1
            gnd.printout('   crc_obc,       ' + hex(obc_tm[ix]) + ' ?= ' + hex( gnd.getcrc(pkdata[:tmlen-1]) ) + '\r\n' )
            ix+=1
            gnd.printout (pkdata[tmlen:])
            
            obc_tm_dic = dict(zip(tm_obc_keys, obc_tm))
            
            gnd.printout(str( adcs_tm_dic))
            
            return (tm_adcs_keys, adcs_tm)
            
        return ([], [])
                
    def process_pic_packets(self, data):
        print "pics or gtfo"
     
    '''Produces an image from byte data.  
    '''
    def display_image_from_data(self, data):
        f = io.BytesIO(base64.b64decode(data))
        self.image = Image.open(f)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor = tk.NW, image = self.img)
        
    '''Loads an image from the specified path and displays it in the GUI. 
    '''
    def display_image_from_disk(self, path):
        path = r'earth.png'
        self.img = ImageTk.PhotoImage(Image.open(path))
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor = tk.NW, image = self.img)
        
    '''Saves data as a file on disk
       overwrites existing data, if the file doesn't already exist it's created
    '''
    def save_to_file(self, filename, data):
        newFile = open(filename, "wb")
        newFileByteArray = bytearray(data, 'utf-8')
        newFile.write(newFileByteArray)