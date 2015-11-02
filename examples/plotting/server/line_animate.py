# The plot server must be running
# Go to http://localhost:5006/bokeh to view this plot

import time

import numpy as np

from bokeh.plotting import figure, show, output_server, curdoc
from bokeh.client import push_session
N = 80

x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)

output_server("line_animate")

p = figure()

p.line(x, y, color="#3333ee", name="sin")
p.line([0,4*np.pi], [-1, 1], color="#ee3333")

# Open a session which will keep our local doc in sync with server
session = push_session(curdoc())
# Open the session in a browser
session.show()

renderer = p.select(dict(name="sin"))
ds = renderer[0].data_source

while True:
    for i in np.hstack((np.linspace(1, -1, 100), np.linspace(-1, 1, 100))):
        ds.data["y"] = y * i
        
        # TODO this is a Bokeh bug workaround: Document
        # doesn't notice that we assigned to 'ds.data'
        ds.trigger('data', ds.data, ds.data)
        time.sleep(0.05)
