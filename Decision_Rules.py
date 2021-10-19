#Automated Analysis Decision Rule on Decision Tables
import tkinter as tk
import numpy as np

import util

class DecisionRules(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.create()
    
    def create(self):
        self.instruction = tk.Label(self, 
            text = ' ' * 10 + 
                'Insert Decision Table ' +
                'with: \n' +
                '* actions over the rows and events over the columns' + 
                '\n' +
                '* each row starting a new line' +
                '\n' +
                '* each element in the row separated by at least one space' +
                '\n' +
                '* each element represents the value gain',
            anchor = 'nw', justify = 'left', font = ('Courier', 11)
            )
        self.instruction.grid(row = 0, column = 0)
        self.Text = tk.Text(self, height = 8, width = 50) #text widget for decision table input
        self.Text.grid(row = 0, column = 1, rowspan = 6, columnspan = 4)
        tk.Label(self, text = ' ').grid(row = 0, column = 5)
        self.DecisionRules = tk.Button(self, text = 'Apply Decision Rules',
                                       font = ('Courier', 12, 'bold'), 
                                       command = lambda: self.compute())
        self.DecisionRules.grid(row = 0, column = 6)
        self.ERROR = None
        
    def compute(self):
        if self.ERROR: #if previous ERROR display exists
            self.ERROR.destroy() #remove the ERROR display
        try:
            self.DT = util.Text_to_Matrix(self.Text.get('1.0', 'end'))
        except Exception as e:
            error_message = str(e)
            self.ERROR = tk.Label(self, text = '\nERROR: \n' + error_message, 
                                  font = ('Helvetica', 12, 'bold'), fg = '#b10000')
            self.ERROR.grid(row = 6, column = 2) #ERROR display beneath the text widget
            
        
        

root = tk.Tk()
root.title(string = 'Decision-Rules')
root.geometry('1200x600')
app = DecisionRules(master = root)
app.mainloop()
root.destroy()