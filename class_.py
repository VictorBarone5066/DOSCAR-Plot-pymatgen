# for making graphs
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

from pymatgen.core.composition import Element
from pymatgen.electronic_structure.core import OrbitalType, Spin

COLORS = [(0, 0, 0), #black
          (255, 0, 0), #red
          (0, 173, 0), #(better) green
          (0, 0, 255), #blue
          (255, 0, 183), #pink
          (15, 243, 255), #cyan
          (235, 109, 0), #orange
          (153, 0, 235) #purple
          ]
COLOR_INDEX = 0
def GetColor(i):
    return (a / 255 for a in COLORS[i])


class TempName:
    plot = None
    completeDos = None
    uniqueElements = []    
    
    lineStyle = {'s': '-',
                 'p': '--',
                 'd': ':'
                }
    legend = []
    
    def __init__(self, vasprun):
        #Initialize list of unique elements and their pdos
        for i in range(0, len(vasprun.complete_dos.structure.sites)):
            counted = False
            for j in range(0, len(self.uniqueElements)):
                if(vasprun.complete_dos.structure.sites[i].species_string == self.uniqueElements[j].name):
                    counted = True
                    break
            if(not counted):
                self.uniqueElements.append(Element(vasprun.complete_dos.structure.sites[i].species_string))
        
        self.completeDos = vasprun.complete_dos
        
    def GetElementDosPlot(self, elements, sigma = 0, scaleByEf = True, hideS = False, hideP = False, hideD = False):
        global COLORS
        global COLOR_INDEX
        COLOR_INDEX = (COLOR_INDEX + 1)%len(COLORS)
        color = tuple(GetColor(COLOR_INDEX))   
         
        if(not isinstance(elements, list)):
            elements = [elements]
        
        #This is (probably) the non-general part.  I need info on what kinds of things get_element_spd_dos
        #can return to make this work for all cases (xyz decomposed?  Where is the spin-pol stuff at???
        #what happens if you just have total DOS w/o spd?).
        for element in elements:
            self.legend.append(Line2D([0], [0], color=color, lw=2, label=element.name))
            
            #I forsee needing to get rid of explicit DOS variables b/c of the number of potential cases
            s = (self.completeDos.get_element_spd_dos(element)[OrbitalType.s])
            p = (self.completeDos.get_element_spd_dos(element)[OrbitalType.p])
            d = (self.completeDos.get_element_spd_dos(element)[OrbitalType.d])        
            
            x = [e - s.efermi for e in s.energies] if scaleByEf else s.efermi
            if(not hideS):
                style = self.lineStyle['s']
                y = s.densities[Spin.up] if sigma <= 0 else s.get_smeared_densities(sigma)[Spin.up]
                plt.plot(x, y, color=color, linestyle=str(style), linewidth=.8)
            if(not hideP):
                style = self.lineStyle['p']
                y = p.densities[Spin.up] if sigma <= 0 else p.get_smeared_densities(sigma)[Spin.up]                
                plt.plot(x, y, color=color, linestyle=str(style), linewidth=.8)            
            if(not hideD):
                style = self.lineStyle['d']
                y = d.densities[Spin.up] if sigma <= 0 else d.get_smeared_densities(sigma)[Spin.up]                
                plt.plot(x, y, color=color, linestyle=str(style), linewidth=.8)        
        return

