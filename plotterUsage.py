from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import LDosPlotter
from matplotlib import pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.tight_layout = True

PATH = "C://Users//baron//Desktop//tests//"
#Examples of use:

## <codecell> Make a minimally customized plot
#v = Vasprun(PATH + "vasprun.xml.AgBiI4")
#dos = LDosPlotter(v)
#dos.AutoCreateGraph(x_lims = [-5, 5], save_path = PATH + "1_.pdf", legend_style=1)
##You can do this in a sinlge line with the following:
##LDosPlotter(Vasprun(PATH+"vasprun.xml.AgBiI4")).AutoCreateGraph(x_lims=[-5, 5], save_path="1.5_.pdf")
#
#
#
## <codecell> DOS smoothing, easy-ish manual legend placements, custom y-label
#v = Vasprun(PATH + "vasprun.xml.AgBiI4")
#dos = LDosPlotter(v)
#dos.AddAllElements(sigma = 0.065)
##Generate Legend: Defaults to atoms in upper right, linestyles in lower right.  All of the 
##normal location keywords should work here
#dos.GenerateLegend(atom_legend_loc="upper center", line_style_loc="upper right")
#
#plt.ylabel(r"$l$-decomposed DOS (states/eV)")
#
#plt.savefig(PATH + "2_.pdf")
#plt.clf()
#
#
#
## <codecell> Non-scaled energy, hide line-style legend, manual zoom-in
#v = Vasprun(PATH + "vasprun.xml.AgBiI4")
#dos = LDosPlotter(v)
#dos.AddAllElements(scale_by_ef = False)
#dos.GenerateLegend(line_styles = False)
#
#plt.xlabel("energy (eV)")
#plt.xlim(3, 7)
#plt.ylim(0, 35)
#
#plt.savefig(PATH + "3_.pdf")
#plt.clf()
#
#
#
## <codecell> Dark theme with custom colors, ignoring s orbital DOS, horizontal atom-only legend
#plt.style.use("dark_background") #(for when you want to use a lot of black ink while printing)
#
#v = Vasprun(PATH + "vasprun.xml")
#dos = LDosPlotter(v)
#
##Changing colors: The two lists are parallel arrays.  The first list is the index and the second is the color.
##It is important to do this step before plotting the atoms, or the color changes will not show up.
##The reason that I start at 1 is because index 0 is designated black, which is used for single-element plots.
##If there is more than one atom (like in this example), the color at index 0 is unused 
#for index, color in zip([1, 2, 3, 4], [(15, 243, 255), (235, 109, 0), (255, 0, 183), (0, 255, 0)]):
#    dos.colors[index] = color
#    
#dos.AddAllElements(sigma = 0.065, hide_s = True)
#
##Legend editing: Making specific edits to the legend outside of simple keyword-based location changes (like in
##an above example) requires getting the legend dictionaries from the class itself and converting them to lists
##since plt.legend() expects the legend handles to be in list form.  
#atomHandlesList = [h for h in dos.atom_legend_handles.values()] 
#plt.legend(handles = atomHandlesList, bbox_to_anchor=(0.0, 1, 1, 0.1),
#           loc='lower left', ncol=len(dos.unique_elements), mode="expand")   
##You could also get the s-p-d legend entries a similar way.  If you want two seperate legends like the plotter's
##default, you have to add the first legend like this:
#'''plt.gca().add_artist(firstplt.legend(handles=atomHandlesList, ...) '''      
##before calling plt.legend() on the s-p-d handles.  
#                    
#plt.xlim(-10, 5)
#plt.savefig(PATH + "4_.pdf")
#plt.clf()
#
#
#
#plt.style.use("default") #setting the background color above was a global change, so need to revert
## <codecell> Ignore Oxygen, change line styles, combinine two legends into one, line at fermi energy
#v = Vasprun(PATH + "vasprun.xml")
#dos = LDosPlotter(v)
#
##Change linestyles: the two arguments are parallel arrays of [orbital], [style].  They don't 
##necessairily have to be in the order s-p-d (because i'm storing the data in dicts, not lists).  
##If you just want to change one style, you don't need to send it as a list.  Like color editing,
##you have to do this before plotting the DOS or the changes won't show up  
#dos.ChangeLineStyle(['s', 'p', 'd'], [':', ':', '-'])
#
##Manually selecting elements:  An example of how you could ignore the DOS of an entire element.
#for elem in dos.unique_elements:
#    if(elem.symbol != 'O'):
#        dos.GetElementDosPlot(elem, sigma = 0.1, scale_by_ef = False)
#
##Legend editing: This first bit is, again, getting the legends into list form.  Same as above.
#atomHandlesList = [h for h in dos.atom_legend_handles.values()] 
#spdHandlesList = [s for s in dos.style_legend_handles.values()] 
##Now we want to have all of the legend entries in a single box on the graph.  So we have to concat
##one array (the s-p-d linestyle array in this case) to the end of the other (atom color) array:
#allHandlesList = [] 
#for sublist in [atomHandlesList, spdHandlesList]:
#    for subsublist in sublist:
#        allHandlesList.append(subsublist)
##I'm going to have a line for the fermi energy, so I'll want a legend entry for that too:
#from matplotlib.lines import Line2D
#fermiHandle = Line2D([0], [0], color='orange', alpha=.5, lw=2, linestyle='-', label=r"$E_\mathrm{F}$")  
#allHandlesList.append(fermiHandle)      
##Now, pass the array of all handles to plt.legend() and specify where to put it        
#plt.legend(handles = allHandlesList, bbox_to_anchor = (0.99, 1), loc = "upper left",
#           frameon = False)         
#
#plt.axvline(x=v.efermi, color='orange', linewidth = 0.85, ymin = 0.1, ymax = 0.9, alpha=.5)                    
#plt.savefig(PATH + "5_.pdf")
#plt.clf()
#
#
#
# <codecell> Make a grid of DOS plots
from matplotlib import gridspec
import os
from glob import glob as glob
from math import ceil

