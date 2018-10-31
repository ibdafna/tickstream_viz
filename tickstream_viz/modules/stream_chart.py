import zmq
import pandas as pd
import datetime as dt
import numpy as np
import bqplot as bplot
import ipywidgets
import threading
import subprocess
import signal
import os
import datetime
import time
from IPython.display import display
from bqplot import (OrdinalScale, DateScale, LinearScale, Bars, Lines, Axis, Figure)
from ipywidgets import HBox, Layout


class StreamChart():
    def __init__(self):
        self.threads = []
        self.tick_server_process = None
        self.context = None
        self.socket = None
        self.df = pd.DataFrame(data={'AAPL':[], 'SMA1':[], 'SMA2':[]})
        self.x_sc = DateScale()
        self.y_sc = LinearScale()
        self.line = Lines(x=[], y=[], scales={'x': self.x_sc, 'y': self.y_sc},
                          stroke_width=2.5, display_legend=True, 
                          labels=['Asset Price'], colors=['dodgerblue'])
        
        self.sma1 = Lines(x=[], y=[], scales={'x': self.x_sc, 'y': self.y_sc},
                          stroke_width=1.5, display_legend=True, 
                          labels=['SMA1'], colors=['darkorange'])
        
        self.sma2 = Lines(x=[], y=[], scales={'x': self.x_sc, 'y': self.y_sc},
                          stroke_width=1.5, display_legend=True, 
                          labels=['SMA2'], colors=['limegreen'])
        
        self.ax_x = Axis(scale=self.x_sc, grid_lines='solid', label='Time')
        self.ax_y = Axis(scale=self.y_sc, orientation='vertical', tick_format='0.2f', 
                         grid_lines='solid', label='Price')

        self.fig = Figure(marks=[self.line, self.sma1, self.sma2], axes=[self.ax_x, self.ax_y], 
                          title='Streaming Data', legend_location='top-left', 
                          layout=Layout(flex='1 1 auto', width='100%'))

        display(HBox([self.fig]).add_class('theme-dark'))
        
        
    def server_connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect('tcp://0.0.0.0:5555')
        self.socket.setsockopt_string(zmq.SUBSCRIBE, 'AAPL')
        print('Connected to tick server.')
        
    def server_start(self):
        self.tick_server_process = subprocess.Popen(['python', './modules/server.py'], stdout=subprocess.PIPE,
                                                    preexec_fn=os.setsid)
        print('Tick server started.')
        
    def server_stop(self):
        os.killpg(os.getpgid(self.tick_server_process.pid), signal.SIGTERM)
        print('Tick server stopped.')
        
    def update_dataframe(self, num_ops=1000):
        while self.df.shape[0] < num_ops:
            t = np.datetime64(dt.datetime.now())
            asset, val = self.socket.recv_string().split()
            self.df = self.df.append(pd.DataFrame(data={asset:np.float(val)},  index=[t]))
            self.compute_sma()
        
    def update_line(self, num_ops=1000, disp_length=50):
        time.sleep(5)
        while self.df.shape[0] < num_ops:
            self.line.x = self.df.index[-disp_length:]
            self.line.y = self.df.iloc[-disp_length:, 0]
            
            self.sma1.x = self.df.index[-disp_length:]
            self.sma2.x = self.df.index[-disp_length:]
            
            self.sma1.y = self.df.iloc[-disp_length:, 1]
            self.sma2.y = self.df.iloc[-disp_length:, 2]
            
    def compute_sma(self):
        self.df['SMA1'] = self.df[self.df.columns[0]].rolling(5).mean()
        self.df['SMA2'] = self.df[self.df.columns[0]].rolling(10).mean()
        
               
    def run(self):
        self.server_start()
        self.server_connect()
        t1 = threading.Thread(target=self.update_dataframe, args=(1000, ), daemon=True)
        t2 = threading.Thread(target=self.update_line, args=(1000, 50), daemon=True)
        
        self.threads.extend([t1, t2])
        
        for t in self.threads:
            t.start()