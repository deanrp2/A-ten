#Main file for namsless should splinter later in development
 
#UNITS
#time:s
#weight:g
#length:cm
#density: g/cm^3
 
import numpy as np
import scipy.signal
import scipy.optimize
import matplotlib.pyplot as plt
from collections import OrderedDict
import os

 
SMALL_SIZE = 16
MEDIUM_SIZE = 18
BIGGER_SIZE = 24
 
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
 
 
def pull_spectrum(spec_file):
    """
    Function to extract the spectrum from a *.Spe file
    Parameters:
        spec_file - file name of *.Spe file
    Returns:
        spectrum - numpy array of the number of counts per bin 
    """
    with open(spec_file) as data:
        spectrum = np.array([float(i.strip()) for i in data.readlines()[12:2060]])
    return spectrum
 
def smooth(y, box_pts):
    """
    Simple 1-D convolution function
    Parameters:
        y - 1-D numpy array to be smoothed
        box_pts - width of kernel
    Returns:
        y_smooth - smoothed version of y
    """
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
    
 
class ATen:
    def __init__(self,input_filepath):
        self.banner = """                     _______     _________ _______  _       
                    (  ___  )    \__   __/(  ____ \( (    /|
                    | (   ) |       ) (   | (    \/|  \  ( |
                    | (___) | _____ | |   | (__    |   \ | |
                    |  ___  |(_____)| |   |  __)   | (\ \) |
                    | (   ) |       | |   | (      | | \   |
                    | )   ( |       | |   | (____/\| )  \  |
                    |/     \|       )_(   (_______/|/    )_)
                    
               "The People's 1D Continuous Energy Attenuation Code"  
                    
                                                                  _____
                                 .-~~     ~~~~--......___
                                <  |-.                   ~~--._
                                |  |  ~T-....______     ______ `.
                                |  |   |       .   ~~~~~      ~~~
                                |  |   `.     /    -~~-.
                                |  |  . |   .'    '             /`.
                                :  |  | |   |    '            ,' ,.`.
                                \  |  | /   | ,''            / ,' \  ~-.
                                 \  . |`-~~--L |.--.       ,'     /.   `
                          ____  ,'\ >  .~.'   ~`'   `~-.  /   ,  / >    `.
                        /~   _\/   `' '  |           .  \/  ,' .'.~,\    `.
                       /   ,d#b    / '   |           `     '.-~~~,'  >    `m.
                       \  m####b  | '    `            |    ~~~~-<  ,d#.    "##
                     ,-~' ######b ||   |  `           `          \d"d#b      Y
                      ~:  #######b|:   `\  `         ` :          "d###b      .
                       | d########b\    \\  `.        :|           "####b     :
                       ' ##########b     \`-.  .      |`.:          "####b     .
                      ;  ###########\     `--`=`.\     .||          |#####b    |
                     :   ###########b\ :      __  .   '|;|      \   d######\   |
                      \.'############/.`   .-~ \-.|  /./,'      .' d######P `  |
                       ; ###########P | \  ;,b `~|; /,'~`      ,',d######P   | |
                      < :"#########P  '  : \ /.  |,' T~|/ , +-~ db"#####P    | |
                       ~| ########P ,'   '  `-'  ~   P ; /  |  d#######P      \|
                         ~`#####P' /    /           <'  <   `~""######P
                           `###P ,'    <          `.`- / ;  |    "###P..
                        __  "#P /     / \      ._ /   | .   `.    ##P__ ~7~
                     .-~  ~--~\/    ,'/ ,`     | '   _| |     \ -_ P~  ~-'
                    '~\_.-~~7\/    / |L/. `.   `'  .-`  |`.   \`.  ~~~.
                      ~    / |    .| '|-/   `.  .-~\  \\ \_`-. \`  \`.|
                          /  /`.  |_\\\_\.-...~~<__.\  \`-.~~ `-|   | \
                         '~., ##m##"      \  oo. .'  `.~~T~ ~~~/:-. | |
                           |  ###P   .'   |_|88)mmmm'-~  |    / | | /,'
                              ##"    :   dd##>"'####b~-. .  /  | ;-
                              |      :  d###P     ~"~~   > `<  ,'/
                              |      `./"#P~        |   /    \  ~
                              |       /  |          ;  /      |
                              `      /   |      |     .       |
                               \    /    |      |  :  '       '
                                \  ; /`.  \     \  ','       ,
                                 \| '   `.  \  | `./        .
                                  |/      `--._;_ /   ._ _.+'
                                  |             /`-..   ~  |
                                   \           |   ,'      |
                                    `.          \,'/       |
                                      `._      ,' /        |
         _...---.._                     \.       /_        |
       ,'          ~~"--..                ~     /~ ~-_     ;
      /                   ~"-._            \   /      T.  .
     /                         ~-.         |  /       `8bd8
    /              .              `-.      | '         8888
    \             -.\                `-.    '`.        8888b
     \              ~-.                 `-.   |   :   d8888P\
  ,-~~\                ~.                  `. |   ;  d8888P  \
 /     \                 `.                 .~'.    d8888P    \   _.,_
.       \                  `.               `.  `. d8888P      \-~  ~ ~-.
|        \                   .               |    <8888P        \        ~-.
|         \                   \              |     \88P .        \         |
 .         `.                  \             |     |`P-~          .        \
             \                  \            |     |              |        .'
  `           `.                 \           |     |              |        >
   `           \.                 \          |     |              |        '
    `           \`.                \         '     |              ;       ~;
     .           \ -.               \       '      '             .        /
     `               -.              \     '      :              ;      /~
      .           `    -              \  .'       '             .~-.  /~
      `            \    ~-             \~        /              ;   ~~
       `            .     ~.            \     _-~              /
        .            \      -_           \  .-                /
        `                    _-           \~                .'
         .            |`.---~  ~.          \              _-
         `            |  `.___.-~\          \         _.-~
          .           |    `.     \          \~-.__.-~
          `           |      `-.   `.         \
           `          `         ~~---\         \
            .          .              `.        `.
            `          :                \         `.
             \         `                 \          `.
              \         .                 `.         `~~-.
               \        :                   `         \   \
                .        .                   \         : `.\
                `        :                    \        |  | .
                 \        .                    \       |  |
                  \       :                     \      `  |  `
                   .                             .      | |_  .
                   `       `.                    `      ` | ~.;
                    \       `.                    .      . .
                     .       `.                   `      ` `
                     `.       `._.                 \      `.\
                      `        <  \                 `.     | .
                       `       `   :                 `     | |
                        `       \                     `    | |
                         `.     |   \                  :  .' |
   Super-Idol Misty May   `     |    \                 `_-'  |
   (from "Otaku no         :    | |   |                 :    ;
     Video [1985]")        `    ; |~-.|                 :    '
     --- Dov Sherman        :   \ |                     `   ,
                            `    \`                      :  '
                             :    \`                     `_/
                             `     .\
                              `    ` \
                               \    | :
                                \  .'  :
                                 T~    :
                                 |    .'
                                 |    :
                                 |    '
                                 |   /
                                 `_.'

"""
        
        self.input_filepath = input_filepath
        self.casename = self.input_filepath.split("/")[-1][:-3]
        self.working_directory = "./" + "/".join(self.input_filepath.split("/")[:-1]) + "/"
        
        #Reading contecnts of input file
        with open(input_filepath) as input_file:
            self.raw_input = input_file.readlines()
            input_data = [line.strip() for line in self.raw_input if not (line[0] == "#" or line == "\n")]
         
        #Read raw input text into cards
        self.material_card = input_data[input_data.index('READ MATERIAL')+1:input_data.index('END MATERIAL')]
        self.geometry_card = input_data[input_data.index('READ GEOMETRY')+1:input_data.index('END GEOMETRY')]
        self.parameters_card = input_data[input_data.index('READ PARAMETERS')+1:input_data.index('END PARAMETERS')]
        self.paths_card = input_data[input_data.index('READ PATHS')+1:input_data.index('END PATHS')]
         
        #initializing material card
        self.material_process()
        
        
        #parsing geometry related inputs
        self.layer_materials = [a for a in self.geometry_card if a.split()[0] == "layer_material"][0].split()[2:] 
        self.layer_thicknesses = np.array([a for a in self.geometry_card if a.split()[0] == "layer_thicknesses"][0].split()[2:]).astype(np.float32)
        
        #parsing parameter related inputs
        self.parameters = {x[0] : x[1] for x in [parameter.replace(" ", "").split("=") for parameter in self.parameters_card]}
         
        #parsing path related inputs
        self.paths = {x[0] : x[1] for x in [parameter.replace(" ", "").split("=") for parameter in self.paths_card]}
        self.bin_calibration(self.paths["cs137spec_filepath"])
         
        self.source_spec = pull_spectrum(self.paths["source_filepath"])/float(self.parameters["source_time"])
         
        if "background_filepath" in self.paths:
            self.source_spec -= pull_spectrum(self.paths["background_filepath"])/float(self.parameters["background_time"])
        
        #identigy groups and strengths and assign "cross sections"
        self.id_groups(plot_spec_peaks = False, plot_norm_peaks = False)
        self.ac_process()
 
        #layer_thickness
         
         
    def bin_calibration(self,cs137spec_filepath):
        """
        Function to set energy values to each bin. Must be based on cs137 spectrum.
        Parameters:
            self - does not pull any attributes from self
            cs137spec_filepath - file name  of a *.Spe file containing unattenuated spectrum from a Cs-137 source 
        Returns:
            self.bin_energies - numpy array containing the estimated energies associated with each bin
        """
        cs137_peak = 661.6 #keV
         
        #Smooth the spectrum and extract energy local maxima
        cs137_spec = pull_spectrum(cs137spec_filepath)  
        cs137_spec = smooth(cs137_spec,30)
        peaks, empty_dict = scipy.signal.find_peaks(cs137_spec)
         
        #calculate the prominence associated with each maxima and find the bin with the largest prominence
        prominences, left_bases, right_bases = scipy.signal.peak_prominences(cs137_spec, peaks)
        maxEpeak = prominences.argmax()
         
        #Find bin of maximum energy
        maxEbin = peaks[maxEpeak]
        self.maxEbin = maxEbin
        self.cs137_spec = cs137_spec
        delE = cs137_peak/maxEbin
         
        #Create bin energy array
        self.bin_energies = np.arange(0, cs137_spec.size * delE, delE)
                 
        return 1
     
    def id_groups(self, plot_spec_peaks = False, plot_norm_peaks = False, width_threshold = [40, 120], width_rel_height = 0.7):
        """
        Function to identify energy group and count rate of each energy group.
        Parameters:
            self - both bin_energies and source_spec must be defined
            plot_spec_peaks - boolean to plot full source spectrum with e group identified
            plot_norm_peaks = boolean to plot norm fits as well. Should only be true if plot_spec_peaks is true
            width_threshold - tuning parameter for acceptable peak width
        Returns:
            self.group_counts - count rate associated with each group
            self.group_energies - energy value associated with each group
        """
        #Define gaussian checker for later in function    
        def is_gaussian(n, x, y, width_rel_height,be,plot_norm_peaks):
            def gaus(x,a0,mu,sigma):
                return a0*(sigma*np.sqrt(2*np.pi))**-1*np.exp(-(x-mu)**2/(2*sigma**2)) 
 
            a0 = np.trapz(y) #4253
            mean0 =  x[y.argmax()] #sum(x*y)/n #377.977
            sigma0 =  sum(y*(x-mean0)**2)/n # 114.967
             
 
            popt,pcov = scipy.optimize.curve_fit(gaus,x,y,p0=[a0,mean0,sigma0],maxfev=100000)
            perr = np.sqrt(np.diag(pcov)).sum()
             
 
            if perr > 50:
                return (False, 0)
            else:
                if plot_norm_peaks:
                    plt.plot(be,gaus(x,*popt),'o', c = "mediumseagreen", MarkerSize=5, label = "Gaussian Approximation")
                return (True, popt[0])
         
        #initializing figure if necessary
        if plot_spec_peaks or plot_norm_peaks:
            plt.figure(figsize=[15,8])
         
        #Smooth signal to and easily identify spectrum peaks
        smoothed_spec = smooth(self.source_spec,30)
        peaks, empty_dict = scipy.signal.find_peaks(smoothed_spec)
         
         
        #Apply criteria that prominences must be greater than the average promenance
        prominences, left_bases, right_bases = scipy.signal.peak_prominences(smoothed_spec, peaks)
        peaks = np.compress(prominences > prominences.mean(), peaks)
         
        #Apply criteria that widths must be greater than width_threshold
        widths, width_heights, leftips, rightips = scipy.signal.peak_widths(x = smoothed_spec, peaks = peaks, rel_height = width_rel_height)
        peaks = np.compress((widths > width_threshold[0]) * (widths < width_threshold[1]), peaks)
        leftips = np.floor(np.compress((widths > width_threshold[0]) * (widths < width_threshold[1]), leftips)).astype(np.int32)
        rightips = np.ceil(np.compress((widths > width_threshold[0]) * (widths < width_threshold[1]), rightips)).astype(np.int32)    
        widths = np.compress((widths > width_threshold[0]) * (widths < width_threshold[1]), widths)
         
         
        #Apply criteria that shape must be appropriately gaussian
        #Hiding in here is getting the count rate under each peak as a return from the is_gaussian
        remove_i = np.array([]).astype(int)
        group_counts = np.array([])
        for i in range(peaks.size):
            n = rightips[i]-leftips[i]
            x = np.linspace(leftips[i],rightips[i],n)
            y = self.source_spec[leftips[i]:rightips[i]]
            gaussianality, group_count = is_gaussian(n,x,y, width_rel_height,self.bin_energies[leftips[i]:rightips[i]],plot_norm_peaks = plot_norm_peaks)
            if not gaussianality:
                remove_i = np.append(remove_i, i)
            else:
                group_counts = np.append(group_counts, group_count)
             
        peaks = np.delete(peaks,remove_i)
        leftips = np.delete(leftips,remove_i)
        rightips = np.delete(rightips,remove_i)
                      
        #Add optional peak plotted to make sure peaks were done correctly
        if plot_spec_peaks:
            plt.plot(self.bin_energies,self.source_spec, c = "royalblue",label = "Source Spectrum")
             
            for i in range(leftips.size):
                plt.axvline(self.bin_energies[peaks[i]], c = "crimson", label = "Group Energy Value")
 
                 
            plt.ylabel("Counts [#/s]")
            plt.xlabel("Energy [keV]")
            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = OrderedDict(zip(labels, handles))
            plt.legend(by_label.values(), by_label.keys())
 
     
        self.group_counts = group_counts
        self.group_energies = self.bin_energies[peaks]
        return 1
     
    def material_process(self):
        """
        Function to decompose entries in MATERIAL CARD from text into data structs
        Parameters:
            self - must have material_card specified
        Returns:
            self.materials - dictionary-containing two items, a density and a 
            material composition list
        """
        self.materials = {}
        for entry in self.material_card:
            entry = entry.split()
            material = entry.pop(0)
            density = float(entry.pop(0))
            composition = [[int(entry[2*i]), float(entry[2*i-1])] for i in range(int(len(entry)/2))]
            self.materials[material] = [density, composition]
         
        return 1
     
    def ac_process(self):
        """
        Function to assign cross sections to each energy group for each material
        Parameters:
            self - must have self.materials defined
        Returns:
            self.ac - dictionary with keys of each material ID and values of list representing energies
                    - energy list as follows 
                        - each row is a separate nuclide
                        - each column is an energy group
                        - sum each row for total ac for an energy group
        """
        def pull_ac(filename):
            #function to pull cross sections from libraries in workable form
            with open(filename, "r") as f:
                lib = np.array([s[3:].split() for s in f.readlines()])[:,:2].astype(np.float32)
            return lib

        self.ac = {}
        for key, value in self.materials.items():
            density = value[0]
            group_ac = np.empty((len(value[1])))
            for energy in self.group_energies:
                ac = np.array([])
                for znum, mass_frac in value[1]:
                    library = "alib/" + [i for i in os.listdir("alib/") if "alib_" + str(znum) in i][0]
                    temp_ac = pull_ac(library)
                    ac = np.append(ac, np.interp(energy/1000,temp_ac[:,0],temp_ac[:,1])*mass_frac)
                
                group_ac = np.vstack((group_ac, ac*density))
            self.ac[key] = group_ac[1:,:] #some adjustment that needs to be made because of array initialization
        return 1
                 
    
    def compute(self):
        """
        
        """
        def solve_master(master_ara, div_rows):
            for i in range(master_ara.shape[0]):
                if np.isclose(master_ara[i,1],0):
                    thickness = master_ara[i,2] - master_ara[i-1,2] 
                    master_ara[i,1] = master_ara[i-1,1]*np.exp(-master_ara[i-1,3]*thickness)

        
        #setting up depth vector and n depending on "layer_mesh_divs"
        if "layer_mesh_divs" in self.parameters.keys():
            depth = np.array([0])
            material_list = []
    
            n = int(self.parameters["layer_mesh_divs"])
            
            for thickness, material in zip(self.layer_thicknesses,self.layer_materials):
                material_list += n*[material]
                start = depth[-1]
                stop = depth[-1]+thickness
                depth = np.append(depth, np.linspace(start + (stop-start)/(n+1) ,depth[-1]+thickness,n))
        else:
            n = 1
            depth = np.append(0,np.cumsum(self.layer_thicknesses))
            material_list = self.layer_materials
            
            
        #set up master array with columns energy, strength, depth, and atten coeff
        master_ara = np.zeros((depth.size*self.group_energies.size, 4))
        
        #create array with enery group repeated the same number of times as the length of depth vec
        working_grp = np.array([])
        for i in reversed(range(self.group_energies.size)):
            working_grp = np.append(working_grp, np.tile(self.group_energies[i],depth.size))
        
        #set up attenuation coeff vector
        ac_vec = np.array([])
        
        self.material_divisions = []
        
        for i in range(self.group_energies.size):
            ac_vec = np.append(0,ac_vec)
            for mat in material_list:
                ac_vec = np.append( self.ac[mat][i,:].sum(), ac_vec)
                self.material_divisions.append(mat)
        

        #place these vectors in master_ara
        master_ara[:,0] = working_grp
        master_ara[:,2] = np.tile(depth, self.group_energies.size)
        master_ara[:,3] = ac_vec
        
        #finding rows that start each energy group
        div_rows = np.array([0])
        for i in range(master_ara.shape[0]-1):
            if master_ara[i,3]==0:
                div_rows = np.append(div_rows, i+1)
                
        #initializing count rate for each energy group
        master_ara[div_rows,1] = self.group_counts
        
        #Fill in counts to each division in master_ara
        solve_master(master_ara, div_rows)
        
        self.master_ara = [master_ara,div_rows]
        
        return 1
        
    def print_output(self):
        def heading(string):
            return("\n" + 80*"-" + "\n" + string + "\n" + 80*"-" + "\n")
            
        #for i in vars(self):
        #    print(i, vars(self)[i])
        #print("\n\n\n\n\n\n")
        
        #set up output and banner
        output = open(self.working_directory + self.casename + ".out", "w")
        output.write(self.banner + "\n\n")
        
        #printing raw input
        output.write(heading("Raw Input"))
        output.write("".join(self.raw_input))
        
        #printing cards
        output.write(heading("Material Card"))
        output.write("\n".join(self.material_card) + "\n")
        output.write(heading("Geometry Card"))
        output.write("\n".join(self.geometry_card) + "\n")
        output.write(heading("Parameters Card"))
        output.write("\n".join(self.parameters_card) + "\n")        
        output.write(heading("Paths Card"))
        output.write("\n".join(self.paths_card) + "\n")        

        #printing materials
        output.write(heading("Materials"))
        for key, item in self.materials.items():
            #print(key,item[)
            output.write("Material: %s       Density: %.4f [g/cm^3]\n" % (key.ljust(15), item[0]))
            output.write("Atomic Number        Mass Fraction\n")
            for z,p in item[1]:
                output.write("%i                   %.5f\n"%(z,p))
            output.write("\n")
        
        #printing geomety
        output.write(heading("Geometry"))
        output.write("Material             Layer Thickness [cm]    Cumulative Thickness [cm]\n")
        accum = 0
        for i in range(len(self.layer_materials)):
            accum += self.layer_thicknesses[i]
            output.write("{:<17}".format(self.layer_materials[i]) + "    %.5f"%self.layer_thicknesses[i] + " "*17 + "%.5f"%(accum) + "\n")
            
        #printing group energy and strength
        output.write(heading("Energy Group Identification"))
        output.write("Group Energy [keV]                Group Count Rate [#/s]\n")
        for i in range(len(self.group_counts)):
            grp = "%.5f"%(self.group_energies[i])
            output.write(grp + (34 - len(grp))*" " + "%.5f\n"%(self.group_counts[i]))
            
        #printing master array
        output.write(heading("Master Array"))
        output.write("Grp Energy [keV]   Count Rate [#/s]   Depth [cm]   Atten Coeff [cm^2]   Material\n")
      
        i = 0
        for j, row in enumerate(self.master_ara[0]):
            e = "%.3f"%row[0]
            s = "%.3f"%row[1]
            d = "%.3f"%row[2]
            c = "%.5f"%row[3]
            
            if np.isclose(row[3],0):
                m = ""
            else:
                m = self.material_divisions[i]
                i += 1
            
            output.write(e + " "*(19-len(e)) + s + " "*(19-len(s)) + d + " "*(13-len(d))+ c + (21-len(c))*" " + m + "\n")
            
            if m == "":
                output.write(26*" - " + "\n")
            
        #attenuation coefficient libraries
        output.write(heading("Attenuation Coefficient Values"))
        for key, item in self.ac.items():
            output.write("Material = {mat}\n".format(mat = key))
            output.write("Atomic Number   Mass Fraction    ")
            for i, e in enumerate(self.group_energies):
                a = "E%i:%.2f"%(i,e)
                output.write(a + " "*(15-len(a)))
            output.write("\n")    
            for i in range(item.T.shape[0]):
                anum = str(self.materials[key][1][i][0])
                frac = "%.4f"%self.materials[key][1][i][1]
                output.write(anum + " "*(16-len(anum)) + frac + " "*11 ) 
                for j in range(item.T.shape[1]):
                    const = "%.4f"%item.T[i,j]
                    output.write(const + " "*(15-len(const)))
                output.write("\n")
            output.write("\n")
            
        
        #printing calibration spectra with peak identified
        output.write(heading("Cs-137 Calibration Spectrum"))
        output.write("Bin Number           Count Number\n")
        for i in range(self.cs137_spec.size):
            output.write("{:<21}".format(str(i)) + str(self.cs137_spec[i]))
            
            if i == self.maxEbin:
                output.write("    *661.5 keV peak, used for calibration")
            
            output.write("\n")
            
        #printing source spectra
        output.write(heading("Unattenuated Spectra"))
        output.write("Bin Energy [keV]              Count Rate [#/s]\n")
        for i in range(self.source_spec.size):
            e = "%.5f"%self.bin_energies[i]
            s = "%.5f\n"%np.abs(self.source_spec[i])
            output.write(e +(30-len(e))*" " + s)
        
        
        output.close()
             

             
for file in os.listdir("working/"):
    if ".at" in file:                                                                      
        test = ATen("working/" + file)    
        test.compute()
        test.print_output()
