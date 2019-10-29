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
    
    '''Creates the graphical components of the main window.
    '''
    def __init__(self, master=None):
        self.root = master
        
        #allows frames to resize with window
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_rowconfigure(0, weight = 1)       
        
        #creates the frames that widgets will be placed in
        self.top_frame  = tk.Frame(self.root, width = 1215, height = 250) 
        self.uplink_frame = tk.Frame(self.root, width = 1215, height = 70)
        self.inputFrame = tk.Frame(self.root, width = 1215, height = 50)
        self.command_frame = tk.Frame(self.top_frame, width = 405, height = 250)
        self.canvas_frame = tk.Frame(self.top_frame, width = 405, height = 250)
        self.console_frame = tk.Frame(self.root, width = 405, height = 350)
        self.table_frame = tk.Frame(self.top_frame, width = 405, height = 350)
        self.bottommost_frame = tk.Frame(self.root, width = 1215, height = 30)

        #stops widgets from changing frame sizes
        self.top_frame.grid_propagate(False)
        self.uplink_frame.grid_propagate(False)
        self.inputFrame.grid_propagate(False)
        self.command_frame.grid_propagate(False)
        self.canvas_frame.grid_propagate(False)
        self.console_frame.grid_propagate(False)
        self.table_frame.grid_propagate(False)
        self.bottommost_frame.grid_propagate(False)
        
        #places the frames in the window        
        self.top_frame.grid(row = 0, column = 0, sticky = tk.W + tk.E + tk.S + tk.N)
        self.uplink_frame.grid(row = 1, column = 0, sticky = tk.W + tk.E + tk.S + tk.N)
        self.inputFrame.grid(row = 2, column = 0, sticky = tk.W + tk.E + tk.S + tk.N)
        self.command_frame.grid(row = 0, column = 0, sticky = tk.W + tk.E + tk.S + tk.N)
        self.canvas_frame.grid(row = 0, column = 1, sticky = tk.W + tk.E + tk.S + tk.N)
        self.console_frame.grid(row = 3, column = 0, sticky = tk.W + tk.E + tk.S + tk.N)
        self.table_frame.grid(row = 0, column = 2, sticky = tk.W + tk.E + tk.S + tk.N)
        self.bottommost_frame.grid(row = 4, column = 0, sticky = tk.W + tk.E + tk.S + tk.N)
        
        #allows top frames to resize with window
        self.top_frame.grid_columnconfigure(0, weight = 1)
        self.top_frame.grid_columnconfigure(1, weight = 1)
        self.top_frame.grid_columnconfigure(2, weight = 1)
        self.top_frame.grid_rowconfigure(0, weight = 1)
        
        #initialises widgets in window
        self.root.title("GUI")
        self.init_buttons()
        self.init_console()
        self.init_table()
        self.init_canvas()
        self.controller = cont.Controller(self.table, self.console, self.canvas, self.scrollBar, self.scrollBar2, self.root)
        self.init_uplink_frame()
        self.init_input_frame()
        self.init_bottommost_frame()
    
    '''Initialises the widgets in the bottommost frame.
    '''  
    def init_bottommost_frame(self):
        print_gui_Button = tk.Button(self.bottommost_frame, text = "Print to GUI", command = lambda : self.controller.switchOutput(1))
        print_console_Button = tk.Button(self.bottommost_frame, text = "Print to Console", command = lambda : self.controller.switchOutput(0))

        print_gui_Button.grid(row = 0, column = 0, sticky = tk.W + tk.E, padx = 2, pady = 2)
        print_console_Button.grid(row = 0, column = 1, sticky = tk.W + tk.E, padx = 2, pady = 2)
    
    '''Initialises the widgets in the input frame.
    '''     
    def init_input_frame(self):
        self.input = tk.StringVar()
        self.input.set("")
        
        inputLabel = tk.Label(self.inputFrame, text="Input:")
        inputLabel.grid(row = 0, column = 0,sticky = tk.W + tk.E,)
        
        self.inputEdit = tk.Entry(self.inputFrame, textvariable=self.input)
        self.inputEdit.grid(row = 0, column = 1, sticky = tk.W + tk.E, padx = 2, pady = 2)
        
        send_tleButton = tk.Button(self.inputFrame, text = "Send TLE", command = lambda : self.controller.send_tle((self.inputEdit.get())))
        send_tleButton.grid(row = 0, column = 2, sticky = tk.W + tk.E, padx = 2, pady = 2)
        print self.inputEdit.get()
        sendCmd = tk.Button(self.inputFrame, text = "Send Command", command = lambda : self.controller.customCommand(self.inputEdit.get()))
        sendCmd.grid(row = 0, column = 3, sticky = tk.W + tk.N, padx = 2, pady = 2)
        
        self.inputFrame.grid_columnconfigure(1, weight = 1)
     
    '''Initialises the widgets in the uplink frame.
    '''     
    def init_uplink_frame(self):
        #gets the list of open ports
        ports = self.controller.getPorts()
        self.upComVar = tk.StringVar()          
        self.upComVar.set(ports[0])
        
        self.downComVar = tk.StringVar()          
        self.downComVar.set(ports[0])

        #creates and places the labels and drop down menus
        upComLabel = tk.Label(self.uplink_frame, text="Uplink COM:")
        upComLabel.grid(row = 0, column = 0)
        
        downComLabel = tk.Label(self.uplink_frame, text="Downlink COM:")
        downComLabel.grid(row = 1, column = 0)
        
        selectUpPort = tk.OptionMenu(self.uplink_frame, self.upComVar, "")
        selectUpPort.grid(row = 0, column = 1, sticky = tk.W + tk.E, padx = 2, pady = 2)
        selectUpPort['menu'].delete(0, 'end')
        
        selectDownPort = tk.OptionMenu(self.uplink_frame, self.downComVar, "")
        selectDownPort.grid(row = 1, column = 1, sticky = tk.W + tk.E, padx = 2, pady = 2)
        selectDownPort['menu'].delete(0, 'end')
        
        #Adds each open port to the drop down menus
        for port in ports:
            selectUpPort['menu'].add_command(label=port, command=tk._setit(self.upComVar, port))
            selectDownPort['menu'].add_command(label=port, command=tk._setit(self.downComVar, port))
            
        self.upRateVar = tk.StringVar() 
        self.downRateVar = tk.StringVar() 
        
        #Default rate value is 115200
        self.upRateVar.set("115200")
        self.downRateVar.set("115200")
        
        #creates nd places the rest of the widgets in the fame
        upRateLabel = tk.Label(self.uplink_frame, text="Uplink Rate:")
        upRateLabel.grid(row = 0, column = 2)
        
        downRateLabel = tk.Label(self.uplink_frame, text="Downlink Rate:")
        downRateLabel.grid(row = 1, column = 2)
        
        upRateEdit = tk.Entry(self.uplink_frame, textvariable=self.upRateVar)
        upRateEdit.grid(row = 0, column = 3)
        upRateEdit.insert(0, self.controller.upRate) 
        
        downRateEdit = tk.Entry(self.uplink_frame, textvariable=self.downRateVar)
        downRateEdit.grid(row = 1, column = 3)
        downRateEdit.insert(0, self.controller.downRate) 
        
        setConnBtn = tk.Button(self.uplink_frame, text = "Set Connection", command = lambda : self.setComNRate(self.upComVar.get(), self.upRateVar.get(), self.downComVar.get(), self.downRateVar.get()))
        openConnBtn = tk.Button(self.uplink_frame, text = "Open Connection", command = lambda : self.controller.openConn())
        closeConnBtn = tk.Button(self.uplink_frame, text = "Close Connection", command = lambda : self.controller.closeConn())
        
        setConnBtn.grid(row = 0, column = 4, sticky = tk.W + tk.E, padx = 4, pady = 2) 
        openConnBtn.grid(row = 0, column = 5, sticky = tk.W + tk.E, padx = 4, pady = 2)
        closeConnBtn.grid(row = 0, column = 6, sticky = tk.W + tk.E, padx = 4, pady = 2)
        
    '''Creates and places the command buttons in the command frame.
    '''
    def init_buttons(self):
        tmOrbitButton = tk.Button(self.command_frame, text = "TM_Orbit", command = lambda : self.controller.showOrbitTM())
        picButton = tk.Button(self.command_frame, text = "Get_Pic", command = lambda : self.controller.showPic())
        get_tm_healthButton = tk.Button(self.command_frame, text = "Tm_Health", command = lambda : self.controller.show_tm_health())
        get_tm_initButton = tk.Button(self.command_frame, text = "Tm_Init", command = lambda : self.controller.show_tm_init())
        adcs_offButton = tk.Button(self.command_frame, text = "Adcs_Off", command = lambda : self.controller.turn_adcs_off())
        adcs_resetButton = tk.Button(self.command_frame, text = "Adcs_Reset", command = lambda : self.controller.reset_adcs())
        radios_kill_allButton = tk.Button(self.command_frame, text = "Radios_Kill_All", command = lambda : self.controller.radio_kill())
        radio_uhf_killButton = tk.Button(self.command_frame, text = "Radios_Kill_UHF", command = lambda : self.controller.uhf_radio_kill())
        radio_sband_killButton = tk.Button(self.command_frame, text = "Radios_Kill_Sband", command = lambda : self.controller.radio_sband_kill())
        payload_killButton = tk.Button(self.command_frame, text = "Payload_Kill", command = lambda : self.controller.kill_payload())
        
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
                        
    ''''Creates and places the console in the console frame.
    '''
    def init_console(self):
       
        self.console = tk.Text(self.console_frame)
        self.scrollBar = ttk.Scrollbar(self.console_frame, command=self.console.yview)
        self.scrollBar.grid(row=0, column=1, sticky='nsew')
        #binds the console and the scrollbar
        self.console.config(yscrollcommand = self.scrollBar.set)
        self.console.grid(row = 0, column = 0, sticky = tk.W + tk.E + tk.S + tk.N, padx = 2, pady = 2)
        #allows the console to resize with the frame
        self.console_frame.grid_columnconfigure(0, weight = 1)
        self.console_frame.grid_rowconfigure(0, weight = 1)
        #stops users from editing the text in the console
        self.console.configure(state='disabled')
     
    '''Sets the uplink and downlink values for the controller.    
    '''
    def setComNRate(self, upCom, upRate, downCom, downRate):
        if self.controller.is_int(upRate) and int(upRate) > 0 and self.controller.is_int(downRate) and int(downRate) > 0:
            self.controller.upCom = upCom
            self.controller.upRate = upRate
            self.controller.downCom = downCom
            self.controller.downRate = downRate
        else:
            tkm.showerror("Invalid Rate Format", "Please provide a valid rate")
        
    '''Creates and places the text box for the table. 
    '''
    def init_table(self):
        self.table = tk.Text(self.table_frame)
        self.scrollBar2 = ttk.Scrollbar(self.table_frame, command=self.table.yview)
        self.scrollBar2.grid(row=0, column=1, sticky='nsew')
        #binds the table and the scrollbar
        self.table.config(yscrollcommand = self.scrollBar2.set)
        self.table.grid(row = 0, column = 0, sticky = tk.W + tk.E + tk.S + tk.N, padx = 2, pady = 2)
        #allows the table to resize with the frame
        self.table_frame.grid_columnconfigure(0, weight = 1)
        self.table_frame.grid_rowconfigure(0, weight = 1)
        #stops users from editing the text in the table
        self.table.configure(state='disabled') 

    '''Creates and places the canvas for displaying the 3d model and images.    
    '''
    def init_canvas(self):
        self.canvas_frame.grid_columnconfigure(0, weight = 1)
        self.canvas_frame.grid_rowconfigure(0, weight = 1)
        self.canvas = tk.Canvas(self.canvas_frame) 
        self.canvas.grid(row = 0, column = 0, sticky='nsew', padx = 2, pady = 2)