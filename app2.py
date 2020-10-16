# %%
from GA_opt_func import *
import numpy as np
import matplotlib.pyplot as plt
from bqplot import pyplot as bqplt
from bqplot import LinearScale, Scatter, Axis, Figure, Lines
from IPython.display import display, clear_output
from ipywidgets import widgets

def simple_optimazation_app():
    population_cnt = 20
    itter_time = 50
    crossover_rate = 0.1
    drop_rate = 0.5
    mutation_rate = 0.1

    i = 0
    best_score = 0
    best_ind = []
    best_ind_ready = []
    population = []

    '''
    dynamic figure
    '''
    X = np.linspace(0, 1, 1000)
    y = np.array([target_function(x) for x in X])


    x_sc = LinearScale()
    y_sc = LinearScale()

    ref = Lines(x=X, y=y, scales={'x': x_sc, 'y': y_sc})
    # scatter = Scatter(x=[population], y=np.array([target_function(ind) for ind in population]), 
    #                     scales={'x': x_sc, 'y': y_sc},
    #                     colors=['DarkOrange'], stroke='red', 
    #                     stroke_width=0.4, default_size=20)
    scatter = Scatter(x=[], y=[], 
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
    # display(fig)
    # %%
    run_itter_slider = population_slider = widgets.IntSlider(
                                value=50, description='#Iteration',
                                min=1,max=100,
                                step=1)

    run_btn = widgets.Button(
                description='Run', icon='play',
                disabled=True)


    population_cnt_slider = widgets.IntSlider(
                                value=30, description='#Population',
                                min=0,max=100,
                                step=10)

    init_population_btn = widgets.Button(
                    description='Initialize Population')

    descriptor1 = widgets.Label('crossover_rate')
    crossover_rate_slider = widgets.FloatSlider(
                                value=0.1, description='',
                                min=0,max=1.0,
                                step=0.1)
    descriptor2 = widgets.Label('drop_rate')                            
    drop_rate_slider = widgets.FloatSlider(
                                value=0.5, description='',
                                min=0,max=1.0,
                                step=0.1)
    descriptor3 = widgets.Label('mutation_rate')  
    mutation_rate_slider = widgets.FloatSlider(
                                value=0.3, description='',
                                min=0,max=1.0,
                                step=0.1)
    patch1 = widgets.HBox([descriptor1, crossover_rate_slider])
    patch2 = widgets.HBox([descriptor2, drop_rate_slider])
    patch3 = widgets.HBox([descriptor3, mutation_rate_slider])

    blank = widgets.Label('')

    run_out = widgets.Output(layout={'border': '1px solid black', 'height':'50px'})
    row1 = widgets.VBox([population_cnt_slider, init_population_btn])
    row2 = widgets.HBox([patch1,patch2,patch3])
    row_n = widgets.VBox([run_itter_slider, run_btn])

    app = widgets.VBox([row1, blank,row2, blank, row_n, run_out, fig])

    # %%
    def initialize():
        nonlocal population, i
        population = np.random.rand(population_cnt_slider.value)
        scatter.x = population
        scatter.y = get_scores(scatter.x)
        i = 0
        fig.title = f'迭代{i}次\n'

    @run_out.capture()
    def update(
        itter_time = itter_time,
        crossover_rate = crossover_rate, 
        drop_rate=drop_rate, 
        mutation_rate=mutation_rate):
        nonlocal scatter, fig, best_score, best_ind_ready, best_ind, i
        for j in range(itter_time):
            new_population = select_and_crossover(population, crossover_rate=crossover_rate, drop_rate=drop_rate)
            new_population_ready = encode_all(new_population)

            new_population_ready = mutatie_all(new_population_ready, mutation_rate=mutation_rate)

            new_population = decode_all(new_population_ready)

            ind, score = get_best(new_population)
            if score > best_score:
                best_ind = ind
                best_score = score
                best_ind_ready = encode(best_ind)
            i += 1
        scatter.x = new_population
        scatter.y = get_scores(new_population)
        fig.title = f'迭代{i}次' # + f'最优个体为: {best_ind_ready}; 函数值为:{best_score}'
        clear_output(wait=True)
        display(f'最优个体为: {best_ind_ready}; 函数值为:{best_score}') 
    # %%
    # update()

    # %%
    def on_click_init(change):
        initialize()
        run_btn.disabled = False
    def on_click_run(change):
        update(
        itter_time = run_itter_slider.value,
        crossover_rate = crossover_rate_slider.value, 
        drop_rate=drop_rate_slider.value, 
        mutation_rate=mutation_rate_slider.value)

    init_population_btn.on_click(on_click_init)
    run_btn.on_click(on_click_run)
    return app
# %%
