'''
Created on 6 Jun 2019

@author: Scott Hurley
         scott.james.hurley.97@gmail.com
'''

'''
This class acts as the view component of the Model View Controller design 
pattern. It creates the main window and all of its contents.
'''

import Tkinter as tk
import ttk
import controller as cont
import tkMessageBox as tkm

class MainWindow(tk.Frame):
    
    #creates the graphical components of the main window
    def __init__(self, master=None):
        self.root = master
        
        self.top_left_frame = tk.Frame(self.root, width = 410, height =100)
        self.middle_left_frame = tk.Frame(self.root, width = 410, height = 20)
        self.bottom_left_frame = tk.Frame(self.root, width = 410, height = 20)

        self.top_left_frame.grid_propagate(False)
        self.middle_left_frame.grid_propagate(False)
        self.bottom_left_frame.grid_propagate(False)
                
        self.top_left_frame.grid(row = 0, column = 0, sticky = tk.W + tk.E + tk.S + tk.N)
        self.middle_left_frame.grid(row = 1, column = 0, sticky = tk.W + tk.E + tk.S + tk.N)
        self.bottom_left_frame.grid(row = 2, column = 0, sticky = tk.W + tk.E + tk.S + tk.N)
        
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_rowconfigure(1, weight = 1)
        self.root.grid_rowconfigure(2, weight = 1)
        
        self.root.title("GUI")
        self.root.resizable(1, 0)  
        self.init_window()   
        self.controller = cont.Controller(self.console)
        self.init_middle_frame()
        
    def init_window(self):
        self.init_buttons()  
        self.init_console()
        
    #creates and places the command buttons
    def init_buttons(self):
        tmOrbitButton = tk.Button(self.top_left_frame, text = "TM_Orbit", command = lambda : self.controller.showOrbitTM())
        picButton = tk.Button(self.top_left_frame, text = "Get_Pic", command = lambda : self.controller.showPic())
        get_tm_healthButton = tk.Button(self.top_left_frame, text = "Tm_Health", command = lambda : self.controller.show_tm_health())
        get_tm_initButton = tk.Button(self.top_left_frame, text = "Tm_Init", command = lambda : self.controller.show_tm_init())
        adcs_offButton = tk.Button(self.top_left_frame, text = "Adcs_Off", command = lambda : self.controller.turn_adcs_off())
        adcs_resetButton = tk.Button(self.top_left_frame, text = "Adcs_Reset", command = lambda : self.controller.reset_adcs())
        radios_kill_allButton = tk.Button(self.top_left_frame, text = "Radios_Kill_All", command = lambda : self.controller.radio_kill())
        radio_uhf_killButton = tk.Button(self.top_left_frame, text = "Radios_Kill_UHF", command = lambda : self.controller.uhf_radio_kill())
        radio_sband_killButton = tk.Button(self.top_left_frame, text = "Radios_Kill_Sband", command = lambda : self.controller.radio_sband_kill())
        payload_killButton = tk.Button(self.top_left_frame, text = "Payload_Kill", command = lambda : self.controller.kill_payload())
        setConnBtn = tk.Button(self.top_left_frame, text = "Set Connection", command = lambda : self.setComNRate(self.comVar.get(), self.rateVar.get()))
        openConnBtn = tk.Button(self.top_left_frame, text = "Open Connection", command = lambda : self.controller.openConn())
        closeConnBtn = tk.Button(self.top_left_frame, text = "Close Connection", command = lambda : self.controller.closeConn())
        
        tmOrbitButton.grid(row = 0, column = 0, sticky = tk.W + tk.E, padx = 2, pady = 2)
        picButton.grid(row = 0, column = 1, sticky = tk.W + tk.E, padx = 2, pady = 2)
        get_tm_healthButton.grid(row = 0, column = 3, sticky = tk.W + tk.E, padx = 2, pady = 2)
        get_tm_initButton.grid(row = 1, column = 0, sticky = tk.W + tk.E, padx = 2, pady = 2)
        adcs_offButton.grid(row = 1, column = 1, sticky = tk.W + tk.E, padx = 2, pady = 2)
        adcs_resetButton.grid(row = 1, column = 2, sticky = tk.W + tk.E, padx = 2, pady = 2)
        radios_kill_allButton.grid(row = 1, column = 3, sticky = tk.W + tk.E, padx = 2, pady = 2)
        radio_uhf_killButton.grid(row = 2, column = 0, sticky = tk.W + tk.E, padx = 2, pady = 2)
        radio_sband_killButton.grid(row = 2, column = 1, sticky = tk.W + tk.E, padx = 2, pady = 2)
        payload_killButton.grid(row = 0, column = 2, sticky = tk.W + tk.E, padx = 2, pady = 2)
        setConnBtn.grid(row = 3, column = 0, sticky = tk.W + tk.E, padx = 2, pady = 40) 
        openConnBtn.grid(row = 3, column = 1, sticky = tk.W + tk.E, padx = 2, pady = 40)
        closeConnBtn.grid(row = 3, column = 2, sticky = tk.W + tk.E, padx = 2, pady = 40)
        
    def init_middle_frame(self):
        ports = self.controller.getPorts()
        self.comVar = tk.StringVar()          
        self.comVar.set(ports[0])

        comLabel = tk.Label(self.middle_left_frame, text="COM:")
        comLabel.grid(row = 0, column = 0)
        selectPort = tk.OptionMenu(self.middle_left_frame, self.comVar, "")
        selectPort.grid(row = 0, column = 1, sticky = tk.W + tk.E, padx = 2, pady = 2)
        selectPort['menu'].delete(0, 'end')
        for port in ports:
            selectPort['menu'].add_command(label=port, command=tk._setit(self.comVar, port))
            
        self.rateVar = tk.StringVar() 
        #Default rate value is 115200
        self.rateVar.set("115200")
        rateLabel = tk.Label(self.middle_left_frame, text="Rate:")
        rateLabel.grid(row = 0, column = 2)
        rateEdit = tk.Entry(self.middle_left_frame, textvariable=self.rateVar)
        rateEdit.grid(row = 0, column = 3)
        rateEdit.insert(0, self.controller.rate) 
                
    #creates and places the console for entering custom commands
    def init_console(self):
        consoleLabel = tk.Label (self.bottom_left_frame, text = "Command: ")
        consoleLabel.grid(row = 0, column = 0, sticky = tk.W + tk.N, padx = 2, pady = 2)
        
        self.console = tk.Entry(self.bottom_left_frame)
        self.console.grid(row = 0, column = 1, sticky = tk.W + tk.E + tk.N, padx = 2, pady = 2)
        
        self.bottom_left_frame.grid_columnconfigure(1, weight = 1)
        self.bottom_left_frame.grid_rowconfigure(0, weight = 0)
        self.bottom_left_frame.grid_rowconfigure(1, weight = 0)
        
        sendCmd = tk.Button(self.bottom_left_frame, text = "Send Command", command = lambda : self.controller.customCommand(self.console.get()))
        sendCmd.grid(row = 1, column = 0, sticky = tk.W + tk.N, padx = 2, pady = 2)
        
        sendCmd = tk.Button(self.bottom_left_frame, text = "Send TLE", command = lambda : self.controller.customCommand(self.console.get()))
        sendCmd.grid(row = 2, column = 0, sticky = tk.W + tk.N, padx = 2, pady = 2)
        
    #Checks the user input and if valid, sets the serial port and rate and destroys the dialog 
    def setComNRate(self, com, rate):
        if self.controller.is_int(rate) and int(rate) > 0:
            self.controller.com = com
            self.controller.rate = rate
        else:
            tkm.showerror("Invalid Rate Format", "Please provide a valid rate")