# %%
from ipyfilechooser import FileChooser
from ipywidgets import widgets
import ipysheet
from ipysheet.numpy_loader import from_array
from IPython.display import display
from GA_usable import read_txt_input
# filechooser
filechooser = FileChooser(path='.\input', use_dir_icons=True, title='请选择输入文件：')
filechooser
# %% OK button
OK_btn =widgets.Button(description='确定', disabled=True)
OK_btn
# %% sheet
sheet = ipysheet.sheet()
sheet
# %% debug_out
debug_out = widgets.Output(layout={'border': '3px solid black'})
debug_out

# %% callbacks
def on_file_choosed(change):
    OK_btn.disabled = False

@debug_out.capture()    # <- 函数修饰器
def on_click_OK(change):
    global sheet
    print('OK clicked')
    display(from_array(read_txt_input(path=filechooser.selected)))

# register callbacks
filechooser.register_callback(on_file_choosed)
OK_btn.on_click(on_click_OK)

# %%
