from matplotlib import pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Bbox
import numpy as np
#https://matplotlib.org/stable/tutorials/advanced/transforms_tutorial.html

def axis_data_transform(parentfig,srcAx,xin,yin,inverse=False):
    xy = parentfig.transFigure.inverted().transform(
                                        srcAx.transData.transform((xin,yin)))
    return xy[0],xy[1]


def addzoomplot(fig, srcAx, desLoc=[], srcLoc=[], conVec=[], color='r', linewidth = 1,
                showconnectors=True, showhighlightbox=True, showTicks = True):

    """
    Adds a zoom axes inside the given figure and axes.

    Call signatures::
    
        
        addzoomplot(fig, srcAx, xmin, xmax, ymin, ymax, bl_x, bl_y, tr_x, tr_y)   # adds a zoom axes inside fig and srcAx
        ax = addzoomplot(fig, srcAx, xmin, xmax, ymin, ymax, bl_x, bl_y, tr_x, tr_y)   # adds a zoom axes inside fig and srcAx
        

    Parameters:
    
    - fig (figure):The figure the zoom axes will be inserted in.
        
    - srcAx (axis): The axis inside fig that the zoom axes will be inserted in

    - srcLoc = [xmin, ymin, xmax, ymax]

    - desLoc = [bl_x, bl_y, tr_x, tr_y]

    - conVec = [parentloc1=3, parentloc2=4, zoomloc1=1, zoomloc2=2]
        
    -- xmin, xmax (values): The minimum and maximum values for the xlimit on the zoom axis
        
    -- ymin, ymax (values): The minimum and maximum values for the ylimit on the zoom axis
        
    -- bl_x, bl_y (values): The bottom left corner of the zoom axis in the data coordinate of the srcAx
                             e.g., if you want the zoom axis to appear with the bottom left corner at x=2.5 and 
                                   y=3 on your parent axis you just set the bl_x = 2.5 and bl_y = 3 and the 
                                   function will automatically convert the coordiantes to srcAx normalized 
                                   values between 0 and 1
                                   
                                   It is important to call tight_layout() before you add any zoomplots using this
                                   function for this coordinate conversion to work properly, otherwise it will not
                                   work as expected.
                                 
    -- tr_x, tr_y (values): The top right corner of the zoom axis in the data coordinate of the srcAx
                             e.g., if you want the zoom axis to appear with top right corner at x=2.5 and y=3 
                                   on your parent axis you just set the bl_x = 2.5 and bl_y = 3 and the 
                                   function will automatically convert the coordiantes to srcAx normalized 
                                   values between 0 and 1
                                   
                                   It is important to call tight_layout() before you add any zoomplots using this
                                   function for this coordinate conversion to work properly, otherwise it will not
                                   work as expected.
                                   
    -- parentloc1, parentloc2 ({1,2,3,4}): The start location of the connections from the box that highlights the
                                            limits of the zoom on the srcAx with xmin, xmax, ymin and ymax values
                                            to the zoom axes added to the plot with the function
                                            1: top left corner
                                            2: top right corner
                                            3: bottom right corner
                                            4: bottom left corner            

    -- zoomloc1, zoomloc2 ({1,2,3,4}): The end location of the connections from the box that highlights the
                                            limits of the zoom on the srcAx with xmin, xmax, ymin and ymax values
                                            to the zoom axes added to the plot with the function
                                            1: top left corner
                                            2: top right corner
                                            3: bottom right corner
                                            4: bottom left corner
                                            
    - color (color value or string): The color for the highliught box and the connection lines
      
    - linewidth (decimal): The linewidth (thickness) for the highlight box and connectors
      
    - showconnectors (bool): The boolean to set whether to show the connector lines or not
      
    - showhighlightbox (bool): The boolean to set wether to show the highlight box or not
                                            
    Returns:

        Added zoom plot axis (Axis)
        
    Notes:
        
    If you call plt.tight_layout() on your plot or figure for the figure 
    you are working with, it is important to call it before you call the 
    addzoomplot function as the dimensions will not be proper otherwise
    """
    # This functions helps add a zoom sub axis to your existing plot
    # It is very useful when you need to add magnieifed portions to your plot
    # to give your viewer a better understanding of what is going on in a 
    # region of the plot that is very crowded

    if(srcLoc==[]):
        prompt = plt.text(0, 1, 'Step 1: Select SOURCE rectangle, 1st bottom-left then top-right corner',
        horizontalalignment='left',
        verticalalignment='top', 
        color='red',
        transform = srcAx.transAxes)
        pts = plt.ginput(2)
        srcLoc = [pts[0][0], pts[0][1], pts[1][0], pts[1][1]]
        prompt.remove()

    xmin = srcLoc[0]
    ymin = srcLoc[1]
    xmax = srcLoc[2]
    ymax = srcLoc[3]

    rect = patches.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin, linewidth=linewidth, edgecolor=color, facecolor='none')
    if (showhighlightbox):
        srcAx.add_patch(rect)
       
    if(desLoc==[]):
        prompt = plt.text(0, 1, 'Step 2: Select DESTINATION rectangle, 1st bottom-left then top-right corner',
        horizontalalignment='left',
        verticalalignment='top', 
        color='blue',
        transform = srcAx.transAxes)
        pts = plt.ginput(2)
        desLoc = [pts[0][0], pts[0][1], pts[1][0], pts[1][1]]
        prompt.remove()
    bl_x = desLoc[0]
    bl_y = desLoc[1]
    tr_x = desLoc[2]
    tr_y = desLoc[3]

    if(conVec==[]):
        srcCenter = [(srcLoc[0]+srcLoc[2])/2, (srcLoc[1]+srcLoc[3])/2]
        desCenter = [(desLoc[0]+desLoc[2])/2, (desLoc[1]+desLoc[3])/2]
        if(srcCenter[0]<desCenter[0]):
            if(desCenter[1]>srcLoc[1] and desCenter[1]<srcLoc[3]):
                conVec = [2, 3, 1, 4]
            elif(desCenter[1]<srcLoc[1]):
                conVec = [3, 4, 2, 1]
            elif(desCenter[1]>srcLoc[1]):
                conVec = [1, 2, 4, 3]
        else:
            if(desCenter[1]>srcLoc[1] and desCenter[1]<srcLoc[3]):
                conVec = [1, 4, 2, 3]
            elif(desCenter[1]<srcLoc[1]):
                conVec = [3, 4, 2, 1]
            elif(desCenter[1]>srcLoc[1]):
                conVec = [1, 2, 4, 3]

    parentloc1 = conVec[0]
    parentloc2 = conVec[1]
    zoomloc1 = conVec[2]
    zoomloc2 = conVec[3]

    
    bb_data = Bbox.from_bounds(bl_x, bl_y, tr_x-bl_x, tr_y-bl_y)
    disp_coords = srcAx.transData.transform(bb_data)
    fig_coords = fig.transFigure.inverted().transform(disp_coords)

    zoomax = fig.add_axes(Bbox(fig_coords))
    
    axblx, axbly = axis_data_transform(fig,srcAx, bl_x, bl_y)
    axtrx, axtry = axis_data_transform(fig,srcAx, tr_x, tr_y)
    for l in srcAx.get_lines():
        zoomax.plot(l.get_data()[0], l.get_data()[1], linestyle = l.get_linestyle(),
                    markevery=l.get_markevery(), color = l.get_color(), 
                    markersize = l.get_markersize(), label = l.get_label(),
                    antialiased = l.get_antialiased())

    bblx, bbly = axis_data_transform(fig,srcAx, xmin, ymin) 
    btrx, btry = axis_data_transform(fig,srcAx, xmax, ymax) 


    if parentloc1==1:
        x1 = bblx
        y1 = btry
    elif parentloc1==2:
        x1 = btrx
        y1 = btry
    elif parentloc1==3:
        x1 = btrx
        y1 = bbly
    else:
        x1 = bblx
        y1 = bbly

    if zoomloc1==1:
        x2 = axblx
        y2 = axtry
    elif zoomloc1==2:
        x2 = axtrx
        y2 = axtry
    elif zoomloc1==3:
        x2 = axtrx
        y2 = axbly
    else:
        x2 = axblx
        y2 = axbly

    if (showconnectors):    
        srcAx.annotate("",
            xy=(x1, y1), xycoords='figure fraction',
            xytext=(x2, y2), textcoords='figure fraction',
            arrowprops=dict(arrowstyle="-",
                            connectionstyle="arc3,rad=0",
                            color=color,
                            linewidth=linewidth))

    if parentloc2==1:
        x1 = bblx
        y1 = btry
    elif parentloc2==2:
        x1 = btrx
        y1 = btry
    elif parentloc2==3:
        x1 = btrx
        y1 = bbly
    else:
        x1 = bblx
        y1 = bbly

    if zoomloc2==1:
        x2 = axblx
        y2 = axtry
    elif zoomloc2==2:
        x2 = axtrx
        y2 = axtry
    elif zoomloc2==3:
        x2 = axtrx
        y2 = axbly
    else:
        x2 = axblx
        y2 = axbly
        
    if (showconnectors):
        srcAx.annotate("",
            xy=(x1, y1), xycoords='figure fraction',
            xytext=(x2, y2), textcoords='figure fraction',
            arrowprops=dict(arrowstyle="-",
                            connectionstyle="arc3,rad=0",
                            color=color,
                            linewidth=linewidth))


    plt.setp(zoomax, xlim=(xmin,xmax),ylim=(ymin,ymax))
    
    print('desLoc=[' + ', '.join(('%.3g' % f) for f in desLoc) + ']' +
          ', srcLoc=[' + ', '.join(('%.3g' % f) for f in srcLoc) + ']' + 
          ', conVec=[' + ', '.join(('%d' % f) for f in conVec) + ']')


    if (showTicks==False):
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False, # labels along the bottom edge are off
            labeltop=False)    # labels along the top edge are off
        plt.tick_params(
            axis='y',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            left=False,        # ticks along the left edge are off
            right=False,       # ticks along the right edge are off
            labelleft=False,   # labels along the left edge are off
            labelright=False)  # labels along the right edge are off

    return zoomax