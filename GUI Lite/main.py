'''
Created on 6 Jun 2019

@author: Scott Hurley
         scott.james.hurley.97@gmail.com
'''

'''
This file creates and runs the GUI. Run this file if you want to use it.
'''

import Tkinter as tk
import main_window as mw

if __name__ == '__main__':
    root = tk.Tk() 
    root.minsize(500, 350)
    app = mw.MainWindow(root)
    root.mainloop()
    pass