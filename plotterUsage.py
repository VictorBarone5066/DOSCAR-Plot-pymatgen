from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import LDosPlotter
from matplotlib import pyplot as plt


PATH = "C://Users//baron//Desktop//"
#Examples of use:

# <codecell> Make a minimally customized plot
v = Vasprun(PATH + "vasprun.xml.AgBiI4")
dos = LDosPlotter(v)
dos.AutoCreateGraph(x_lims = [-5, 5], save_path = PATH + "1_.pdf")
#You can do this in a sinlge line with the following:
#LDosPlotter(Vasprun(PATH+"vasprun.xml.AgBiI4")).AutoCreateGraph(x_lims=[-5, 5], save_path="1.5_.pdf")



# <codecell> DOS smoothing, easy-ish manual legend placements, custom y-label
v = Vasprun(PATH + "vasprun.xml.AgBiI4")
dos = LDosPlotter(v)
dos.AddAllElements(sigma = 0.065)
#Generate Legend: Defaults to atoms in upper right, linestyles in lower right.  All of the 
#normal location keywords should work here
dos.GenerateLegend(atom_legend_loc="upper center", line_style_loc="upper right")

plt.ylabel(r"$l$-decomposed DOS (states/eV)")

plt.savefig(PATH + "2_.pdf")
plt.clf()


# <codecell> Non-scaled energy, hide line-style legend, manual zoom-in
v = Vasprun(PATH + "vasprun.xml.AgBiI4")
dos = LDosPlotter(v)
dos.AddAllElements(scale_by_ef = False)
dos.GenerateLegend(line_styles = False)

plt.xlabel("energy (eV)")
plt.xlim(3, 7)
plt.ylim(0, 35)

plt.savefig(PATH + "3_.pdf")
plt.clf()



# <codecell> Dark theme with custom colors, ignoring s orbital DOS, horizontal atom-only legend
plt.style.use("dark_background") #(for when you want to use a lot of black ink while printing)

v = Vasprun(PATH + "vasprun.xml")
dos = LDosPlotter(v)

#Changing colors: The two lists are parallel arrays.  The first list is the index and the second is the color.
#It is important to do this step before plotting the atoms, or the color changes will not show up.
#The reason that I start at 1 is because index 0 is designated black, which is used for single-element plots.
#If there is more than one atom (like in this example), the color at index 0 is unused 
for index, color in zip([1, 2, 3, 4], [(15, 243, 255), (235, 109, 0), (255, 0, 183), (0, 255, 0)]):
    dos.colors[index] = color
    
dos.AddAllElements(sigma = 0.065, hide_s = True)

#Legend editing: Making specific edits to the legend outside of simple keyword-based location changes (like in
#an above example) requires getting the legend dictionaries from the class itself and converting them to lists
#since plt.legend() expects the legend handles to be in list form.  
atomHandlesList = [h for h in dos.atom_legend_handles.values()] 
plt.legend(handles = atomHandlesList, bbox_to_anchor=(0.0, 1, 1, 0.1),
           loc='lower left', ncol=len(dos.unique_elements), mode="expand")   
#You could also get the s-p-d legend entries a similar way.  If you want two seperate legends like the plotter's
#default, you have to add the first legend like this:
'''plt.gca().add_artist(firstplt.legend(handles=atomHandlesList, ...) '''      
#before calling plt.legend() on the s-p-d handles.  
                    
plt.xlim(-10, 5)
plt.savefig(PATH + "4_.pdf")
plt.clf()



plt.style.use("default") #setting the background color above was a global change, so need to revert
# <codecell> Ignore Oxygen, change line styles, combinine two legends into one, line at fermi energy
v = Vasprun(PATH + "vasprun.xml")
dos = LDosPlotter(v)

#Change linestyles: the two arguments are parallel arrays of [orbital], [style].  They don't 
#necessairily have to be in the order s-p-d (because i'm storing the data in dicts, not lists).  
#If you just want to change one style, you don't need to send it as a list.  Like color editing,
#you have to do this before plotting the DOS or the changes won't show up  
dos.ChangeLineStyle(['s', 'p', 'd'], [':', ':', '-'])

#Manually selecting elements:  An example of how you could ignore the DOS of an entire element.
for elem in dos.unique_elements:
    if(elem.symbol != 'O'):
        dos.GetElementDosPlot(elem, sigma = 0.1, scale_by_ef = False)

#Legend editing: This first bit is, again, getting the legends into list form.  Same as above.
atomHandlesList = [h for h in dos.atom_legend_handles.values()] 
spdHandlesList = [s for s in dos.style_legend_handles.values()] 
#Now we want to have all of the legend entries in a single box on the graph.  So we have to concat
#one array (the s-p-d linestyle array in this case) to the end of the other (atom color) array:
allHandlesList = [] 
for sublist in [atomHandlesList, spdHandlesList]:
    for subsublist in sublist:
        allHandlesList.append(subsublist)
#I'm going to have a line for the fermi energy, so I'll want a legend entry for that too:
from matplotlib.lines import Line2D
fermiHandle = Line2D([0], [0], color='orange', alpha=.5, lw=2, linestyle='-', label=r"$E_\mathrm{F}$")  
allHandlesList.append(fermiHandle)      
#Now, pass the array of all handles to plt.legend() and specify where to put it        
plt.legend(handles = allHandlesList, bbox_to_anchor = (0.99, 1), loc = "upper left",
           frameon = False)         

plt.axvline(x=v.efermi, color='orange', linewidth = 0.85, ymin = 0.1, ymax = 0.9, alpha=.5)                    
plt.savefig(PATH + "5_.pdf")
plt.clf()



