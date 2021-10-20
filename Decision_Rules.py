#Automated Analysis of Decision Rules on Decision Tables
import tkinter as tk

import util

class DecisionRules(tk.Frame):
    
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.create()
    
    
    def create(self):
        self.instruction = tk.Label(self, #instructions
            text = '\n' + ' ' * 10 + 
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
        
        self.Text = tk.Text(self, height = 12, width = 50, bg = '#f7f6f3') #text widget for decision table input
        self.Text.grid(row = 0, column = 1, rowspan = 7, columnspan = 4)
        tk.Label(self, text = ' ').grid(row = 7, column = 0, columnspan = 5)
        tk.Label(self, text = ' ').grid(row = 0, column = 5)
        
        self.DecisionRules = tk.Button(self, text = 'Apply Decision Rules',
                                       font = ('Courier', 12, 'bold'), 
                                       command = lambda: self.compute())
        self.DecisionRules.grid(row = 1, column = 0) #main button
        
        tk.Label(self, text = 'Hurwicz optimism index (alpha): ').grid(row = 0, column = 6)
        self.Hurwicz_alpha = tk.Text(self, height = 1, width = 8, bg = '#fffbf3')
        self.Hurwicz_alpha.insert('1.0', '0.5')
        self.Hurwicz_alpha.grid(row = 0, column = 7)
        
        tk.Label(self, text = 'Probability weights: ' + '\n' + 
                           '* separated by at least one space' + '\n' +
                           '* must be same number of elements' + '\n' +
                           '* weights scaled to become probabilities',
                 anchor = 'nw', justify = 'left'
                 ).grid(row = 1, column = 6, columnspan = 2)
        self.prob = tk.Text(self, height = 1, width = 25, bg = '#fffbf3')
        self.prob.grid(row = 2, column = 6, columnspan = 2)        
        
        tk.Label(self, text = ' ').grid(row = 3, column = 6)
        
        self.ERROR = None
        self.TABLE = None
        self.FRAME = None      
    
    
    def compute(self):
        #remove previous results
        if self.ERROR: 
            self.ERROR.destroy()
            self.ERROR = None
        if self.TABLE:
            self.TABLE.destroy()
            self.TABLE = None            
        if self.FRAME:
            self.FRAME.destroy()
            self.FRAME = None
        
        
        try:
            self.DT = util.Text_to_Matrix(self.Text.get('1.0', 'end'))
            self.RT = util.Regret(self.DT)            
            
            self.alpha = float(self.Hurwicz_alpha.get('1.0', 'end').strip()) #optimism index
            if not 0 <= self.alpha <= 1:
                raise Exception('Hurwicz optimism index (alpha) not in [0, 1]')
            
            prob_w = self.prob.get('1.0', 'end').strip().split()
            if prob_w:
                self.prob_w = [float(n) for n in prob_w]
            else:
                self.prob_w = [1 for _ in self.DT[0]] #same as Laplace
            
            #decision rules
            self.dr = []
            self.dr.append(util.maxi_Max(self.DT))
            self.dr.append(util.maxi_Min(self.DT))
            self.dr.append(util.mini_Max(self.RT))
            self.dr.append(util.Laplace(self.DT))
            self.dr.append(util.Hurwicz(self.DT, self.alpha))
            self.dr.append(util.Bayes(self.DT, self.prob_w))
            
            #display tables (Value/Regret)
            self.TABLE = tk.Frame(self)
            self.TABLE.grid(row = 8, column = 0, columnspan = 2, rowspan = 5)
            tk.Label(self.TABLE, text = ' Value Table \n\n' + util.Table_display(self.DT) + '\n'*2, 
                     font = ('Helvetica', 15, 'bold'), fg = '#063158',
                     anchor = 'nw', justify = 'left'
                     ).pack()
            tk.Label(self.TABLE, text = ' Regret Table \n\n' + util.Table_display(self.RT) + '\n'*2,  
                     font = ('Helvetica', 15, 'bold'), fg = '#5a1515',
                     anchor = 'nw', justify = 'left'
                     ).pack()            
            
            #display actions
            self.FRAME = tk.Frame(self, borderwidth = 2, relief = 'ridge')
            self.FRAME.grid(row = 8, column = 3, columnspan = 4, rowspan = 5)
            for actions, rule in zip(self.dr, util.DR):
                tk.Label(self.FRAME, text = ' ' * 10 + rule + ' ' * 10, 
                         font = ('Helvetica', 11, 'bold'), fg = '#144a4d',
                         anchor = 'nw', justify = 'left'
                         ).pack()
                tk.Label(self.FRAME, text = 'action(s):  ' + ' ,  '.join([str(int(n) + 1) for n in actions]
                                                                       ) + '\n',
                         font = ('Helvetica', 11), 
                         anchor = 'nw', justify = 'left'
                         ).pack()
            
        except Exception as e: #display error message
            error_message = str(e)
            self.ERROR = tk.Label(self, text = '\nERROR: \n' + error_message, 
                                  font = ('Helvetica', 12, 'bold'), fg = '#b10000')
            self.ERROR.grid(row = 8, column = 2) #ERROR display beneath the text widget


if __name__ == '__main__':
    root = tk.Tk()
    root.title(string = 'Decision-Rules')
    root.geometry('1200x650')
    app = DecisionRules(master = root)
    app.mainloop()
