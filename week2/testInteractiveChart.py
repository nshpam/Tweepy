# Interactive Donut pie chart using matplotlib-----------------------
# import matplotlib.pyplot as plt
# from matplotlib.widgets import CheckButtons

# labels = ['Frogs', 'Hogs', 'Dogs', 'Logs']
# values = [15, 30, 45, 10]

# fig, ax = plt.subplots()
# ax.pie(values, labels=labels, autopct='%1.1f%%', radius=1,
#        wedgeprops=dict(width=0.3, edgecolor='w'))
# ax.set(aspect="equal", title='Donut Chart')

# # Add check buttons for toggling wedges
# rax = plt.axes([0.05, 0.4, 0.1, 0.15])
# check = CheckButtons(rax, labels)

# def func(label):
#     index = labels.index(label)
#     wedges = ax.patches
#     wedges[index].set_visible(not wedges[index].get_visible())
#     fig.canvas.draw_idle()

# check.on_clicked(func)
# plt.show()

# Interactive Stacked bar chart using matplotlib-----------------------
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.widgets import CheckButtons

# data = np.array([[5., 30., 45., 22.],
#   [5., 25., 50., 20.],
#   [1.,  2.,  1.,  1.]])

# color_list = ['b', 'g', 'r']

# X = np.arange(data.shape[1])
# fig, ax = plt.subplots()
# bar1 = ax.barh(X, data[0], color = color_list[0 % len(color_list)])
# bar2 = ax.barh(X, data[1], left=data[0], color = color_list[1 % len(color_list)])
# bar3 = ax.barh(X, data[2], left=np.sum(data[:2], axis = 0), color = color_list[2 % len(color_list)])

# # Add check buttons for toggling bars
# rax = plt.axes([0.05, 0.8, 0.1, 0.1])
# check = CheckButtons(rax, ['Bar1', 'Bar2', 'Bar3'])

# def func(label):
#     if label == 'Bar1':
#         for bar in bar1:
#             bar.set_visible(not bar.get_visible())
#     elif label == 'Bar2':
#         for bar in bar2:
#             bar.set_visible(not bar.get_visible())
#     elif label == 'Bar3':
#         for bar in bar3:
#             bar.set_visible(not bar.get_visible())
#     fig.canvas.draw_idle()

# check.on_clicked(func)
# plt.show()

# Interactive Horizon bar chart using matplotlib-----------------------
# import numpy as np
# import matplotlib.pyplot as plt

# # Fixing random state for reproducibility
# np.random.seed(19680801)

# # make up data in the open interval 0, 1
# a = np.random.rand(5)

# # set position of bar on X axis
# r = [0,1,2,3,4]

# # plotting
# barWidth = 0.5
# fig, ax = plt.subplots()
# bar1 = ax.barh(r, a, height = barWidth, color='#7f6d5f', edgecolor='white')

# annot = ax.annotate("", xy=(0,0), xytext=(20,20),
#             textcoords="offset points",
#             bbox=dict(boxstyle="round", fc="w"),
#             arrowprops=dict(arrowstyle="->"))
# annot.set_visible(False)

# def update_annot(bar):
#     x = bar.get_x() + bar.get_width()/2.
#     y = bar.get_y() + bar.get_height()/2.
#     annot.xy = (x,y)
#     text = "Value: {}".format(bar.get_height())
#     annot.set_text(text)

# def hover(event):
#     vis = annot.get_visible()
#     if event.inaxes == ax:
#         for bar in bar1:
#             contains, attrd = bar.contains(event)
#             if contains:
#                 update_annot(bar)
#                 annot.set_visible(True)
#                 fig.canvas.draw_idle()
#                 return
#     if vis:
#         annot.set_visible(False)
#         fig.canvas.draw_idle()

# fig.canvas.mpl_connect("motion_notify_event", hover)

# plt.show()

# Interactive Donut pie chart using Bokeh-----------------------
# from math import pi

# from bokeh.io import show
# from bokeh.models import (AnnularWedge, ColumnDataSource,
#                           Legend, LegendItem, Plot, Range1d)
# from bokeh.sampledata.browsers import browsers_nov_2013 as df

# xdr = Range1d(start=-2, end=2)
# ydr = Range1d(start=-2, end=2)

# plot = Plot(x_range=xdr, y_range=ydr)
# plot.title.text = "Web browser market share (November 2013)"
# plot.toolbar_location = None

# colors = {
#     "Chrome": "seagreen",
#     "Firefox": "tomato",
#     "Safari": "orchid",
#     "Opera": "firebrick",
#     "IE": "skyblue",
#     "Other": "lightgray"
# }

