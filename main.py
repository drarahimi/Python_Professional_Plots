from pandas import read_csv
from matplotlib import pyplot as plt
import numpy as np
import os

series = read_csv(os.path.dirname(os.path.realpath(__file__)) + '/rwspeed.csv')

# x axis values 
x= np.arange(len(series)) / 10
m_interval = 5
m_size = 5
# corresponding y axis values 
y= series.values
y = y[:,1] 
 
# close all open figures
plt.close('all')

# the following 2 lines of code set the font size and name 
# for all elements in the plot and the math font fot latex scripts
plt.rcParams["font.family"] = "Times New Roman" #font name
plt.rcParams["font.size"] = "18" # font size
plt.rcParams['mathtext.fontset'] = 'stix' # for math fonts
plt.rcParams["figure.facecolor"]= 'white'
plt.rcParams["axes.facecolor"]= 'white'
plt.rcParams["savefig.facecolor"]= 'white'
plt.rcParams["figure.figsize"] = (12,7) # figure size
plt.style.use('grayscale') # if you want everything to be grayscale
 
# plotting the points  
fig, ax1 = plt.subplots()

ax1.plot(x, y,'k-',antialiased=True)

#plot style and grid
ax1.grid(color="0.5", linestyle=':', linewidth=1,antialiased=True)

# naming the x axis 
ax1.set_xlabel('Time [second]')
# naming the y axis 
ax1.set_ylabel('RW Speed ($\omega$)\ [radian/second]') #note the $ sign for latex scripting using stinx font in line 21

# only use one of the following 2 options to add a zoom axes
# you can change the value of the variable option to 1 or 2
# if you use it in your code, make sure to make the necessary changes based on
# the option you choose to use in your code

option = 4

if (option == 1):
    ## zoom plot - option 1 - manual addition
    # location [left top width height] in scale of axis from 0 to 1
    ax2 = plt.axes([.47, .18, .45, .35]) 
    ax2.plot(x, y,'k-',antialiased=True)
    # range of x and y axis in the zoom plot, note that this is try/error 
    # approach to find the right values for your use case
    plt.setp(ax2, xlim=(20,40),ylim=(-0.05,0.06)) 
elif (option == 2):
    ## zoom plot - option 2 - using a library
    # add necessary libraries
    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
    from mpl_toolkits.axes_grid1.inset_locator import mark_inset
    # add the zoom axis
    axins = zoomed_inset_axes(ax1, zoom=3, loc=4,borderpad=2)
    # plot all you need again in the zoom axis
    axins.plot(x, y,'k-',antialiased=True)
    # set the x and y limits for the zoom axis
    axins.set_xlim(23, 33) # Limit the region for zoom
    axins.set_ylim(0.025, 0.06)
    # if you want to remove the axes tick values uncomment the following 2 lines
    #plt.xticks(visible=False)
    #plt.yticks(visible=False)
    # draw a box around the region of the inset axes in the parent axes and
    # connecting lines between the bbox and the inset axes area
    mark_inset(ax1, axins, loc1=1, loc2=2, fc="none", ec="0.1")
elif (option == 3):
    ## zoom plot - option 3 - using Dr. Rahimi's library with hard-code inputs
    # add necessary libraries
    # Note that to properly import the library, the file zoomplot.py must
    # be located in the same directory as the script (.py) file you are 
    # calling the import from, for other projects, just copy and paste the
    # zoomplot.py file from the directory of this package to your project
    import zoomplot
    # Note that for this library to work properly, you have to call 
    # tight_layout() on your plot before calling teh addzoomplot function
    # calling the tight layout to make sure addzoomplot works properly
    plt.tight_layout(pad=0.6, w_pad=0.3, h_pad=0.5)
    # adding a zoom plot with Dr. Rahimi's library
    ax2 = zoomplot.addzoomplot(fig=fig, srcAx=ax1,
                      srcLoc=[23,0.025,33,0.06], 
                      desLoc=[22, -0.15, 60,-0.05],
                      conVec=[3,4,2,1],
                      color='r',
                      linewidth=1.5,
                      showconnectors=True,
                      showhighlightbox=True)
    # you can further modify the axis of the added zoom plot (axis)
    # for example, in the line below we add customized grids to it
    ax2.grid(color="0.5", linestyle=':', linewidth=1,antialiased=True)
elif (option == 4):
    ## zoom plot - option 4 - using Dr. Rahimi's library with interactive inputs
    # add necessary libraries
    # Note that to properly import the library, the file zoomplot.py must
    # be located in the same directory as the script (.py) file you are 
    # calling the import from, for other projects, just copy and paste the
    # zoomplot.py file from the directory of this package to your project
    import zoomplot
    # Note that for this library to work properly, you have to call 
    # tight_layout() on your plot before calling teh addzoomplot function
    # calling the tight layout to make sure addzoomplot works properly
    plt.tight_layout(pad=0.6, w_pad=0.3, h_pad=0.5)
    # adding a zoom plot with Dr. Rahimi's library
    ax2 = zoomplot.addzoomplot(fig=fig, srcAx=ax1,
                      srcLoc = [],
                      desLoc=[],
                      conVec = [],
                      color='r',
                      linewidth=1.5,
                      showconnectors=True,
                      showhighlightbox=True,
                      showTicks=False)
    # you can further modify the axis of the added zoom plot (axis)
    # for example, in the line below we add customized grids to it
    ax2.grid(color="0.5", linestyle=':', linewidth=1,antialiased=True)

# give a title to plot 
#plt.title('Graph of Time Vs. RW Speed') 

# setting legends
#ax1.legend(loc='best')

# set plot layout options
plt.tight_layout(pad=0.6, w_pad=0.3, h_pad=0.5)

# Save the plot on hard drive
plt.savefig(os.path.dirname(os.path.realpath(__file__)) + '/Plot.svg', format='svg', dpi = 300)
  
# show the plot 
plt.show() 


