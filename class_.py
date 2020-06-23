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
    completeDos = None
    uniqueElements = []    
    spinPol = None
    
    lineStyle = {'s': '-',
                 'p': '--',
                 'd': ':'
                }
    legend = []
    
    def __init__(self, vasprun):
        #Initialize list of unique elements and their pdos if formatting is correct
        if(self.IsLDecomposed(vasprun)):
            for i in range(0, len(vasprun.complete_dos.structure.sites)):
                counted = False
                for j in range(0, len(self.uniqueElements)):
                    if(vasprun.complete_dos.structure.sites[i].species_string == self.uniqueElements[j].name):
                        counted = True
                        break
                if(not counted):
                    self.uniqueElements.append(Element(vasprun.complete_dos.structure.sites[i].species_string))
            
            self.completeDos = vasprun.complete_dos
        else:
            print("BadVasprunWarning:  The DOS info in your .xml file is not formatted into s-p-d components.")
    
        #Determine if spin pol is on
        self.spinPol = self.IsSpinPolarized(vasprun)
    
    def IsLDecomposed(self, vasprun):
        if(vasprun.pdos == []):
            return False
        return True
    
    def IsSpinPolarized(self, vasprun):
        return vasprun.is_spin
    
    def GetElementDosPlot(self, elements, sigma = 0, scaleByEf = True, hideS = False, hideP = False, hideD = False):
        global COLORS
        global COLOR_INDEX
        COLOR_INDEX = (COLOR_INDEX + 1)%len(COLORS) if (len(self.uniqueElements) > 1) else (COLOR_INDEX)%len(COLORS)
        color = tuple(GetColor(COLOR_INDEX))   
         
        if(not isinstance(elements, list)):
            elements = [elements]
        
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
                ##condition for spin pol
                if(self.spinPol):
                   y = [-y for y in s.densities[Spin.down]] if sigma <= 0 else [-y for y in s.get_smeared_densities(sigma)[Spin.down]]
                   plt.plot(x, y, color=color, linestyle=str(style), linewidth=.8)                 
            if(not hideP):
                style = self.lineStyle['p']
                y = p.densities[Spin.up] if sigma <= 0 else p.get_smeared_densities(sigma)[Spin.up]                
                plt.plot(x, y, color=color, linestyle=str(style), linewidth=.8)            
                ##condition for spin pol
                if(self.spinPol):
                   y = [-y for y in p.densities[Spin.down]] if sigma <= 0 else [-y for y in p.get_smeared_densities(sigma)[Spin.down]]
                   plt.plot(x, y, color=color, linestyle=str(style), linewidth=.8)
            if(not hideD):
                style = self.lineStyle['d']
                y = d.densities[Spin.up] if sigma <= 0 else d.get_smeared_densities(sigma)[Spin.up]                
                plt.plot(x, y, color=color, linestyle=str(style), linewidth=.8)        
                ##condition for spin pol
                if(self.spinPol):
                   y = [-y for y in d.densities[Spin.down]] if sigma <= 0 else [-y for y in d.get_smeared_densities(sigma)[Spin.down]]
                   plt.plot(x, y, color=color, linestyle=str(style), linewidth=.8)
        return
    
    def GenerateLegend(self, atoms = True, lineStyles = True):
        if(atoms):
            first = plt.legend(handles = self.legend, loc = "upper right")
            plt.gca().add_artist(first)    
        
        if(lineStyles):
            legend2 = []
            legend2.append(Line2D([0], [0], color='k', lw=2, linestyle = self.lineStyle['s'], label='s'))
            legend2.append(Line2D([0], [0], color='k', lw=2, linestyle = self.lineStyle['p'], label='p'))
            legend2.append(Line2D([0], [0], color='k', lw=2, linestyle = self.lineStyle['d'], label='d'))
            plt.legend(handles = legend2, loc = "lower right")
        
        return

