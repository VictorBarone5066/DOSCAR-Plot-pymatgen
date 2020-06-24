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
    atomLegend = []
    styleLegend = []
    
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
            self.atomLegend.append(Line2D([0], [0], color=color, lw=2, label=element.name))
            
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
            first = plt.legend(handles = self.atomLegend, loc = "center", frameon=False, bbox_to_anchor=(1.068, 0.5))
            plt.gca().add_artist(first)    
        
        if(lineStyles):            
            self.styleLegend.append(Line2D([0], [0], color='k', lw=2, linestyle = self.lineStyle['s'], label='s'))
            self.styleLegend.append(Line2D([0], [0], color='k', lw=2, linestyle = self.lineStyle['p'], label='p'))
            self.styleLegend.append(Line2D([0], [0], color='k', lw=2, linestyle = self.lineStyle['d'], label='d'))
            plt.legend(handles = self.styleLegend, loc = "center", frameon=False, bbox_to_anchor=(1.065, .1))
        
        return
    
    def AutoCreateGraph(self, vasprun, xLims = [None, None], yLims = [None, None], saveLoc = "spdGraph.pdf"):
        if(self.IsLDecomposed(vasprun)):  
            #Add elements to the plot.  In this case, add all of them.
            for elem in self.uniqueElements:
                self.GetElementDosPlot(elem)
            
          
            #Plot Customization   
            plt.xlabel(r"$E-E_\mathrm{F}$ (eV)")
            plt.ylabel("DOS (states / eV)")
            self.GenerateLegend()
            if(xLims[0] != None and xLims[1] != None):
                plt.xlim(xLims[0], xLims[1])
            if(yLims[0] != None and yLims[1] != None):
                plt.ylim(yLims[0], yLims[1])                
            elif(not self.spinPol):
                plt.ylim(0)
            
            #Be cure to save (if necessary) and clear the plot when done
            plt.savefig(saveLoc)
            plt.clf() 
            return
        
        else:
            print("AutoCreateGraph:  Your .xml file does not contain s-p-d components\n")
            return

