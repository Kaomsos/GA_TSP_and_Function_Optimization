# %%
from ipyfilechooser import FileChooser
from ipywidgets import widgets
import ipysheet
from ipysheet.numpy_loader import from_array, to_array
from IPython.display import display
from GA_usable import read_txt_input, TSP_run
from time import sleep, time

def TSP_app():
# some global/enclosing variables
    city_count = 0 
    # %%
    # filechooser
    filechooser = FileChooser(path='.\input', use_dir_icons=True, title='请选择输入文件：')

    # %% OK button
    OK_btn = widgets.Button(description='确定', disabled=True)

    # %% sheet
    sheet = ipysheet.sheet()

    # %% run button
    run_btn = widgets.Button(description="运行", disabled=True) 

    # %%
    text_input_page = widgets.Label('邻接矩阵将显示于下表')

    # %%
    input_page = widgets.VBox([filechooser, OK_btn, text_input_page, sheet])

    # %%
    city_count_text = widgets.BoundedIntText(
                            value=0, description='#city', disabled=True,
                            min=0,max=100,
                            step=1)
    population_slider = widgets.IntSlider(
                            value=50, description='#population',
                            min=0,max=100,
                            step=10)
    improve_count_slider = widgets.IntSlider(
                            value=0, description='#improve',
                            min=0,max=10000,
                            step=100)
    retain_rate_slider = widgets.FloatSlider(
                            value=0.3, description='retain_rate',
                            min=0,max=1.0,
                            step=0.1)
    itter_time_slider = widgets.IntSlider(
                            value= 100, description='#iter',
                            min=0,max=500,
                            step=50)
    select_rate_slider = widgets.FloatSlider(
                            value= 0.5, description='select_rate',
                            min=0,max=1,
                            step=0.01)
    mutation_rate_slider = widgets.FloatSlider(
                            value= 0.1, description='mutate_rate',
                            min=0,max=1,
                            step=0.01)
    paramter_row_1 = widgets.HBox([population_slider, itter_time_slider, improve_count_slider])
    paramter_row_2 = widgets.HBox([retain_rate_slider, select_rate_slider, mutation_rate_slider])
    # %%
    run_out = widgets.Output(layout={'border': '2px solid black'})
    run_out.layout.height = '500px'
    # %%
    run_page = widgets.VBox([city_count_text, paramter_row_1, paramter_row_2, run_btn, run_out])

    # %%
    app = widgets.Tab(children=[input_page, run_page], titles=('Input', 'Run'))
    app.set_title(0, '输入')
    app.set_title(1, '运行')
    
    # %% debug_out
    # debug_out = widgets.Output(layout={'border': '3px solid black'})
    # debug_out


    # %% callbacks
    def on_file_choosed(change):
        OK_btn.disabled = False

    # @debug_out.capture()    # <- 函数修饰器
    def on_click_OK(change):
        print('OK clicked')
        nonlocal city_count, sheet
        city_count, distance = read_txt_input(path=filechooser.selected)
        run_btn.disabled = False
        sheet = from_array(distance)
        text_input_page.value = '查看并编辑邻接矩阵'
        input_page.children = [filechooser, OK_btn, text_input_page, sheet]
        city_count_text.disabled=False
        city_count_text.value = city_count
        city_count_text.disabled=True
        sleep(3)
        app.selected_index=1

    @run_out.capture()    # <- 函数修饰器
    def on_clik_run(change):
        print('run clicked')
        nonlocal city_count
        TSP_run(city_count=city_count, count=population_slider.value,
                improve_count=improve_count_slider.value,
                itter_time=itter_time_slider.value,
                retain_rate=retain_rate_slider.value,
                random_select_rate=select_rate_slider.value,
                mutation_rate=mutation_rate_slider.value)
        

    # register callbacks
    filechooser.register_callback(on_file_choosed)
    OK_btn.on_click(on_click_OK)
    run_btn.on_click(on_clik_run)


    display(app)
# %%
# %%
# %%