# aggregated = df.groupby("Browser").sum(numeric_only=True)
# selected = aggregated[aggregated.Share >= 1].copy()
# selected.loc["Other"] = aggregated[aggregated.Share < 1].sum()
# browsers = selected.index.tolist()

# angles = selected.Share.map(lambda x: 2*pi*(x/100)).cumsum().tolist()

# browsers_source = ColumnDataSource(dict(
#     start  = [0] + angles[:-1],
#     end    = angles,
#     colors = [colors[browser] for browser in browsers],
# ))

# glyph = AnnularWedge(x=0, y=0, inner_radius=0.9, outer_radius=1.8,
#                      start_angle="start", end_angle="end",
#                      line_color="white", line_width=3, fill_color="colors")
# r= plot.add_glyph(browsers_source, glyph)

# legend = Legend(location="center")
# for i, name in enumerate(colors):
#     legend.items.append(LegendItem(label=name, renderers=[r], index=i))
# plot.add_layout(legend, "center")

# from bokeh.models import HoverTool

# # Add hover tool
# hover = HoverTool()
# hover.tooltips = [("Browser", "@labels"), ("Share", "@share %")]
# plot.add_tools(hover)

# # Show the plot
# show(plot)


# Interactive Stacked bar chart using Bokeh-----------------------
# from bokeh.io import output_file, show
# from bokeh.models import ColumnDataSource
# from bokeh.palettes import GnBu3, OrRd3
# from bokeh.plotting import figure

# output_file("stacked_split.html")

# fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
# years = ["2015", "2016", "2017"]

# exports = {'fruits' : fruits,
#            '2015'   : [2, 1, 4, 3, 2, 4],
#            '2016'   : [5, 3, 4, 2, 4, 6],
#            '2017'   : [3, 2, 4, 4, 5, 3]}
# imports = {'fruits' : fruits,
#            '2015'   : [-1, 0, -1, -3, -2, -1],
#            '2016'   : [-2, -1, -3, -1, -2, -2],
#            '2017'   : [-1, -2, -1, 0, -2, -2]}

# p = figure(y_range=fruits, height=250, x_range=(-16, 16), title="Fruit import/export, by year",
#            toolbar_location=None)

# p.hbar_stack(years, y='fruits', height=0.9, color=GnBu3, source=ColumnDataSource(exports),
#              legend_label=["%s exports" % x for x in years])

# p.hbar_stack(years, y='fruits', height=0.9, color=OrRd3, source=ColumnDataSource(imports),
#              legend_label=["%s imports" % x for x in years])

# p.y_range.range_padding = 0.1
# p.ygrid.grid_line_color = None
# p.legend.location = "top_left"
# p.axis.minor_tick_line_color = None
# p.outline_line_color = None

# show(p)

# Interactive Horizon bar chart using Bokeh-----------------------
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

output_file("colormapped_bars.html")

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
counts = [5, 3, 4, 2, 4, 6]

source = ColumnDataSource(data=dict(fruits=fruits, counts=counts))

p = figure(y_range=fruits, height=250, toolbar_location=None, title="Fruit counts")
p.hbar(y='fruits', right='counts', height=0.9, source=source, legend_field="fruits",
       line_color='white', fill_color=factor_cmap('fruits', palette=Spectral6, factors=fruits))

# Create a HoverTool object
hover = HoverTool(tooltips=[("Fruits", "@fruits"),("Counts", "@counts")])
hover.tooltips = """
    <style>
        .bk-tooltip>div:not(:first-child) {display:none;}
    </style>
    <div>
        <div>
            <span style="font-size: 17px; font-weight: bold;">@fruits</span>
        </div>
        <div>
            <span style="font-size: 15px;">Counts: @counts</span>
        </div>
    </div>
"""

# Add the HoverTool object to the plot's list of tools
p.add_tools(hover)

p.ygrid.grid_line_color = None

p.x_range.start = 0
p.x_range.end = 9
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)

# Interactive Donut pie bar chart using Plotly-----------------------
# import plotly.graph_objects as go

# labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
# values = [4500, 2500, 1053, 500]

# fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, hoverinfo='label+percent')])
# fig.update_layout(
#     updatemenus=[dict(
#         type='buttons',
#         showactive=False,
#         buttons=[dict(
#             label='Show Values',
#             method='update',
#             args=[{'visible': [True, True, True, True]},
#                   {'title': 'Gas Composition'}]),
#                  dict(
#             label='Hide Values',
#             method='update',
#             args=[{'visible': [False, False, False, False]},
#                   {'title': 'Gas Composition'}])
#         ]
#     )]
# )
# fig.show()

