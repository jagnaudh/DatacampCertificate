#######################----------STANDARD IMPORTING----------#######################
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import HoverTool, ColumnDataSource as CDS, Select, Slider, NumeralTickFormatter
from bokeh.layouts import Row, Column
import seaborn as sns
from matplotlib import rcParams
from bokeh.resources import CDN
from bokeh.embed import file_html



#######################----------IMPORT DATA----------#######################
data = pd.read_excel('googleplayplay.xlsx')



#######################----------BAR CHART CATEGORY VS INSTALLS BY AGE GROUP----------#######################

#Define a function to update the cat_ins_bar chart
def updateBar (attr, old, new):
    print(old, new)
    cat_ins_bar.xaxis.axis_label = ageBarSelect.value
    dfBarNew = cat_ins[cat_ins['Content Rating'] == ageBarSelect.value].reset_index()
    barSource.data = dict(xVal = dfBarNew['Category'], 
                          yVal = dfBarNew['Installs'])
    cat_ins_bar.x_range.factors = list(dfBarNew['Category'])

#Sum #Installs by Content Rating and Category then add to ColumnDataSource
cat_ins = data.groupby(['Content Rating','Category'])['Installs'].sum().reset_index().sort_values(by=['Installs'], ascending = False)
dfBar = cat_ins[cat_ins['Content Rating'] == 'Everyone'].reset_index()
barSource = CDS(data = dict(xVal = dfBar['Category'],
                            yVal = dfBar['Installs']))
#Create a bar figure
cat_ins_bar = figure (width = 600, height = 650,
                     title = 'Number of Installs per Category',
                     x_axis_label = 'Everyone',
                     y_axis_label = 'No. of Installs',
                     tools = 'pan, box_zoom, reset, lasso_select',
                     x_range = dfBar['Category'])
#Add vbar glyph to the figure cat_ins_bar
cat_ins_bar.vbar(x = 'xVal',
                 top = 'yVal',
                 color='green',
                 width=.8,
                 source = barSource)
#Create tooltips for the cat_ins_bar figure
barHover = HoverTool(tooltips = [('Category','@xVal'),
                              ('#Installs','@yVal{0,000A}')])
cat_ins_bar.add_tools(barHover)
#Format visual styling for the cat_ins_bar figure
#Orient x-axis values
cat_ins_bar.xaxis.major_label_orientation = 45
#Hide gridlines
cat_ins_bar.xgrid.grid_line_color = None
cat_ins_bar.ygrid.grid_line_color = None
#Format y values
cat_ins_bar.yaxis[0].formatter = NumeralTickFormatter(format="0,000")
#Style font, font sizes
cat_ins_bar.xaxis.axis_label_text_font_size = '12pt'
cat_ins_bar.yaxis.axis_label_text_font_size = '12pt'

cat_ins_bar.xaxis.axis_label_text_font = 'Times'
cat_ins_bar.yaxis.axis_label_text_font = 'Times'

cat_ins_bar.xaxis.major_label_text_font_size = '8pt'
cat_ins_bar.yaxis.major_label_text_font_size = '8pt'

cat_ins_bar.xaxis.major_label_text_font = 'Times'
cat_ins_bar.yaxis.major_label_text_font = 'Times'

cat_ins_bar.title.text_font = 'Times'
cat_ins_bar.title.text_font = '13pt'




#Adding a Select Box for the cat_ins_bar figure
ageBarSelect = Select(title = 'Select a target group',
                      options = ['Everyone', 'Adults only 18+', 'Everyone 10+', 'Mature 17+', 'Teen', 'Unrated'],
                      value = 'Everyone')
ageBarSelect.on_change('value', updateBar)





#######################----------SCATTER PLOT INSTALLS BY SIZE & PRICE----------#######################

#Define a function to update the sp_ins_scatter chart
def updateScatter (attr, old, new):
    print(old, new)
    dfScatterNew = data[data[scatterSelect.value] >= scatterSlider.value].reset_index()
    scatterSource.data = dict(xVal = dfScatterNew[scatterSelect.value],
                              yVal = dfScatterNew['Installs'])
    scatterHover.tooltips = [(scatterSelect.value,'@xVal'),('#Installs','@yVal{0,000A}')]
    
def updateSlider(attr, old, new):
    scatterSlider.start = data[scatterSelect.value].min()
    scatterSlider.end = data[scatterSelect.value].max()
    scatterSlider.value = (data[scatterSelect.value].max()-data[scatterSelect.value].min())/2
    
    
    sp_ins_scatter.title.text = scatterSelect.value + " vs Installs"
    sp_ins_scatter.xaxis.axis_label = scatterSelect.value
    
    updateScatter

#Create ColumnDataSource for Size and Install
scatterSource = CDS(data = dict(xVal = data['Size (MB)'],
                                yVal = data['Installs']))
#Create a scatter figure
sp_ins_scatter = figure(width = 550, height = 600, 
                        tools =  'pan, box_zoom, reset, lasso_select',
                        title = 'App Size vs Installs',
                        x_axis_label = 'Size (MB)',
                        y_axis_label = 'No. of Installs')
