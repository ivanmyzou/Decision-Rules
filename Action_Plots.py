#Decision Action Plotting
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

import numpy as np

from scipy.spatial import ConvexHull

import plotly.graph_objects as go
import plotly.io as pio

import util

pio.renderers.default='browser'


class ActionPlots(tk.Frame):
    
    def __init__(self, master = None):
        ttk.Frame.__init__(self, master)
        self.pack()
        self.create()
    
    
    def create(self):
        self.instruction = ttk.Label(self, #instructions
            text = '\n' + ' ' * 10 + 
                'Insert Decision Table ' +
                'with: \n' +
                '* actions over the rows and events over the columns' + 
                '\n' +
                '* each row starting a new line' +
                '\n' +
                '* two elements in each row separated by at least one space' +
                '\n' +
                '* each element represents the value gain' + 
                '\n',
            anchor = 'nw', justify = 'left', font = ('Courier New', 12)
            )
        self.instruction.grid(row = 0, column = 0)
        
        self.Text = tk.Text(self, height = 12, width = 60, bg = '#f8f9f3') #text widget for decision table input
        self.Text.grid(row = 1, column = 0)
        ttk.Label(self, text = ' ').grid(row = 2, column = 0)

        self.ActionPlots = ttk.Button(self, text = 'Plot Action Mixture',
                                      command = lambda: self.compute()) #themed button
        self.ActionPlots.grid(row = 3, column = 0) #main button
        
        self.ERROR = None
    
    
    def compute(self):
        #remove previous results
        if self.ERROR: 
            self.ERROR.destroy()
            self.ERROR = None
        
        
        try:
            self.DT = util.Text_to_Matrix(self.Text.get('1.0', 'end'))
            self.RT = util.Regret(self.DT)
            
            if self.DT.shape[1] != 2:
                raise Exception('number of columns must be 2')
            
            #plotly
            maxcoor, mincoor = max(self.DT.max(), self.RT.max()), min(self.DT.min(), self.RT.min())
            pts = np.arange(maxcoor + 1) if mincoor >= 0 else np.arange(mincoor, maxcoor + 1)
            fig = go.Figure(go.Scatter(x = pts, y = pts, mode = 'lines',
                                       name = 'y = x', marker = {'color':'#576675'})) #y = x line
            
            try: #convex hull of values
                Convex_Hull = ConvexHull(points = self.DT)
                vertices_index = Convex_Hull.vertices #anti-clockwise
                DT_vertices = self.DT.take(vertices_index,axis=0)
                fig.add_trace(go.Scatter(x = np.append(DT_vertices[:,0], DT_vertices[0,0]), #looping back so the shape has all edges
                                         y = np.append(DT_vertices[:,1], DT_vertices[0,1]), #looping back so the shape has all edges
                                         fill = "toself",
                                         name = 'action value mixture', marker = {'color':'#7388A0'}))
            except: #convex hull not possible
                fig.add_trace(go.Scatter(x = self.DT[:,0], y = self.DT[:,1], mode = 'lines',
                                         name = 'action value mixture', marker = {'color':'#7388A0'}))
            
            try: #convex hull of regrets
                Convex_Hull = ConvexHull(points = self.RT)
                vertices_index = Convex_Hull.vertices #anti-clockwise
                RT_vertices = self.RT.take(vertices_index,axis=0)
                fig.add_trace(go.Scatter(x = np.append(RT_vertices[:,0], RT_vertices[0,0]), #looping back so the shape has all edges
                                         y = np.append(RT_vertices[:,1], RT_vertices[0,1]), #looping back so the shape has all edges
                                         fill = "toself",
                                         name = 'action regret mixture', marker = {'color':'#D9A2A3'}))
            except: #convex hull not possible
                fig.add_trace(go.Scatter(x = self.RT[:,0], y = self.RT[:,1], mode = 'lines',
                                         name = 'action regret mixture', marker = {'color':'#D9A2A3'}))
                
            
            #points scatter plot
            actions = ['action ' + str(n) for n in range(1, self.DT.shape[0]+1)]
            fig.add_trace(go.Scatter(x = self.DT[:,0], y = self.DT[:,1], text = actions,
                                     mode = 'markers', name = 'values', marker = {'color':'#375678'}))
            fig.add_trace(go.Scatter(x = self.RT[:,0], y = self.RT[:,1], text = actions,
                                     mode = 'markers', name = 'regrets', marker = {'color':'#903838'}))
            try:
                #intersects
                intersects = np.array([util.diag_intersect(DT_vertices)[-1], util.diag_intersect(RT_vertices)[0]])
                #values
                fig.add_trace(go.Scatter(x = [intersects[0,0]], y = [intersects[0,1]], 
                                         mode = 'markers', name = 'maximin value', marker = {'color':'#7495A0', 'size':10}))
                #regrets
                fig.add_trace(go.Scatter(x = [intersects[1,0]], y = [intersects[1,1]], 
                                         mode = 'markers', name = 'minimax regret', marker = {'color':'#D0A9A3', 'size':10}))
            except:
                pass
            fig.show()
            
        except Exception as e: #display error message
            error_message = str(e)
            self.ERROR = tk.Label(self, text = '\nERROR: \n' + error_message, 
                                  font = ('Helvetica', 12, 'bold'), fg = '#b10000')
            self.ERROR.grid(row = 4, column = 0) #ERROR display beneath the text widget


if __name__ == '__main__':
    root = ThemedTk(theme="breeze")
    root.title(string = 'Action-Plots')
    root.geometry('600x500')
    app = ActionPlots(master = root)
    try:
        root.iconbitmap('icon\yunyun.ico')
    except:
        pass
    app.mainloop()
