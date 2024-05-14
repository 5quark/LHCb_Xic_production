import ROOT
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/user/achoban/LHCb_Xic_production/analysis/Scripts/')
import Imports
import os


#The function calculates the trigger efficiencies for each bin in 2 axis.
def tistos(file_path, bins_chosen_branch_1,branchname_1, bins_chosen_branch_2,branchname_2 ):

    root_file = ROOT.TFile.Open(file_path)

    # Check if the file is opened successfully
    if not root_file or root_file.IsZombie():
        print("Error: Could not open the ROOT file.")
        return

    tree_name = "DecayTree"
    tree = root_file.Get(tree_name)
    if tree:
        print(f"\nTree '{tree_name}' has {tree.GetEntries()} entries.")
    else:
        print(f"\nError: Tree '{tree_name}' not found in the ROOT file.")

    branch_list = tree.GetListOfBranches()

    #histograms for TEfficiency class
    hist_tistos = ROOT.TH2F("passed_hist", "Passed Events", len(bins_chosen_branch_1) - 1, bins_chosen_branch_1, len(bins_chosen_branch_2) - 1, bins_chosen_branch_2)
    hist_tis = ROOT.TH2F("all_tis_hist", "All TIS Events", len(bins_chosen_branch_1) - 1, bins_chosen_branch_1, len(bins_chosen_branch_2) - 1, bins_chosen_branch_2)
    hist_tos = ROOT.TH2F("tos_passed_hist", "TOS Passed Events", len(bins_chosen_branch_1) - 1, bins_chosen_branch_1, len(bins_chosen_branch_2) - 1, bins_chosen_branch_2)
    hist_all = ROOT.TH2F("all_hist", "All Events", len(bins_chosen_branch_1) - 1, bins_chosen_branch_1, len(bins_chosen_branch_2) - 1, bins_chosen_branch_2)

    for branch in branch_list:
        branch_name = branch.GetName()

        if branch_name == branchname_1: #The branch that was used for the binning
            chosen_branch_1 = branch
        if branch_name == branchname_2: #The branch that was used for the binning on the second axis
            chosen_branch_2 = branch
            
        if branch_name == "lcplus_Hlt1Global_Dec":
            Hlt1Global_Dec_branch=branch
        if branch_name == "lcplus_L0Global_TIS":
            L0Global_TIS_branch = branch
        if branch_name == "lcplus_L0Global_TOS":
            L0Global_TOS_branch = branch
        if branch_name == "lcplus_L0Global_Dec":
            L0Global_Dec_branch=branch  
        if branch_name == "lcplus_L0HadronDecision_TOS":
            L0HadronDecision_TOS_branch = branch
        if branch_name == "lcplus_Hlt2CharmHadD2HHHDecision_TOS":
            Hlt2CharmHadD2HHHDecision_TOS_branch = branch
        if branch_name == "lcplus_Hlt1Phys_Dec":
           Hlt1Phys_Dec_branch=branch
        

    N_all=0
    N_passed_hlt1=0
    Hlt2CharmHadD2HHHDecision_TOS_sum=0
    N_L0Global_Dec=0
    N_Hlt1Phys_Dec=0
    for i in range(tree.GetEntries()):

        chosen_branch_1.GetEntry(i)
        value_chosen_branch_1 = getattr(tree, chosen_branch_1.GetName())

        chosen_branch_2.GetEntry(i)
        value_chosen_branch_2 = getattr(tree, chosen_branch_2.GetName())

        #check if the values are in the specified range
        if bins_chosen_branch_1[0]<value_chosen_branch_1<bins_chosen_branch_1[-1] and bins_chosen_branch_2[0]<value_chosen_branch_2<bins_chosen_branch_2[-1]       :        
            #Get values:
            L0Global_Dec_branch.GetEntry(i)
            value_L0Global_Dec = getattr(tree, L0Global_Dec_branch.GetName())   
            Hlt1Global_Dec_branch.GetEntry(i)
            value_Hlt1Global_Dec = getattr(tree, Hlt1Global_Dec_branch.GetName()) 
    
            L0Global_TIS_branch.GetEntry(i)
            value_L0Global_TIS = getattr(tree, L0Global_TIS_branch.GetName())

            L0HadronDecision_TOS_branch.GetEntry(i)
            value_L0HadronDecision_TOS = getattr(tree, L0HadronDecision_TOS_branch.GetName()) 

            Hlt2CharmHadD2HHHDecision_TOS_branch.GetEntry(i)
            value_Hlt2CharmHadD2HHHDecision_TOS = getattr(tree, Hlt2CharmHadD2HHHDecision_TOS_branch.GetName())
            
            Hlt1Phys_Dec_branch.GetEntry(i)
            value_Hlt1Phys_Dec = getattr(tree, Hlt1Phys_Dec_branch.GetName())  
            
            #Fill the histograms for L0 efficiency
            if value_L0Global_TIS==1 and value_L0HadronDecision_TOS==1 :
                hist_tistos.Fill(value_chosen_branch_1,value_chosen_branch_2)

            if value_L0Global_TIS==1:
                hist_tis.Fill(value_chosen_branch_1,value_chosen_branch_2)

            if value_L0HadronDecision_TOS==1:
                hist_tos.Fill(value_chosen_branch_1,value_chosen_branch_2)
            hist_all.Fill(value_chosen_branch_1,value_chosen_branch_2)
   
           #####   Hlt1 and Hlt2   ##########################################################################################
            if value_Hlt2CharmHadD2HHHDecision_TOS==1:
                Hlt2CharmHadD2HHHDecision_TOS_sum +=1 
            if value_Hlt1Global_Dec==1:
                N_passed_hlt1+=1
            N_all+=1 
            if value_L0Global_Dec==1:
                N_L0Global_Dec=N_L0Global_Dec+1
            if value_Hlt1Phys_Dec==1:
                N_Hlt1Phys_Dec=N_Hlt1Phys_Dec+1
            ################################################################################################################

    ####### Hlt1 and Hlt2 ###########################################################################################
    Hlt2_efficiency_all=Hlt2CharmHadD2HHHDecision_TOS_sum /N_all
    print("HLT2_efficiency=Hlt2CharmHadD2HHHDecision_TOS_sum /N= ",  Hlt2_efficiency_all)
    Hlt2_efficiency_L0=Hlt2CharmHadD2HHHDecision_TOS_sum/N_L0Global_Dec
    print("HLT2_efficiency=Hlt2CharmHadD2HHHDecision_TOS_sum /N_L0Global_Dec= ",  Hlt2_efficiency_L0)
    Hlt2_efficiency_Hlt1=Hlt2CharmHadD2HHHDecision_TOS_sum/N_Hlt1Phys_Dec
    print("HLT2_efficiency=Hlt2CharmHadD2HHHDecision_TOS_sum /n_Hlt1Phys_Dec= ",  Hlt2_efficiency_Hlt1)

    Hlt1_efficiency_all= N_Hlt1Phys_Dec/N_all
    print("Hlt1_efficiency: N_passed_hlt1/N", Hlt1_efficiency_all)
    Hlt1_efficiency_L0= N_Hlt1Phys_Dec/N_L0Global_Dec
    print("Hlt1_efficiency: N_passed_hlt1/N_L0Global_Dec", Hlt1_efficiency_L0)
    #if you want to save it to the .root file a_named = ROOT.TNamed("variable_a", "a", 1.24) and then a_named.Write()
    
    np.savez("hlt1_hlt2_efficiencies.npz",
     Hlt2_efficiency_all=Hlt2_efficiency_all,
    Hlt2_efficiency_L0 = Hlt2_efficiency_L0,
    Hlt2_efficiency_Hlt1 = Hlt2_efficiency_Hlt1,
    Hlt1_efficiency_all = Hlt1_efficiency_all,
    Hlt1_efficiency_L0 = Hlt1_efficiency_L0)
    ################################################################################################################
    



    #Calculate the efficiencies with TISTOS method and the True efficiency
    #TEfficiency(hist_passed, hist_all)
    
    tistos_efficiency = ROOT.TEfficiency(hist_tistos, hist_tis)
    tistos_efficiency.SetStatisticOption(ROOT.TEfficiency.kBBayesian)  
    true_efficiency= ROOT.TEfficiency(hist_tos, hist_all)
    true_efficiency.SetStatisticOption(ROOT.TEfficiency.kBBayesian)

    

    #Plot histograms 

    #Create histogram showing the difference between TISTOS and true
    hist_ratio_tistos_true = ROOT.TH2F("all_hist", "All Events", len(bins_chosen_branch_1) - 1, bins_chosen_branch_1, len(bins_chosen_branch_2) - 1, bins_chosen_branch_2)
    n_bins_x = tistos_efficiency.GetTotalHistogram().GetNbinsX()
    n_bins_y = tistos_efficiency.GetTotalHistogram().GetNbinsY()
    for i in range(1, n_bins_x + 1):
        for j in range(1, n_bins_y + 1):
            content_tistos_efficiency=tistos_efficiency.GetEfficiency( hist_tistos.GetBin(i,j)) 
            content_true_efficiency = true_efficiency.GetEfficiency( hist_tos.GetBin(i,j)) 
            hist_ratio_tistos_true.SetBinContent(i, j,content_true_efficiency/content_tistos_efficiency )

    # True Efficiency/TISTOS
    canvas_true_tistos = ROOT.TCanvas("hist_true_tistos", "hist_true_tistos", 1600, 1200)
    hist_ratio_tistos_true.SetTitle("True/TISTOS")
    hist_ratio_tistos_true.GetXaxis().SetTitle("Pt")  
    hist_ratio_tistos_true.GetYaxis().SetTitle("Eta")
    hist_ratio_tistos_true.SetStats(0)

    hist_ratio_tistos_true.Draw("colztext")
    canvas_true_tistos.SaveAs("hist_ratio_true_tistos.eps")
    canvas_true_tistos.Close()
    
    # Number of TISTOS events
    canvas_tistos = ROOT.TCanvas("hist_tistos", "hist_tistos", 1600, 1200)
    hist_tistos.SetTitle("TISTOS")
    hist_tistos.GetXaxis().SetTitle("Pt")  
    hist_tistos.GetYaxis().SetTitle("Eta")
    hist_tistos.SetStats(0)
    hist_tistos.Draw("colztext")
    canvas_tistos.SaveAs("hist_number_of_tistos.eps")
    canvas_tistos.Close()
    
    #Number of All events
    canvas_all = ROOT.TCanvas("hist_all", "hist_all", 1600, 1200)
    hist_all.SetTitle("All")
    hist_all.GetXaxis().SetTitle("Pt")  
    hist_all.GetYaxis().SetTitle("Eta")
    hist_all.SetStats(0)
    hist_all.Draw("colztext")
    canvas_all.SaveAs("hist_number_of_all.eps")
    canvas_all.Close()

    #True Efficiency
    canvas_true_efficiency = ROOT.TCanvas("hist_true_efficiency", "hist_true_efficiency", 1600, 1200)
    true_efficiency.SetTitle("True Efficiency")
    true_efficiency.Draw("colztext")
    canvas_true_efficiency.SaveAs("hist_true_efficiency.eps")
    canvas_true_efficiency.Close()

    #TISTOS Efficiency
    canvas_tistos_efficiency = ROOT.TCanvas("hist_tistos_efficiency", "hist_tistos_efficiency", 1600, 1200)
    tistos_efficiency.SetTitle("TISTOS Efficiency")
    tistos_efficiency.Draw("colztext")
    canvas_tistos_efficiency.SaveAs("hist_tistos_efficiency.eps")
    canvas_tistos_efficiency.Close()





    #save the TEfficiency object
    output_file = ROOT.TFile("myfile.root", "recreate")
    tistos_efficiency.Write()
    true_efficiency.Write()
    output_file.Close()

    print("TEfficiency object saved to myfile.root")



