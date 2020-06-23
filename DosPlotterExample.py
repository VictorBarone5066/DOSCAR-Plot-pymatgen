#Making the pymatgen plots not quite as ugly

from pymatgen.io.vasp import Vasprun
import matplotlib.pyplot as plt

import class_ as myClass

#Stuff to force times new roman style
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.tight_layout = True

#Initialize a vasprun instance and a myClass instance
v = Vasprun("C://Users//baron//Desktop//xmlgen//spdDosPol//vasprun.xml")
test = myClass.TempName(v)

if(test.IsLDecomposed(v)):  
    #Add elements to the plot.  In this case, add all of them.  Sigma = (cubic) spline smoothing
    for elem in test.uniqueElements:
        test.GetElementDosPlot(elem, sigma = 0.065)
    
  
    #Customize the plot with whatever else you want    
    plt.title("hello :)")
    plt.xlabel(r"$E-E_\mathrm{F}$ (eV)")
    plt.ylabel("DOS (states / eV)")
    #plt.legend(handles = test.legend)
    test.GenerateLegend()
    if(not test.spinPol):
        plt.ylim(0)
    
    #Be cure to save (if necessary) and clear the plot when done
    plt.savefig("C://Users//baron//Desktop//exmple.pdf")
    plt.clf()

  
    