#Add a circle glyph to the sp_ins_scatter plot
sp_ins_scatter.circle(x = 'xVal',
                      y = 'yVal',
                      size = 4,
                      color = 'green',
                      source = scatterSource)
#Create tooltips for the sp_ins_scatter plot
scatterHover = HoverTool(tooltips = [('Size (MB)','@xVal'),('#Installs','@yVal{0,000A}')])
sp_ins_scatter.add_tools(scatterHover)
#Format visual styling for the sp_ins_scatter plot
#Hide gridlines
sp_ins_scatter.xgrid.grid_line_color = None
sp_ins_scatter.ygrid.grid_line_color = None
#Format x and y values
sp_ins_scatter.xaxis[0].formatter = NumeralTickFormatter(format="0,000")
sp_ins_scatter.yaxis[0].formatter = NumeralTickFormatter(format="0,000")
#Style font, font sizes
sp_ins_scatter.xaxis.axis_label_text_font_size = '12pt'
sp_ins_scatter.yaxis.axis_label_text_font_size = '12pt'

sp_ins_scatter.xaxis.axis_label_text_font = 'Times'
sp_ins_scatter.yaxis.axis_label_text_font = 'Times'

sp_ins_scatter.xaxis.major_label_text_font_size = '8pt'
sp_ins_scatter.yaxis.major_label_text_font_size = '8pt'

sp_ins_scatter.xaxis.major_label_text_font = 'Times'
sp_ins_scatter.yaxis.major_label_text_font = 'Times'

sp_ins_scatter.title.text_font = 'Times'
sp_ins_scatter.title.text_font = '13pt'


#Fixate starting value on x and y axes
sp_ins_scatter.x_range.start = 0
sp_ins_scatter.y_range.start = 0
#Adding a Select Box for the cat_ins_bar figure
scatterSelect = Select(title = 'Select a parameter',
                       options = ['Size (MB)', 'Price ($)'],
                       value = 'Size (MB)')
scatterSelect.on_change('value', updateSlider)

#Adding a Slider for the cat_ins_bar figure
scatterSlider = Slider(title = "Select a Threshold",
                       start = data['Size (MB)'].min(),
                       end = data['Size (MB)'].max(),
                       value = (data['Size (MB)'].max()-data['Size (MB)'].min())/2,
                       step=5)
scatterSlider.on_change('value', updateScatter)




#######################----------HISTOGRAM----------#######################
hist, edges = np.histogram(data['Rating'], bins = 20, range = [0,6])                               
dfHist = pd.DataFrame({'NoApps': hist, 'left': edges[:-1], 'right': edges[1:]})
histSource = CDS(dfHist)

ratingHist = figure(plot_height = 600, plot_width = 600,
                    title = 'Histogram of Rating',
                    x_axis_label = 'Rating', 
                    y_axis_label = 'Number of Apps')

ratingHist.quad(bottom = 0, 
                top = 'NoApps', 
                left = 'left', 
                right = 'right', 
                fill_color='green',
                line_color = 'white',
                source = histSource)

histHover = HoverTool(tooltips = [('Rating ', '@left{0.0}'), ('#Apps', '@NoApps{0,000}')])
ratingHist.add_tools(histHover)

#Visual Styling for Histogram
#Hide gridlines
ratingHist.xgrid.grid_line_color = None
ratingHist.ygrid.grid_line_color = None

#Format x and y values
ratingHist.xaxis[0].formatter = NumeralTickFormatter(format="0,000")
ratingHist.yaxis[0].formatter = NumeralTickFormatter(format="0,000")
#Style font, font sizes
ratingHist.xaxis.axis_label_text_font_size = '12pt'
ratingHist.yaxis.axis_label_text_font_size = '12pt'

ratingHist.xaxis.axis_label_text_font = 'Times'
ratingHist.yaxis.axis_label_text_font = 'Times'

ratingHist.xaxis.major_label_text_font_size = '8pt'
ratingHist.yaxis.major_label_text_font_size = '8pt'

ratingHist.xaxis.major_label_text_font = 'Times'
ratingHist.yaxis.major_label_text_font = 'Times'

ratingHist.title.text_font = 'Times'
ratingHist.title.text_font = '13pt'






#histSlider = Slider(title = 'Select a number of Installs',
#                    start = 0,
#                    end = 1000000000,
#                    value = 0,
#                    step = 100000)

#histSlider.on_change('value', updateHistogram)

#def updateHistogram(attr, old, new):
#    dfNew = data[data['Installs'] >= histSlider.value]
#    histNew, edgesNew = np.histogram(dfNew['Rating'], bins = 20, range = [0,6])   
#    dfHistNew = pd.DataFrame({'NoApps': histNew, 'left': edgesNew[:-1], 'right': edgesNew[1:]})
#    ratingHist.squad.source = CDS(dfHistNew)





#Create a display layout
curdoc().add_root(Column(Row(Column(ageBarSelect, cat_ins_bar),Column(scatterSelect, scatterSlider, sp_ins_scatter)), ratingHist))