# %%
import numpy as np
import matplotlib.pyplot as plt
from bqplot import pyplot as bqplt
from bqplot import LinearScale, Scatter, Axis, Figure, Lines
def target_function(x):
    return np.exp(-(x-0.1) ** 2) * np.sin(6 * np.pi * x ** (3 / 4)) ** 2
X = np.linspace(0, 1, 1000)
y = np.array([target_function(x) for x in X])
population = np.random.rand(30)


x_sc = LinearScale()
y_sc = LinearScale()

ref = Lines(x=X, y=y, scales={'x': x_sc, 'y': y_sc})
scatter = Scatter(x=population, y=np.array([target_function(ind) for ind in population]), 
                    scales={'x': x_sc, 'y': y_sc},
                    colors=['DarkOrange'], stroke='red', 
                    stroke_width=0.4, default_size=20)

x_ax = Axis(label='X', scale=x_sc)
y_ax = Axis(label='Y', scale=y_sc, orientation='vertical')

x_ax.min = 0
x_ax.max = 1
x_ax.num_ticks = 7
x_ax.grid_color = 'orangered'

fig = Figure(marks=[ref, scatter], title='A Figure', axes=[x_ax, y_ax],
                animation_duration=1000)
fig
# %%
scatter.x=np.random.rand(30)
scatter.y=np.array([target_function(ind) for ind in scatter.x])

# %%
from ipywidgets import widgets

math_expression = widgets.Label(r'\( f(x) = \exp(-(x-0.1)^2)\times\sin^2(6\pi x^{3/4}) \)')
# %%