#Get number of rows and columns while adding all of the xml files
nCols = 3
xmlList = []
for path, dirs, files in os.walk(PATH):
    xmlList_ = glob(str(path) + "*.xml*")
    for x in xmlList_:
        xmlList.append(x)
nRows = ceil(len(xmlList) / nCols)
#At this point you may want to add logic to order the xml files.  Here, i'm sorting them by the last
#2 characters in the filename.  If you're deleting files form the list, remember to re-initialize
#the nRows variable (or just set it after the deletions)
xmlList.sort(key = lambda s: s[-3:])   

#Add plots in order
fig = plt.figure(figsize=(8.5, 11), dpi=300) #not setting figsize makes the picture look dumb
gs = gridspec.GridSpec(nRows, nCols, fig, hspace=0.1)
#Add main lables to figure
fig.text(0.05, 0.5, "Electronic DOS (states/eV)", rotation="vertical", ha="center", va="center", 
         fontsize=13)
fig.text(0.5, 0.05, r"$E-E_\mathrm{F}$ (eV)", ha="center", va="center", fontsize=13)   

for row in range(0, nRows):
    for col in range(0, nCols):
        if(row*nCols) + col >= len(xmlList): #avoids error if you don't have enough plots to 
            pass                             #completly fill out the last row
        else:          
            #Create the vasprun object
            ax = fig.add_subplot(gs[row, col])
            v = Vasprun(xmlList[(row*nCols) + col])
            dos = LDosPlotter(v, return_figure = True)

            #Do case-specific editing
            ##Make all plots share the same x-axis scaling, only show the bottom x-axis ticks
            ax.set_xlim(-5, 5)
            if(row != nRows - 1):
                ax.tick_params('x', labelbottom=False)
            ##Make all plots share the same y-axis scaling, only show the left y-axis ticks    
            ax.set_ylim(0, 15)
            if(col != 0):
                ax.tick_params('y', labelleft=False)

            ##Add labels for rows and cols
            if(row == nRows - 1):
                if(col == 0):
                    ax.set_xlabel("Col 0")
                if(col == 1):
                    ax.set_xlabel("Col 1")
                if(col == 2):
                    ax.set_xlabel("Col 2")
            if(col == 0):
                if(row == 0):
                    ax.set_ylabel("Row 0")
                if(row == 1):
                    ax.set_ylabel("Row 1")
                if(row == 2):
                    ax.set_ylabel("Row 2")                                      

            #Add elements to plot (be sure to do this last, since the code returns a 'figure' object
            #and not an 'axis' object.  The two have different functions which can be used by them
            ax = dos.AddAllElements()
                    
plt.savefig(PATH + "test.pdf")
plt.clf()






