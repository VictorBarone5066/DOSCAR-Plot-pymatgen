#Making the pymatgen plots not quite as ugly

from pymatgen.io.vasp import Vasprun
import matplotlib.pyplot as plt

import class_ as myClass

#Stuff to force times new roman style
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.tight_layout = False

#Initialize a vasprun instance and a myClass instance
v = Vasprun("C://Users//baron//Desktop//xmlgen//vasprun.xml.AgBiI4")
test = myClass.TempName(v)
test.AutoCreateGraph(v, xLims = [-5, 5], saveLoc = "C://Users//baron//Desktop//pleaseBroPlease.pdf")

#if(test.IsLDecomposed(v)):  
#    #Add elements to the plot.  In this case, add all of them.  Sigma = (cubic) spline smoothing
#    for elem in test.uniqueElements:
#        test.GetElementDosPlot(elem, sigma = 0.065)
#    
#  
#    #Customize the plot with whatever else you want    
#    plt.title("hello :)")
#    plt.xlabel(r"$E-E_\mathrm{F}$ (eV)")
#    plt.ylabel("DOS (states / eV)")
#    test.GenerateLegend()
#    if(not test.spinPol):
#        plt.ylim(0)
#    
#    #Be cure to save (if necessary) and clear the plot when done
#    plt.savefig("C://Users//baron//Desktop//exmple.pdf")
#    plt.clf()

  
    





