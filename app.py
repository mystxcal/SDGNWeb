# Packages
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.plotting import figure
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px
import random
import pandas as pd
from scipy.stats import norm
from faker import Faker
import numpy as np
import plotly.express as px
from datetime import datetime
from datetime import timedelta

#import PyQt5

st.title('🧊Data Tweaking Labs_')
st.text('Synthic Data Generation')
st.file_uploader('Upload Data')

st.radio('Pick one', ['Bias Detection and Mitigation',
                      'New Data', 'More Data'])


st.text('New Data')

# xmin = float(input("Enter lowest x value "))
# xmax = float(input("Enter highest x value "))
# ymin = float(input("Enter lowest y value "))
# ymax = float(input("Enter highest y value "))
xmin = 1
xmax = 5
ymin = 5
ymax = 50


class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print('click', event)
        if event.inaxes != self.line.axes:
            return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()


fig, ax = plt.subplots()
ax.set_title('click to build line segments')
ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
line, = ax.plot([], [])  # empty line
linebuilder = LineBuilder(line)
st.write(fig)

# fig, ax = plt.subplots()
# ax.set_title('click to build line segments')
# ax.set_xlim([xmin, xmax])
# ax.set_ylim([ymin, ymax])
# line, = ax.plot([], [])  # empty line
# linebuilder = LineBuilder(line)

# st.plotly_chart(plt.show(), filename="test")

# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# fake = Faker()
# data_normal = norm.rvs(size=10, loc=0, scale=1)
# cols = []
# calcsteps = []
# nrows = 10
# ncols = 5

# for i in range(ncols):
#     cols.append(list(range(nrows)))
#     calcsteps.append([])


# def poshness(inp1, inp2):
#     if((inp2-(18500+((inp1-2)*5000))) > 0):
#         return 'prime'
#     else:
#         return 'regular'


# def locality(poshness):
#     ls = ['Mumbai', 'Pune', 'Mahableshwar', 'Goa']
#     if (poshness == 'prime'):
#         locality = ls[random.randint(0, 1)]
#     else:
#         locality = ls[random.randint(2, 3)]
#     return locality


# def propage(cpr, price, poshness):
#     mp = max(price)
#     mnp = min(price)
#     pd = (mp+mnp)/2
#     if (poshness == 'prime'):
#         pm = 1.5
#     else:
#         pm = 1
#     return abs((random.randint(1, 5)+(pd/cpr)*pm))


# # print(cols)
# # print(calcsteps)
# # # random.randint(10000,20000)+((cols[i-1][j]-2)*5000)
# # print(len(houseprices))
# calcsteps[0].append('random.randint(1,4)')
# calcsteps[1].append('random.randint(14000,20000)+((cols[i-1][j]-2)*5000)')
# calcsteps[2].append('poshness(cols[i-2][j],cols[i-1][j])')
# calcsteps[3].append('locality(cols[i-1][j])')
# calcsteps[4].append('propage(cols[i-3][j],cols[i-3],cols[i-2][j])')

# for i in range(ncols):
#     for j in range(nrows):
#         for k in range(len(calcsteps[i])):
#             cols[i][j] = eval(calcsteps[i][k])


# x = pd.DataFrame(cols)
# x_n = x.rename(index={0: 'bhk', 1: 'price', 2: 'locality',
#                       3: 'location', 4: 'age in years'})
# x = x_n.transpose()
# st.write(x.head(10))
