import ROOT
from ROOT import TChain
from ctypes import c_double
import os
import numpy as np

years = ["2015","2016","2017"]
yeardict = { 
   "2011": "Strip20",
  "2015" : "Turbo15",
  "2016" : "Turbo16",
  "2017" : "Turbo17",
  }
magnitudes = ["MagDown"]
binnings = ["non-BHH", "new-binning"]
binning_schemes = {
  "non-BHH" : "",
  "new-binning" : "Xic_Binning_",
}
mother_particles = ["Lc", "Xic"]
particles = ["pplus","kminus", "piplus"]
particles_short ={
  "pplus" : "P",
  "kminus" : "K",
  "piplus" : "Pi",
}



def make_comparison_graph_plot(year, magnitude, binning, mother_particle, particle):
  print(f'running with({year}, {magnitude}, {binning}, {mother_particle}, {particle})')
  c1 = ROOT.TCanvas('c1', f'{mother_particle}_{particle}')
  
  if binning=="non-BHH":
    
    if year=="2017":
        PID_cuts = {
                    "pplus" : "ProbNNp > 0.5 && DLLp > 0_",
                    "kminus" : "ProbNNK > 0.4 && DLLK > 0_",
                    "piplus" : "ProbNNpi > 0.5_",
                    }
        PIDfolder = "/project/bfys/jdevries/cmtuser/LHCb_Xic_production/pidcalib/UraniaDev_v10r1/"
        PIDfilename = f"PerfHists_{particles_short[particle]}_{yeardict[year]}_{magnitude}_P_ETA_nTracks_Brunel.root"
    else: 
        PID_cuts = {
            "pplus" : "ProbNNp > 0.5_0_",
            "kminus" : "ProbNNK > 0.4_0_",
            "piplus" : "ProbNNpi > 0.5_0_",
           }
        PIDfolder = "/project/bfys/jdevries/cmtuser/LHCb_Xic_production/pidcalib/UraniaDev_v7r0/"
        PIDfilename = f"PerfHists_{particles_short[particle]}_{yeardict[year]}_{magnitude}_P_ETA_nTracks_Brunel.root"
    
   
    PIDfile = ROOT.TFile.Open(PIDfolder + PIDfilename)
 
    

    PIDhistbeforecut_name = f"TotalHist_{particles_short[particle]}_MC15TuneV1_{PID_cuts[particle]}_{particles_short[particle]}_P_{particles_short[particle]}_Eta_nTracks_Brunel"
    print( PIDhistbeforecut_name)
    PIDhistbeforecut = PIDfile.Get(PIDhistbeforecut_name)
    PIDhistaftercut_name = f"PassedHist_{particles_short[particle]}_MC15TuneV1_{PID_cuts[particle]}_{particles_short[particle]}_P_{particles_short[particle]}_Eta_nTracks_Brunel"
    PIDhistaftercut = PIDfile.Get(PIDhistaftercut_name)
    

  if binning=="new-binning":
    print("new-binning***********************")

    if year=="2017":
        PID_cuts = {
            "pplus" : "ProbNNp > 0.5 && DLLp > 0_",
            "kminus" : "ProbNNK > 0.4 && DLLK > 0_",
            "piplus" : "ProbNNpi > 0.5_"}
        PIDfolder = "/project/bfys/jdevries/cmtuser/LHCb_Xic_production/pidcalib/UraniaDev_v10r1/"
        PIDfilename = f"PerfHists_{particles_short[particle]}_{yeardict[year]}_{magnitude}_Xic_Binning_P_ETA_nTracks_Brunel.root"

    else: 
        PID_cuts = {
            "pplus" : "ProbNNp > 0.5 && DLLp > 0_0_",
            "kminus" : "ProbNNK > 0.4 && DLLK > 0_0_",
            "piplus" : "ProbNNpi > 0.5_0_"}
        PIDfolder = "/project/bfys/jdevries/cmtuser/LHCb_Xic_production/pidcalib/UraniaDev_v7r0/"
        PIDfilename = f"PerfHists_{particles_short[particle]}_{yeardict[year]}_{magnitude}_BHH_Binning_P_ETA_nTracks_Brunel.root"
 
    PIDfile = ROOT.TFile.Open(PIDfolder + PIDfilename)
    PIDhistbeforecut_name = f"TotalHist_{particles_short[particle]}_MC15TuneV1_{PID_cuts[particle]}_{particles_short[particle]}_P_{particles_short[particle]}_Eta_nTracks_Brunel"
    PIDhistbeforecut = PIDfile.Get(PIDhistbeforecut_name)
    PIDhistaftercut_name = f"PassedHist_{particles_short[particle]}_MC15TuneV1_{PID_cuts[particle]}_{particles_short[particle]}_P_{particles_short[particle]}_Eta_nTracks_Brunel"
    PIDhistaftercut = PIDfile.Get(PIDhistaftercut_name)
  print(type(PIDhistbeforecut))
  print(PIDhistbeforecut_name)
  if PIDhistbeforecut.GetEntries() > 0:
    print("The histogram has entries.")
  X = PIDhistbeforecut.ProjectionX('X')
  Y = PIDhistbeforecut.ProjectionY('Y')
  Z = PIDhistbeforecut.ProjectionZ('Z')
  
  if mother_particle == 'Lc':
    print("lc")
    filedir = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/145"
    filename = "MC_Lc2pKpiTuple_25103064.root"
  if mother_particle == 'Xic':
    filedir = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/16"
    filename = "MC_Lc2pKpiTuple_26103092.root"

  subjobs = next(os.walk(filedir))[1]
  excludedjobs = []
  tree = TChain("tuple_Lc2pKpi/DecayTree")


  for job in subjobs:
    if not job in excludedjobs :
      tree.Add("{0}/{1}/{2}".format(filedir,job,filename))
  """for branch in tree.GetListOfBranches():
    print(f"Branch Name: {branch.GetName()}")
    print("*****************************************")"""





  #add the sweights here:
  file_path = "/data/bfys/cpawley/LcAnalysis_plots/sWeights/2017_MagDown/Lc_total_sWeight_swTree.root"
  tree_sw = TChain("dataNew") 
  tree_sw.Add(file_path)
  """
  if tree.GetEntries() != tree_sw.GetEntries():
    raise ValueError("Number of entries in the main tree does not match the number of entries in the sWeights tree") """


  weights_branch=tree_sw.GetBranch("Actual_signalshape_Norm_sw")
  """for entry in tree_sw:
    print(getattr(entry, "Actual_signalshape_Norm_sw"))
  for  entry in tree_sw:
    weight=getattr(entry, "Actual_signalshape_Norm_sw")
    print(type(weight))"""






  
  output_file = ROOT.TFile("/data/bfys/cpawley/LcAnalysis_plots/sWeights/experimenting_cloned_tree_with_weights.root", "RECREATE")
  cuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus_P < 120000 && kminus_P < 115000 && piplus_P < 80000"
  cloned_tree = tree.CopyTree(cuts)
  print(f"Number of entries in original tree: {tree.GetEntries()}")
  print(f"Number of entries in cloned tree: {cloned_tree.GetEntries()}")
  cloned_tree.AddFriend(tree_sw, "sw_tree")
  biggest=0
  smallest=0
  for entry in cloned_tree:
    weight = getattr(entry, "sw_tree.Actual_signalshape_Norm_sw")
    if weight<smallest:
      smallest=weight
    if weight>biggest:
      biggest=weight

  print(f"smallest: {smallest} and the biggest= {biggest}")




  
  myhistogram_mother_particle = {
    "Lc" : "myhistogram_Lc",
    "Xic" : "myhistogram_Xic",
  }
  myhistogram = myhistogram_mother_particle[mother_particle]
  axesbinsX = X.GetXaxis().GetXbins()
  axesbinsY = Y.GetXaxis().GetXbins()
  axesbinsZ = Z.GetXaxis().GetXbins()
  print("***********************************************",axesbinsX,axesbinsY,axesbinsZ,"****************************************")
  


  myhistogram = ROOT.TH3F('myhistogram',f'Total efficiency {particle}_{mother_particle}', axesbinsX.GetSize()-1, axesbinsX.GetArray(), axesbinsY.GetSize()-1, axesbinsY.GetArray(), axesbinsZ.GetSize()-1, axesbinsZ.GetArray())
  cuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus_P < 120000 && kminus_P < 115000 && piplus_P < 80000"
  cuts = "lcplus_M >= 2240 && lcplus_M <= 2340"
  #tree.Draw(f"nTracks:{particle}_ETA:{particle}_P>>+myhistogram", cuts)
  import numpy as np 
  num_entries = tree_sw.GetEntries()
  weights_vector=ROOT.std.vector('double')(num_entries, 1.0)
  weights_array = np.ones(num_entries)

  #tree.Draw(f"nTracks:{particle}_ETA:{particle}_P>>+myhistogram", f"({cuts}) * sw_tree.Actual_signalshape_Norm_sw")

  xaxis = myhistogram.GetXaxis()
  print("X axis title:", xaxis.GetTitle()) 
  yaxis = myhistogram.GetYaxis()
  print("Y axis title:", yaxis.GetTitle()) 
  zaxis = myhistogram.GetZaxis()
  print("Z axis title:", zaxis.GetTitle()) 
  
  print("X axis bin edges:", [xaxis.GetBinLowEdge(i) for i in range(1, xaxis.GetNbins()+2)])
  print("Y axis bin edges:", [yaxis.GetBinLowEdge(i) for i in range(1, yaxis.GetNbins()+2)])
  print("Z axis bin edges:", [zaxis.GetBinLowEdge(i) for i in range(1, zaxis.GetNbins()+2)])


  n_bins_x = PIDhistaftercut.GetNbinsX()
  n_bins_y = PIDhistaftercut.GetNbinsY()
  n_bins_z = PIDhistaftercut.GetNbinsZ()


  
  for entry in cloned_tree:
    z= getattr(entry, "nTracks")  
    y= getattr(entry, f"{particle}_ETA")  
    x= getattr(entry, f"{particle}_P")  
    weight= getattr(entry, "sw_tree.Actual_signalshape_Norm_sw")
    if weight<0:
      weight=0
    #print(x,y,z,weight)
    myhistogram.Fill(x,y,z,weight)


  ratio = PIDhistaftercut.Clone()
  ratio.Divide(PIDhistbeforecut)


  n_bins_x = PIDhistaftercut.GetNbinsX()
  n_bins_y = PIDhistaftercut.GetNbinsY()
  n_bins_z = PIDhistaftercut.GetNbinsZ()
  print(f"number x:{n_bins_x}, number y:{n_bins_y}, number z: {n_bins_z}")

  nbinranges = []
  nbinranges += [1]
  nbinranges += [ axesbinsX.GetSize() -1 ]
  nbinranges += [1]
  nbinranges += [ axesbinsY.GetSize() -1 ]
  nbinranges += [1]
  nbinranges += [ axesbinsZ.GetSize() -1 ]

  efftotal_error = c_double(0.0)
  #myhistogram.Sumw2()        #sum of w^2 also stored RETURNS TO NONE THOUGH

  ntotal = myhistogram.Integral(*nbinranges)
  myhistogram.Multiply(ratio)

  for x in range(1, n_bins_x + 1):
    for y in range(1, n_bins_y + 1):
        for z in range(1, n_bins_z + 1):
            ratio_value = ratio.GetBinContent(x, y, z)
            myhist_value = myhistogram.GetBinContent(x, y, z)
            #print(myhist_value)
            
            if myhist_value != 0:
                error_value = ratio_value * (1 - ratio_value) / myhist_value
            else:
                error_value = 0
            
            myhistogram.SetBinError(x, y, z, error_value)
            #print(f"Bin ({x}, {y}, {z}): Value = {myhist_value}, Error = {error_value}")
  efftotal = myhistogram.IntegralAndError(*(nbinranges + [efftotal_error]))
  print(efftotal)
  ntotal = c_double(ntotal)
  efftotal = c_double(efftotal)

  efftotal = efftotal.value / ntotal.value
  efftotal_error = efftotal_error.value / ntotal.value
  print(f"PID efficiency and an error of {mother_particle}_{particle} is {efftotal:.10f} +- {efftotal_error:.10f}")
  return [year, magnitude, mother_particle, particle, f'{efftotal:.10f}', f'{efftotal_error:.10f}'], efftotal, efftotal_error