if __name__ == "__main__":


    
    particle="Lc"
    polarity="MagDown"
    year="2012"

    file_path = f"/dcache/bfys/achoban/mc_data{year}_{polarity}_{particle}.root"

    # Check if the file already exists
    if os.path.exists(file_path):
        print(f"File '{file_path}' already exists.")
    #If the file does not exist create it
    else:
        mc_data = Imports.getMC(year, polarity, particle)
        output_file = ROOT.TFile(file_path, "RECREATE")
        mc_data.Write()
        output_file.Close()
        print("MC data saved to", file_path)


    branch_info_dict = {
        'pt': {'range_list': [2000, 12000], 'branch_name': 'lcplus_PT', 'num_bins': 9},
        'ETA': {'range_list': [2.2, 4.2], 'branch_name': 'lcplus_ETA', 'num_bins': 5} }
    
    #set the branches you want to use
    branch1="pt"
    branch2="ETA"

    range_list1 =  branch_info_dict[branch1]["range_list"]
    num_bins1 =  branch_info_dict[branch1]['num_bins']
    branch_name1=branch_info_dict[branch1]['branch_name']
    bins_chosen_branch1 = Imports.get_bins(file_path, branch_name1, num_bins1, range_list1)

    range_list2 =  branch_info_dict[branch2]["range_list"]
    num_bins2 =  branch_info_dict[branch2]['num_bins']
    branch_name2=branch_info_dict[branch2]['branch_name']
    bins_chosen_branch2 = Imports.get_bins(file_path, branch_name2, num_bins2, range_list2)
    
    #run the function
    tistos(file_path, bins_chosen_branch1, branch_name1,bins_chosen_branch2, branch_name2)
    
    print(branch_name1," and ", branch_name2, " done ")




    