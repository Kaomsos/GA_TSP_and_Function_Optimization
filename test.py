# %%
import numpy as np
import matplotlib.pyplot as plt

def target_function(x):
    return np.exp(-(x-0.1) ** 2) * np.sin(6 * np.pi * x ** (3 / 4)) ** 2

# %%
X = np.linspace(-0.1, 1.1, 1000)
y = np.array([target_function(x) for x in X])

plt.plot(X, y)
plt.show()

# %%
from IPython.display import display
from ipywidgets import widgets
import ipysheet

sheet = ipysheet.sheet(
    rows=3, columns=4, # define ncol and nrow of a sheet
    column_headers=False, row_headers=False # define headers
)
sheet
# %%
# change value and return a cell obj
# cell(row, column, value=0.0, ... )
cell_a = ipysheet.cell(0, 1, 1, label_left='a')
cell_b = ipysheet.cell(1, 1, 2, label_left='b')
cell_sum = ipysheet.cell(2, 1, 3, label_left='sum', read_only=True)
# %%
# create a slider linked to cell a
slider = widgets.FloatSlider(min=-10, max=10, description='a')
widgets.jslink((cell_a, 'value'), (slider, 'value')) # jslink(attr1, attr2) -> Link; type(attr1)=tuple:(<widegt, name>)
# %%
# changes in a or b should trigger this function
def calculate(change):
    cell_sum.value = cell_a.value + cell_b.value

cell_a.observe(calculate, 'value')
cell_b.observe(calculate, 'value')


widgets.VBox([sheet, slider])
# %%
'''
ipysheet.pandas_loader.from_dataframe(dataframe)
Helper function for creating a sheet out of a Pandas DataFrame

Parameters:	dataframe (Pandas DataFrame) –
Returns:	Sheet widget
############
ipysheet.pandas_loader.to_dataframe(sheet)
Reverse of from_dataframe(dataframe)
############
ipysheet.numpy_loader.from_array(array)
ipysheet.numpy_loader.to_array(sheet)
'''
cell_a.keys


# %%
from ipyfilechooser import FileChooser
filechooser = FileChooser(path='.\input', use_dir_icons=True, title='请选择输入文件：')
filechooser
# %%
from ipywidgets import widgets

OK_btn =widgets.Button(description='确定', disabled=True)
OK_btn
# %%
debug_out = widgets.Output(layout={'border': '3px solid black'})
debug_out
# %%
# callbacks
def on_file_choosed(change):
    OK_btn.disabled = False

@debug_out.capture()    # <- 函数修饰器
def on_click_OK(change):
    print('OK clicked')

filechooser.register_callback(on_file_choosed)
OK_btn.on_click(on_click_OK)
# %%