# Table headers
header_1 = ['Year', 'Magnitude', 'Mother_particle', 'Daughter_particle', 'Efficiency', 'Statistical error', 'Systematic_error']
header_2 = ['Mother_particle', 'Efficiency', 'Statistical error', 'Systematic_error']

# Print headers
print(f"{' | '.join(header_1)}")
print('-' * 80)

for mother_particle in mother_particles:
  totaleff = 1
  totaleff_new_binning = 1
  totaleff_error = 0
  for year in years:
    for magnitude in magnitudes:
      for particle in particles:
        table_entry, efftotal, efftotal_error = make_comparison_graph_plot(year=year, magnitude=magnitude, binning='non-BHH', mother_particle=mother_particle, particle=particle)
        _, efftotal_new_binning, _ = make_comparison_graph_plot(year=year, magnitude=magnitude, binning='new-binning', mother_particle=mother_particle, particle=particle)
        table_entry.append(f'{abs(efftotal-efftotal_new_binning):.4f}')
        # Print table entry
        print(f"{' | '.join(table_entry)}")
        totaleff = totaleff * efftotal
        totaleff_new_binning = totaleff_new_binning * efftotal_new_binning
        totaleff_error = efftotal_error / efftotal + totaleff_error
        
  totaleff_error = totaleff_error * totaleff
  # Print summary
  print(f"{mother_particle} | {totaleff:.10f} | {totaleff_error:.10f} | {abs(totaleff-totaleff_new_binning):.10f}")
  print('-' * 80)

print("done")