# Interactive Stacked bar chart using Plotly-----------------------
# import plotly.express as px
# df = px.data.medals_long()

# fig = px.bar(df, y="medal", x="count", color="nation", text_auto=True)
# fig.show()




# Interactive Horizon bar chart using Plotly-----------------------
# import plotly.graph_objects as go

# fig = go.Figure(go.Bar(
#             x=[20, 14, 23],
#             y=['giraffes', 'orangutans', 'monkeys'],
#             orientation='h'))

# fig.show()

# Interactive Donut pie chart using Altair-----------------------
# import pandas as pd
# import altair as alt

# source = pd.DataFrame({"category": [1, 2, 3, 4, 5, 6], "value": [4, 6, 10, 3, 7, 8]})

# chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
# theta=alt.Theta(field="value", type="quantitative"),
# color=alt.Color(field="category", type="nominal"),
# )
# # Add a selection interaction
# selector = alt.selection_single(empty='all', on='mouseover')

# chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
#     theta=alt.Theta(field="value", type="quantitative"),
#     color=alt.Color(field="category", type="nominal"),
#     opacity=alt.condition(selector, alt.value(1), alt.value(0.5))
# )

# chart = chart.add_selection(selector)

# chart.show()



# Interactive Stacked bar chart using Altair-----------------------
# import altair as alt
# from vega_datasets import data

# source = data.barley()

# chart = alt.Chart(source).mark_bar().encode(
#     y='variety',
#     x='sum(yield)',
#     color='site'
# )

# hover = alt.selection(type='single', on='mouseover', nearest=True,
#                      fields=['variety'], empty='none')

# chart = chart.add_selection(hover)

# chart = chart.encode(
#     alt.Color('site:N', legend=alt.Legend(title='Site')),
#     alt.X('sum(yield):Q', axis=alt.Axis(title='Yield')),
#     alt.Y('variety:N', axis=alt.Axis(title='Variety')),
#     alt.Tooltip(['variety', 'site', 'sum(yield)'])
# )

# chart.show()





# Interactive Horizon chart using Altair-----------------------
# import altair as alt
# import pandas as pd

# source = pd.DataFrame({'Activity': ['Sleeping', 'Eating', 'TV', 'Work', 'Exercise'],
#                       'Time': [8, 2, 4, 8, 2]})

# chart = alt.Chart(source).transform_joinaggregate(
#     TotalTime='sum(Time)',
# ).transform_calculate(
#     PercentOfTotal="datum.Time / datum.TotalTime"
# ).mark_bar().encode(
#     alt.X('PercentOfTotal:Q', axis=alt.Axis(format='.0%')),
#     y='Activity:N',
#     tooltip=['Activity', 'Time']
# )

# # Add hover interactivity
# chart = chart.interactive()

# # Add selection interactivity
# selector = alt.selection_single(
#     fields=['Activity'],
#     empty='all',
#     bind='legend'
# )

# chart = chart.add_selection(selector)

# # Add tooltips
# chart = chart.properties(
#     width=300,
#     height=200
# )

# chart.show()


# Interactive Donut pie bar chart using Pygal-----------------------
# # importing pygal
# import pygal
# # creating pie_chart object
# pie_chart = pygal.Pie(inner_radius=.4)
# pie_chart.title = 'random data'
# # adding random data
# pie_chart.add('A', 20.5)
# pie_chart.add('B', 36.0)
# pie_chart.add('C', 35.9)
# pie_chart.add('D', 5.5)
# pie_chart.add('E', 80.3)
# # rendering the svg to file
# pie_chart.render_in_browser()


# Interactive Stacked bar chart using Pygal-----------------------
# import pygal

# chart = pygal.StackedBar()
# chart.title = 'Stacked Bar Chart Example'
# chart.x_labels = ['Year1', 'Year2', 'Year3']
# chart.add('Fruits', [20, 30, 40])
# chart.add('Vegetables', [15, 25, 35])
# chart.render_in_browser()

# Interactive horizon bar chart using Pygal-----------------------
# import pygal

# chart = pygal.HorizontalBar() #change from pygal.StackedBar()
# chart.title = 'Horizontal Bar Chart Example' # you can change the title
# chart.x_labels = ['Year1', 'Year2', 'Year3']
# chart.add('Fruits', [20, 30, 40])
# chart.add('Vegetables', [15, 25, 35])
# chart.render_in_browser()

