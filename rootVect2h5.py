import os, sys
import multiprocessing as mp
import copy
import math
from array import array
import pandas as pd
from tools import ptrank, padd
from timeit import default_timer as timer
from ROOT import ROOT, gROOT, TDirectory, TFile, gFile, TBranch, TLeaf, TTree
from ROOT import AddressOf
pwd = os.popen('pwd').read()
pwd = pwd.split('\n')[0]
pl = '.L ' + pwd + '/Objects' + '/Objects_m1.h+'
gROOT.ProcessLine(pl)
from ROOT import JetType, JetTypeSmall, JetTypePFC_fourVect, JetTypePFC_fiveVect, JetTypePFC_sixVect#, JetTypePFCSmall
Js = JetType()

#print sys.argv[1]

path        = '/beegfs/desy/user/hezhiyua/backed/dustData/'+'crab_folder_v2/'#'/home/brian/datas/roottest/'
#inName     = 'VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-500_jetOnly.root'
testOn      = 0
numOfEntriesToScan = 100 #only when testOn = 1
NumOfVecEl  = 6
Npfc        = 40
#scanDepth  = 44
vectName    = 'MatchedCHSJet1' #'Jets'

#adjusted for different oldfile location
args1       = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/'#'.'
versionN_b  = 'TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'
versionN_s  = 'TuneCUETP8M1_13TeV-powheg-pythia8_PRIVATE-MC'
HT          = '50'
fn          = ''
newFileName = fn.replace('.root','_skimed.root')
lola_on     = 0 # 1: prepared for lola
ct_dep      = 0 #1 for ct dependence comparison
cut_on      = 1
life_time   = ['500'] #['0','0p1','0p05','1','5','10','25','50','100','500','1000','2000','5000','10000']
num_of_jets = 1 #4

len_of_lt = len(life_time)

if   ct_dep == 0:
    matchOn = 0
    if   '50'  == HT:
        channel = {'QCD':'QCD_HT50to100_' + versionN_b + '.root'}
    elif '100' == HT:
        channel = {'QCD':'QCD_HT100to200_' + versionN_b + '.root'}
    elif '200' == HT:
        channel = {'QCD':'QCD_HT200to300_' + versionN_b + '.root'}
    elif '300' == HT:
        channel = {'QCD':'QCD_HT300to500_' + versionN_b + '.root'}
elif ct_dep == 1:
    matchOn = 1
    channel = {}
    for lt in life_time:
        channel['ct' + lt] = 'VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-' + lt + '_' + versionN_s + '.root'

# Struct
if   lola_on == 0:
    Jets1 = JetTypeSmall() #for bdt: JetTypeSmall; for lola: JetTypePFC_fourVect
elif lola_on == 1:
    if   NumOfVecEl == 5:
        Jets1 = JetTypePFC_fiveVect() 
    elif NumOfVecEl == 6:
        Jets1 = JetTypePFC_sixVect()

#-------------------------------------
cs            = {}
cs['pt_L']    = 'pt'  + '>' + '15'
cs['eta_L']   = 'eta' + '>' + '-2.4' 
cs['eta_U']   = 'eta' + '<' + '2.4'
cs['matched'] = 'isGenMatched' + '==' + '1'
#-------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------
condition_str_dict = {}
for j in range(num_of_jets):
    #prs = 'Jet_old_dict[' +str(j+1) + '].'
    prs = 'oldTree.Jets[k].' 
    a   = ' and '
    o   = ' or '
    condition_str_dict[j+1] = '(' + prs + cs['pt_L']  + ')' +\
                              a +\
                              '(' + prs + cs['eta_L'] + ')' +\
                              a +\
                              '(' + prs + cs['eta_U'] + ')'
    if matchOn == 1:
        condition_str_dict[j+1] = condition_str_dict[j+1] +\
                                  a +\
                                  '(' + prs + cs['matched']  + ')'


if   cut_on == 1:
    print condition_str_dict[1]
elif cut_on == 0:
    print 'no cut applied~'
#---------------------------------------------------------------------------------------------------------------------------------


if lola_on == 1:
    inName = channel['ct500']#channel['QCD']#''#[for i in channel: channel[i]][0]

    j1Entry  = []
    j1Num    = [] 
    pan      = []

    f1 = TFile( path + inName , "r" )
    t1 = f1.Get('ntuple/tree')

    NumE = t1.GetEntriesFast()
    print NumE
    t1.SetBranchAddress( vectName , AddressOf(Js, 'pt') )

    b1 = t1.GetBranch('PFCandidates')
    nEntries = b1.GetEntries()



    if testOn == 0:
        numOfEntriesToScan = nEntries


    nr = 0
    for entry in t1:
        print '~~~~~~~~~~another entry:' + str(nr)
        b1.GetEntry(nr)
        nr += 1

        #print 'chf:'
        #print Js.chf
        
        E         = b1.FindBranch('PFCandidates.energy')
        PX        = b1.FindBranch('PFCandidates.px')
        PY        = b1.FindBranch('PFCandidates.py')
        PZ        = b1.FindBranch('PFCandidates.pz')
        C         = b1.FindBranch('PFCandidates.isTrack')
        PID       = b1.FindBranch('PFCandidates.pdgId') #pType
        #M        = b1.FindBranch('PFCandidates.mass')
        jetInd    = b1.FindBranch('PFCandidates.jetIndex')
        j1E       = [] 
        j1PX      = []
        j1PY      = []
        j1PZ      = []
        j1C       = []
        j1PID     = []
        j1M       = [] 
        scanDepth = E.GetNdata()

        for num in range(0,scanDepth):
            if jetInd.GetValue(num,1) == 0:  #0,1
                j1Entry.append(nr) 
                #j1Num.append(num)
                j1E.append(E.GetValue(num,1))
                j1PX.append(PX.GetValue(num,1))
                j1PY.append(PY.GetValue(num,1))
                j1PZ.append(PZ.GetValue(num,1))
                j1C.append( int(C.GetValue(num,1)) ) 
                #print C.GetValue(num,1)
                #print E.GetValue(num,1)
                j1PID.append( int(PID.GetValue(num,1)) )
                #j1M.append(M.GetValue(num,1))
            #if num == 40:
            #    break 
        tempE  , _, _ = ptrank( j1PX, j1PY, j1E   , n_pfc=Npfc)
        tempPX , _, _ = ptrank( j1PX, j1PY, j1PX  , n_pfc=Npfc)
        tempPY , _, _ = ptrank( j1PX, j1PY, j1PY  , n_pfc=Npfc)
        tempPZ , _, _ = ptrank( j1PX, j1PY, j1PZ  , n_pfc=Npfc)
        tempC  , _, _ = ptrank( j1PX, j1PY, j1C   , n_pfc=Npfc) 
        tempPID, _, _ = ptrank( j1PX, j1PY, j1PID , n_pfc=Npfc)
        #tempM, _, _ = ptrank( j1PX, j1PY, j1M , n_pfc=Npfc)
        #print tempN
        #print tempPT
        tE   = padd(tempE  ,  0, Npfc)
        tPX  = padd(tempPX ,  0, Npfc)    
        tPY  = padd(tempPY ,  0, Npfc)
        tPZ  = padd(tempPZ ,  0, Npfc)
        tC   = padd(tempC  , -1, Npfc)
        tPID = padd(tempPID, -1, Npfc)
        #tM  = padd(tempM , 0, Npfc)
    
        if NumOfVecEl == 5:
            tt = [4444]*40*5
            tt[40*0:40*1] = tE 
            tt[40*1:40*2] = tPX 
            tt[40*2:40*3] = tPY  
            tt[40*3:40*4] = tPZ 
            tt[40*4:40*5] = tC 
        elif NumOfVecEl == 6:
            tt = [4444]*40*6
            tt[40*0:40*1] = tE 
            tt[40*1:40*2] = tPX 
            tt[40*2:40*3] = tPY  
            tt[40*3:40*4] = tPZ 
            tt[40*4:40*5] = tC 
            tt[40*5:40*6] = tPID 

        pan.append(tt)
        
        if nr == numOfEntriesToScan:
            break     

    print 'num of entries:'
    print nEntries   

    if NumOfVecEl == 5:
        colN = ['E_1','E_2','E_3','E_4','E_5','E_6','E_7','E_8','E_9','E_10','E_11','E_12','E_13','E_14','E_15','E_16','E_17','E_18','E_19','E_20','E_21','E_22','E_23','E_24','E_25','E_26','E_27','E_28','E_29','E_30','E_31','E_32','E_33','E_34','E_35','E_36','E_37','E_38','E_39','E_40','PX_1','PX_2','PX_3','PX_4','PX_5','PX_6','PX_7','PX_8','PX_9','PX_10','PX_11','PX_12','PX_13','PX_14','PX_15','PX_16','PX_17','PX_18','PX_19','PX_20','PX_21','PX_22','PX_23','PX_24','PX_25','PX_26','PX_27','PX_28','PX_29','PX_30','PX_31','PX_32','PX_33','PX_34','PX_35','PX_36','PX_37','PX_38','PX_39','PX_40','PY_1','PY_2','PY_3','PY_4','PY_5','PY_6','PY_7','PY_8','PY_9','PY_10','PY_11','PY_12','PY_13','PY_14','PY_15','PY_16','PY_17','PY_18','PY_19','PY_20','PY_21','PY_22','PY_23','PY_24','PY_25','PY_26','PY_27','PY_28','PY_29','PY_30','PY_31','PY_32','PY_33','PY_34','PY_35','PY_36','PY_37','PY_38','PY_39','PY_40','PZ_1','PZ_2','PZ_3','PZ_4','PZ_5','PZ_6','PZ_7','PZ_8','PZ_9','PZ_10','PZ_11','PZ_12','PZ_13','PZ_14','PZ_15','PZ_16','PZ_17','PZ_18','PZ_19','PZ_20','PZ_21','PZ_22','PZ_23','PZ_24','PZ_25','PZ_26','PZ_27','PZ_28','PZ_29','PZ_30','PZ_31','PZ_32','PZ_33','PZ_34','PZ_35','PZ_36','PZ_37','PZ_38','PZ_39','PZ_40','C_1','C_2','C_3','C_4','C_5','C_6','C_7','C_8','C_9','C_10','C_11','C_12','C_13','C_14','C_15','C_16','C_17','C_18','C_19','C_20','C_21','C_22','C_23','C_24','C_25','C_26','C_27','C_28','C_29','C_30','C_31','C_32','C_33','C_34','C_35','C_36','C_37','C_38','C_39','C_40']
    elif NumOfVecEl == 6:
        colN = ['E_1','E_2','E_3','E_4','E_5','E_6','E_7','E_8','E_9','E_10','E_11','E_12','E_13','E_14','E_15','E_16','E_17','E_18','E_19','E_20','E_21','E_22','E_23','E_24','E_25','E_26','E_27','E_28','E_29','E_30','E_31','E_32','E_33','E_34','E_35','E_36','E_37','E_38','E_39','E_40','PX_1','PX_2','PX_3','PX_4','PX_5','PX_6','PX_7','PX_8','PX_9','PX_10','PX_11','PX_12','PX_13','PX_14','PX_15','PX_16','PX_17','PX_18','PX_19','PX_20','PX_21','PX_22','PX_23','PX_24','PX_25','PX_26','PX_27','PX_28','PX_29','PX_30','PX_31','PX_32','PX_33','PX_34','PX_35','PX_36','PX_37','PX_38','PX_39','PX_40','PY_1','PY_2','PY_3','PY_4','PY_5','PY_6','PY_7','PY_8','PY_9','PY_10','PY_11','PY_12','PY_13','PY_14','PY_15','PY_16','PY_17','PY_18','PY_19','PY_20','PY_21','PY_22','PY_23','PY_24','PY_25','PY_26','PY_27','PY_28','PY_29','PY_30','PY_31','PY_32','PY_33','PY_34','PY_35','PY_36','PY_37','PY_38','PY_39','PY_40','PZ_1','PZ_2','PZ_3','PZ_4','PZ_5','PZ_6','PZ_7','PZ_8','PZ_9','PZ_10','PZ_11','PZ_12','PZ_13','PZ_14','PZ_15','PZ_16','PZ_17','PZ_18','PZ_19','PZ_20','PZ_21','PZ_22','PZ_23','PZ_24','PZ_25','PZ_26','PZ_27','PZ_28','PZ_29','PZ_30','PZ_31','PZ_32','PZ_33','PZ_34','PZ_35','PZ_36','PZ_37','PZ_38','PZ_39','PZ_40','C_1','C_2','C_3','C_4','C_5','C_6','C_7','C_8','C_9','C_10','C_11','C_12','C_13','C_14','C_15','C_16','C_17','C_18','C_19','C_20','C_21','C_22','C_23','C_24','C_25','C_26','C_27','C_28','C_29','C_30','C_31','C_32','C_33','C_34','C_35','C_36','C_37','C_38','C_39','C_40','PID_1','PID_2','PID_3','PID_4','PID_5','PID_6','PID_7','PID_8','PID_9','PID_10','PID_11','PID_12','PID_13','PID_14','PID_15','PID_16','PID_17','PID_18','PID_19','PID_20','PID_21','PID_22','PID_23','PID_24','PID_25','PID_26','PID_27','PID_28','PID_29','PID_30','PID_31','PID_32','PID_33','PID_34','PID_35','PID_36','PID_37','PID_38','PID_39','PID_40']

    jet1 = pd.DataFrame(pan, columns=colN)  







#########################
#                       #
#                       #
#      filling          #
#                       #
#                       #
#                       #
#########################

#-----------------------------------------------------------------------------------------------------------
def skim_c( name , newFileName ):
    numOfEntriesToScan_local = numOfEntriesToScan
    #--------------------------------
    Jet_old_dict = {}
    for j in range(num_of_jets):
        Jet_old_dict[j+1] = JetType()
    #--------------------------------
    oldFile = TFile(name, "READ")
    oldTree = oldFile.Get("ntuple/tree") 
    NofEntries = oldTree.GetEntriesFast()
    #locate and register the Jet branches of the old ttree
    #~~~~~~~~~~~~~~~~~~~~~~to be improved!!!
    """
    for j in range(num_of_jets):
        if 'QCD' in name:
            #oldTree.SetBranchAddress( 'Jets' , AddressOf(Jet_old_dict[j+1], 'pt') )
            #oldTree.SetBranchAddress( 'MatchedCHSJet' + str(j+1) , AddressOf(Jet_old_dict[j+1], 'pt') )
        elif 'ctauS' in name:
            #oldTree.SetBranchAddress( 'MatchedCHSJet' + str(j+1) , AddressOf(Jet_old_dict[j+1], 'pt') )
            #oldTree.SetBranchAddress( 'Jets' , AddressOf(Jet_old_dict[j+1], 'pt') )
    """ 


    print 'skimming file',oldFile.GetName(),'\tevents =',oldTree.GetEntries(),'\tweight =',oldTree.GetWeight()
    print 'filename:', name
    newFile = TFile('Skim/' + newFileName, "RECREATE")
    newFile.cd()
    newTree = TTree("tree44", "tree44")

    if   lola_on == 0:
        newTree.Branch( 'Jet1s', Jets1, 'pt/F:eta/F:phi/F:mass/F:energy/F:cHadE/F:nHadE/F:cHadEFrac/F:nHadEFrac/F:nEmE/F:nEmEFrac/F:cEmE/F:cEmEFrac/F:cmuE/F:cmuEFrac/F:muE/F:muEFrac/F:eleE/F:eleEFrac/F:eleMulti/F:photonE/F:photonEFrac/F:photonMulti/F:cHadMulti/F:npr/F:cMulti/F:nMulti/F:FracCal/F' )
        if testOn == 0:
            numOfEntriesToScan_local = oldTree.GetEntriesFast()
    elif lola_on == 1:
        if NumOfVecEl == 5:
            newTree.Branch( 'Jet1s', Jets1, 'pfc1_energy/F:pfc1_px/F:pfc1_py/F:pfc1_pz/F:pfc1_ifTrack/I:pfc2_energy/F:pfc2_px/F:pfc2_py/F:pfc2_pz/F:pfc2_ifTrack/I:pfc3_energy/F:pfc3_px/F:pfc3_py/F:pfc3_pz/F:pfc3_ifTrack/I:pfc4_energy/F:pfc4_px/F:pfc4_py/F:pfc4_pz/F:pfc4_ifTrack/I:pfc5_energy/F:pfc5_px/F:pfc5_py/F:pfc5_pz/F:pfc5_ifTrack/I:pfc6_energy/F:pfc6_px/F:pfc6_py/F:pfc6_pz/F:pfc6_ifTrack/I:pfc7_energy/F:pfc7_px/F:pfc7_py/F:pfc7_pz/F:pfc7_ifTrack/I:pfc8_energy/F:pfc8_px/F:pfc8_py/F:pfc8_pz/F:pfc8_ifTrack/I:pfc9_energy/F:pfc9_px/F:pfc9_py/F:pfc9_pz/F:pfc9_ifTrack/I:pfc10_energy/F:pfc10_px/F:pfc10_py/F:pfc10_pz/F:pfc10_ifTrack/I:pfc11_energy/F:pfc11_px/F:pfc11_py/F:pfc11_pz/F:pfc11_ifTrack/I:pfc12_energy/F:pfc12_px/F:pfc12_py/F:pfc12_pz/F:pfc12_ifTrack/I:pfc13_energy/F:pfc13_px/F:pfc13_py/F:pfc13_pz/F:pfc13_ifTrack/I:pfc14_energy/F:pfc14_px/F:pfc14_py/F:pfc14_pz/F:pfc14_ifTrack/I:pfc15_energy/F:pfc15_px/F:pfc15_py/F:pfc15_pz/F:pfc15_ifTrack/I:pfc16_energy/F:pfc16_px/F:pfc16_py/F:pfc16_pz/F:pfc16_ifTrack/I:pfc17_energy/F:pfc17_px/F:pfc17_py/F:pfc17_pz/F:pfc17_ifTrack/I:pfc18_energy/F:pfc18_px/F:pfc18_py/F:pfc18_pz/F:pfc18_ifTrack/I:pfc19_energy/F:pfc19_px/F:pfc19_py/F:pfc19_pz/F:pfc19_ifTrack/I:pfc20_energy/F:pfc20_px/F:pfc20_py/F:pfc20_pz/F:pfc20_ifTrack/I:pfc21_energy/F:pfc21_px/F:pfc21_py/F:pfc21_pz/F:pfc21_ifTrack/I:pfc22_energy/F:pfc22_px/F:pfc22_py/F:pfc22_pz/F:pfc22_ifTrack/I:pfc23_energy/F:pfc23_px/F:pfc23_py/F:pfc23_pz/F:pfc23_ifTrack/I:pfc24_energy/F:pfc24_px/F:pfc24_py/F:pfc24_pz/F:pfc24_ifTrack/I:pfc25_energy/F:pfc25_px/F:pfc25_py/F:pfc25_pz/F:pfc25_ifTrack/I:pfc26_energy/F:pfc26_px/F:pfc26_py/F:pfc26_pz/F:pfc26_ifTrack/I:pfc27_energy/F:pfc27_px/F:pfc27_py/F:pfc27_pz/F:pfc27_ifTrack/I:pfc28_energy/F:pfc28_px/F:pfc28_py/F:pfc28_pz/F:pfc28_ifTrack/I:pfc29_energy/F:pfc29_px/F:pfc29_py/F:pfc29_pz/F:pfc29_ifTrack/I:pfc30_energy/F:pfc30_px/F:pfc30_py/F:pfc30_pz/F:pfc30_ifTrack/I:pfc31_energy/F:pfc31_px/F:pfc31_py/F:pfc31_pz/F:pfc31_ifTrack/I:pfc32_energy/F:pfc32_px/F:pfc32_py/F:pfc32_pz/F:pfc32_ifTrack/I:pfc33_energy/F:pfc33_px/F:pfc33_py/F:pfc33_pz/F:pfc33_ifTrack/I:pfc34_energy/F:pfc34_px/F:pfc34_py/F:pfc34_pz/F:pfc34_ifTrack/I:pfc35_energy/F:pfc35_px/F:pfc35_py/F:pfc35_pz/F:pfc35_ifTrack/I:pfc36_energy/F:pfc36_px/F:pfc36_py/F:pfc36_pz/F:pfc36_ifTrack/I:pfc37_energy/F:pfc37_px/F:pfc37_py/F:pfc37_pz/F:pfc37_ifTrack/I:pfc38_energy/F:pfc38_px/F:pfc38_py/F:pfc38_pz/F:pfc38_ifTrack/I:pfc39_energy/F:pfc39_px/F:pfc39_py/F:pfc39_pz/F:pfc39_ifTrack/I:pfc40_energy/F:pfc40_px/F:pfc40_py/F:pfc40_pz/F:pfc40_ifTrack/I' )
            #newTree.Branch( 'Jet1s', Jets1, 'pfc1_energy/F:pfc1_px/F:pfc1_py/F:pfc1_pz/F:pfc2_energy/F:pfc2_px/F:pfc2_py/F:pfc2_pz/F:pfc3_energy/F:pfc3_px/F:pfc3_py/F:pfc3_pz/F:pfc4_energy/F:pfc4_px/F:pfc4_py/F:pfc4_pz/F:pfc5_energy/F:pfc5_px/F:pfc5_py/F:pfc5_pz/F:pfc6_energy/F:pfc6_px/F:pfc6_py/F:pfc6_pz/F:pfc7_energy/F:pfc7_px/F:pfc7_py/F:pfc7_pz/F:pfc8_energy/F:pfc8_px/F:pfc8_py/F:pfc8_pz/F:pfc9_energy/F:pfc9_px/F:pfc9_py/F:pfc9_pz/F:pfc10_energy/F:pfc10_px/F:pfc10_py/F:pfc10_pz/F:pfc11_energy/F:pfc11_px/F:pfc11_py/F:pfc11_pz/F:pfc12_energy/F:pfc12_px/F:pfc12_py/F:pfc12_pz/F:pfc13_energy/F:pfc13_px/F:pfc13_py/F:pfc13_pz/F:pfc14_energy/F:pfc14_px/F:pfc14_py/F:pfc14_pz/F:pfc15_energy/F:pfc15_px/F:pfc15_py/F:pfc15_pz/F:pfc16_energy/F:pfc16_px/F:pfc16_py/F:pfc16_pz/F:pfc17_energy/F:pfc17_px/F:pfc17_py/F:pfc17_pz/F:pfc18_energy/F:pfc18_px/F:pfc18_py/F:pfc18_pz/F:pfc19_energy/F:pfc19_px/F:pfc19_py/F:pfc19_pz/F:pfc20_energy/F:pfc20_px/F:pfc20_py/F:pfc20_pz/F:pfc21_energy/F:pfc21_px/F:pfc21_py/F:pfc21_pz/F:pfc22_energy/F:pfc22_px/F:pfc22_py/F:pfc22_pz/F:pfc23_energy/F:pfc23_px/F:pfc23_py/F:pfc23_pz/F:pfc24_energy/F:pfc24_px/F:pfc24_py/F:pfc24_pz/F:pfc25_energy/F:pfc25_px/F:pfc25_py/F:pfc25_pz/F:pfc26_energy/F:pfc26_px/F:pfc26_py/F:pfc26_pz/F:pfc27_energy/F:pfc27_px/F:pfc27_py/F:pfc27_pz/F:pfc28_energy/F:pfc28_px/F:pfc28_py/F:pfc28_pz/F:pfc29_energy/F:pfc29_px/F:pfc29_py/F:pfc29_pz/F:pfc30_energy/F:pfc30_px/F:pfc30_py/F:pfc30_pz/F:pfc31_energy/F:pfc31_px/F:pfc31_py/F:pfc31_pz/F:pfc32_energy/F:pfc32_px/F:pfc32_py/F:pfc32_pz/F:pfc33_energy/F:pfc33_px/F:pfc33_py/F:pfc33_pz/F:pfc34_energy/F:pfc34_px/F:pfc34_py/F:pfc34_pz/F:pfc35_energy/F:pfc35_px/F:pfc35_py/F:pfc35_pz/F:pfc36_energy/F:pfc36_px/F:pfc36_py/F:pfc36_pz/F:pfc37_energy/F:pfc37_px/F:pfc37_py/F:pfc37_pz/F:pfc38_energy/F:pfc38_px/F:pfc38_py/F:pfc38_pz/F:pfc39_energy/F:pfc39_px/F:pfc39_py/F:pfc39_pz/F:pfc40_energy/F:pfc40_px/F:pfc40_py/F:pfc40_pz/F' )
            if testOn == 0:
                numOfEntriesToScan_local = oldTree.GetEntriesFast()
        elif NumOfVecEl == 6:
            newTree.Branch( 'Jet1s', Jets1, 'pfc1_energy/F:pfc1_px/F:pfc1_py/F:pfc1_pz/F:pfc1_ifTrack/I:pfc1_pType/I:pfc2_energy/F:pfc2_px/F:pfc2_py/F:pfc2_pz/F:pfc2_ifTrack/I:pfc2_pType/I:pfc3_energy/F:pfc3_px/F:pfc3_py/F:pfc3_pz/F:pfc3_ifTrack/I:pfc3_pType/I:pfc4_energy/F:pfc4_px/F:pfc4_py/F:pfc4_pz/F:pfc4_ifTrack/I:pfc4_pType/I:pfc5_energy/F:pfc5_px/F:pfc5_py/F:pfc5_pz/F:pfc5_ifTrack/I:pfc5_pType/I:pfc6_energy/F:pfc6_px/F:pfc6_py/F:pfc6_pz/F:pfc6_ifTrack/I:pfc6_pType/I:pfc7_energy/F:pfc7_px/F:pfc7_py/F:pfc7_pz/F:pfc7_ifTrack/I:pfc7_pType/I:pfc8_energy/F:pfc8_px/F:pfc8_py/F:pfc8_pz/F:pfc8_ifTrack/I:pfc8_pType/I:pfc9_energy/F:pfc9_px/F:pfc9_py/F:pfc9_pz/F:pfc9_ifTrack/I:pfc9_pType/I:pfc10_energy/F:pfc10_px/F:pfc10_py/F:pfc10_pz/F:pfc10_ifTrack/I:pfc10_pType/I:pfc11_energy/F:pfc11_px/F:pfc11_py/F:pfc11_pz/F:pfc11_ifTrack/I:pfc11_pType/I:pfc12_energy/F:pfc12_px/F:pfc12_py/F:pfc12_pz/F:pfc12_ifTrack/I:pfc12_pType/I:pfc13_energy/F:pfc13_px/F:pfc13_py/F:pfc13_pz/F:pfc13_ifTrack/I:pfc13_pType/I:pfc14_energy/F:pfc14_px/F:pfc14_py/F:pfc14_pz/F:pfc14_ifTrack/I:pfc14_pType/I:pfc15_energy/F:pfc15_px/F:pfc15_py/F:pfc15_pz/F:pfc15_ifTrack/I:pfc15_pType/I:pfc16_energy/F:pfc16_px/F:pfc16_py/F:pfc16_pz/F:pfc16_ifTrack/I:pfc16_pType/I:pfc17_energy/F:pfc17_px/F:pfc17_py/F:pfc17_pz/F:pfc17_ifTrack/I:pfc17_pType/I:pfc18_energy/F:pfc18_px/F:pfc18_py/F:pfc18_pz/F:pfc18_ifTrack/I:pfc18_pType/I:pfc19_energy/F:pfc19_px/F:pfc19_py/F:pfc19_pz/F:pfc19_ifTrack/I:pfc19_pType/I:pfc20_energy/F:pfc20_px/F:pfc20_py/F:pfc20_pz/F:pfc20_ifTrack/I:pfc20_pType/I:pfc21_energy/F:pfc21_px/F:pfc21_py/F:pfc21_pz/F:pfc21_ifTrack/I:pfc21_pType/I:pfc22_energy/F:pfc22_px/F:pfc22_py/F:pfc22_pz/F:pfc22_ifTrack/I:pfc22_pType/I:pfc23_energy/F:pfc23_px/F:pfc23_py/F:pfc23_pz/F:pfc23_ifTrack/I:pfc23_pType/I:pfc24_energy/F:pfc24_px/F:pfc24_py/F:pfc24_pz/F:pfc24_ifTrack/I:pfc24_pType/I:pfc25_energy/F:pfc25_px/F:pfc25_py/F:pfc25_pz/F:pfc25_ifTrack/I:pfc25_pType/I:pfc26_energy/F:pfc26_px/F:pfc26_py/F:pfc26_pz/F:pfc26_ifTrack/I:pfc26_pType/I:pfc27_energy/F:pfc27_px/F:pfc27_py/F:pfc27_pz/F:pfc27_ifTrack/I:pfc27_pType/I:pfc28_energy/F:pfc28_px/F:pfc28_py/F:pfc28_pz/F:pfc28_ifTrack/I:pfc28_pType/I:pfc29_energy/F:pfc29_px/F:pfc29_py/F:pfc29_pz/F:pfc29_ifTrack/I:pfc29_pType/I:pfc30_energy/F:pfc30_px/F:pfc30_py/F:pfc30_pz/F:pfc30_ifTrack/I:pfc30_pType/I:pfc31_energy/F:pfc31_px/F:pfc31_py/F:pfc31_pz/F:pfc31_ifTrack/I:pfc31_pType/I:pfc32_energy/F:pfc32_px/F:pfc32_py/F:pfc32_pz/F:pfc32_ifTrack/I:pfc32_pType/I:pfc33_energy/F:pfc33_px/F:pfc33_py/F:pfc33_pz/F:pfc33_ifTrack/I:pfc33_pType/I:pfc34_energy/F:pfc34_px/F:pfc34_py/F:pfc34_pz/F:pfc34_ifTrack/I:pfc34_pType/I:pfc35_energy/F:pfc35_px/F:pfc35_py/F:pfc35_pz/F:pfc35_ifTrack/I:pfc35_pType/I:pfc36_energy/F:pfc36_px/F:pfc36_py/F:pfc36_pz/F:pfc36_ifTrack/I:pfc36_pType/I:pfc37_energy/F:pfc37_px/F:pfc37_py/F:pfc37_pz/F:pfc37_ifTrack/I:pfc37_pType/I:pfc38_energy/F:pfc38_px/F:pfc38_py/F:pfc38_pz/F:pfc38_ifTrack/I:pfc38_pType/I:pfc39_energy/F:pfc39_px/F:pfc39_py/F:pfc39_pz/F:pfc39_ifTrack/I:pfc39_pType/I:pfc40_energy/F:pfc40_px/F:pfc40_py/F:pfc40_pz/F:pfc40_ifTrack/I:pfc40_pType/I' )
            if testOn == 0:
                numOfEntriesToScan_local = oldTree.GetEntriesFast()
    # this attribute list must exactly match (the order of) the features in the header file!!!! 

    ti = 80000
    #theweight = oldTree.GetWeight() 
    for i in range(  0 , numOfEntriesToScan_local  ):    
        if      i == 0:
            start = timer()
        elif i%ti == 2:
            start = timer()
        
        oldTree.GetEntry(i)
        # selections
        # Trigger
        for j in range(num_of_jets):
            #if cut_on == 0:
            #    condition_str_dict[j+1] = '1'
            #if eval( condition_str_dict[j+1] ):
            if 1:    
                if lola_on == 0:        
                    for k in xrange( oldTree.Jets.size() ):
                        #print oldTree.Jets.size() 
                        if k == 1:
                            if cut_on == 0:
                                condition_str_dict[j+1] = '1'
                            if eval( condition_str_dict[j+1] ):
                                Jets1.pt             = oldTree.Jets[k].pt
                                Jets1.eta            = oldTree.Jets[k].eta
                                Jets1.phi            = oldTree.Jets[k].phi
                                Jets1.mass           = oldTree.Jets[k].mass
                                Jets1.energy         = oldTree.Jets[k].energy

                                Jets1.cHadE          = oldTree.Jets[k].cHadE
                                Jets1.nHadE          = oldTree.Jets[k].nHadE
                                Jets1.cHadEFrac      = oldTree.Jets[k].cHadEFrac
                                Jets1.nHadEFrac      = oldTree.Jets[k].nHadEFrac
                                Jets1.nEmE           = oldTree.Jets[k].nEmE
                                Jets1.nEmEFrac       = oldTree.Jets[k].nEmEFrac
                                Jets1.cEmE           = oldTree.Jets[k].cEmE     
                                Jets1.cEmEFrac       = oldTree.Jets[k].cEmEFrac                    
                                Jets1.cmuE           = oldTree.Jets[k].cmuE
                                Jets1.cmuEFrac       = oldTree.Jets[k].cmuEFrac
                                Jets1.muE            = oldTree.Jets[k].muE     
                                Jets1.muEFrac        = oldTree.Jets[k].muEFrac
                                Jets1.eleE           = oldTree.Jets[k].eleE
                                Jets1.eleEFrac       = oldTree.Jets[k].eleEFrac
                                Jets1.eleMulti       = oldTree.Jets[k].eleMulti  
                                Jets1.photonE        = oldTree.Jets[k].photonE                   
                                Jets1.photonEFrac    = oldTree.Jets[k].photonEFrac
                                Jets1.photonMulti    = oldTree.Jets[k].photonMulti     
                                Jets1.cHadMulti      = oldTree.Jets[k].cHadMulti
                                Jets1.npr            = oldTree.Jets[k].npr
                                Jets1.cMulti         = oldTree.Jets[k].cMulti
                                Jets1.nMulti         = oldTree.Jets[k].nMulti

                                fraccal = oldTree.Jets[k].FracCal  
                                if fraccal <= 0:
                                    Jets1.FracCal    = 0.
                                elif fraccal > 400:
                                    Jets1.FracCal    = 400.
                                else:
                                    Jets1.FracCal    = fraccal
    
                        else: pass    
                        

                    """
                    Jets1.pt             = Jet_old_dict[j+1].pt
                    Jets1.eta            = Jet_old_dict[j+1].eta
                    Jets1.mass           = Jet_old_dict[j+1].mass
                                
                    Jets1.cHadE          = Jet_old_dict[j+1].cHadE
                    Jets1.nHadE          = Jet_old_dict[j+1].nHadE
                    Jets1.cHadEFrac      = Jet_old_dict[j+1].cHadEFrac
                    Jets1.nHadEFrac      = Jet_old_dict[j+1].nHadEFrac
                    Jets1.nEmE           = Jet_old_dict[j+1].nEmE
                    Jets1.nEmEFrac       = Jet_old_dict[j+1].nEmEFrac
                    Jets1.cEmE           = Jet_old_dict[j+1].cEmE     
                    Jets1.cEmEFrac       = Jet_old_dict[j+1].cEmEFrac                    
                    Jets1.cmuE           = Jet_old_dict[j+1].cmuE
                    Jets1.cmuEFrac       = Jet_old_dict[j+1].cmuEFrac
                    Jets1.muE            = Jet_old_dict[j+1].muE     
                    Jets1.muEFrac        = Jet_old_dict[j+1].muEFrac
                    Jets1.eleE           = Jet_old_dict[j+1].eleE
                    Jets1.eleEFrac       = Jet_old_dict[j+1].eleEFrac
                    Jets1.eleMulti       = Jet_old_dict[j+1].eleMulti  
                    Jets1.photonE        = Jet_old_dict[j+1].photonE                   
                    Jets1.photonEFrac    = Jet_old_dict[j+1].photonEFrac
                    Jets1.photonMulti    = Jet_old_dict[j+1].photonMulti     
                    Jets1.cHadMulti      = Jet_old_dict[j+1].cHadMulti
                    Jets1.npr            = Jet_old_dict[j+1].npr
                    Jets1.cMulti         = Jet_old_dict[j+1].cMulti
                    Jets1.nMulti         = Jet_old_dict[j+1].nMulti

                    Jets1.FracCal        = Jet_old_dict[j+1].FracCal
                    """
                    
                    
                elif lola_on == 1:
                    if NumOfVecEl == 5:
                        Jets1.pfc1_energy    = jet1['E_1'][i]
                        Jets1.pfc1_energy    = jet1['E_1'][i]
                        Jets1.pfc1_px        = jet1['PX_1'][i]
                        Jets1.pfc1_py        = jet1['PY_1'][i]
                        Jets1.pfc1_pz        = jet1['PZ_1'][i]
                        Jets1.pfc1_ifTrack   = jet1['C_1'][i]
                        Jets1.pfc2_energy    = jet1['E_2'][i]
                        Jets1.pfc2_px        = jet1['PX_2'][i]
                        Jets1.pfc2_py        = jet1['PY_2'][i]
                        Jets1.pfc2_pz        = jet1['PZ_2'][i]
                        Jets1.pfc2_ifTrack   = jet1['C_2'][i]
                        Jets1.pfc3_energy    = jet1['E_3'][i]
                        Jets1.pfc3_px        = jet1['PX_3'][i]
                        Jets1.pfc3_py        = jet1['PY_3'][i]
                        Jets1.pfc3_pz        = jet1['PZ_3'][i]
                        Jets1.pfc3_ifTrack   = jet1['C_3'][i]
                        Jets1.pfc4_energy    = jet1['E_4'][i]
                        Jets1.pfc4_px        = jet1['PX_4'][i]
                        Jets1.pfc4_py        = jet1['PY_4'][i]
                        Jets1.pfc4_pz        = jet1['PZ_4'][i]
                        Jets1.pfc4_ifTrack   = jet1['C_4'][i]
                        Jets1.pfc5_energy    = jet1['E_5'][i]
                        Jets1.pfc5_px        = jet1['PX_5'][i]
                        Jets1.pfc5_py        = jet1['PY_5'][i]
                        Jets1.pfc5_pz        = jet1['PZ_5'][i]
                        Jets1.pfc5_ifTrack   = jet1['C_5'][i]
                        Jets1.pfc6_energy    = jet1['E_6'][i]
                        Jets1.pfc6_px        = jet1['PX_6'][i]
                        Jets1.pfc6_py        = jet1['PY_6'][i]
                        Jets1.pfc6_pz        = jet1['PZ_6'][i]
                        Jets1.pfc6_ifTrack   = jet1['C_6'][i]
                        Jets1.pfc7_energy    = jet1['E_7'][i]
                        Jets1.pfc7_px        = jet1['PX_7'][i]
                        Jets1.pfc7_py        = jet1['PY_7'][i]
                        Jets1.pfc7_pz        = jet1['PZ_7'][i]
                        Jets1.pfc7_ifTrack   = jet1['C_7'][i]
                        Jets1.pfc8_energy    = jet1['E_8'][i]
                        Jets1.pfc8_px        = jet1['PX_8'][i]
                        Jets1.pfc8_py        = jet1['PY_8'][i]
                        Jets1.pfc8_pz        = jet1['PZ_8'][i]
                        Jets1.pfc8_ifTrack   = jet1['C_8'][i]
                        Jets1.pfc9_energy    = jet1['E_9'][i]
                        Jets1.pfc9_px        = jet1['PX_9'][i]
                        Jets1.pfc9_py        = jet1['PY_9'][i]
                        Jets1.pfc9_pz        = jet1['PZ_9'][i]
                        Jets1.pfc9_ifTrack   = jet1['C_9'][i]
                        Jets1.pfc10_energy    = jet1['E_10'][i]
                        Jets1.pfc10_px        = jet1['PX_10'][i]
                        Jets1.pfc10_py        = jet1['PY_10'][i]
                        Jets1.pfc10_pz        = jet1['PZ_10'][i]
                        Jets1.pfc10_ifTrack   = jet1['C_10'][i]
                        Jets1.pfc11_energy    = jet1['E_11'][i]
                        Jets1.pfc11_px        = jet1['PX_11'][i]
                        Jets1.pfc11_py        = jet1['PY_11'][i]
                        Jets1.pfc11_pz        = jet1['PZ_11'][i]
                        Jets1.pfc11_ifTrack   = jet1['C_11'][i]
                        Jets1.pfc12_energy    = jet1['E_12'][i]
                        Jets1.pfc12_px        = jet1['PX_12'][i]
                        Jets1.pfc12_py        = jet1['PY_12'][i]
                        Jets1.pfc12_pz        = jet1['PZ_12'][i]
                        Jets1.pfc12_ifTrack   = jet1['C_12'][i]
                        Jets1.pfc13_energy    = jet1['E_13'][i]
                        Jets1.pfc13_px        = jet1['PX_13'][i]
                        Jets1.pfc13_py        = jet1['PY_13'][i]
                        Jets1.pfc13_pz        = jet1['PZ_13'][i]
                        Jets1.pfc13_ifTrack   = jet1['C_13'][i]
                        Jets1.pfc14_energy    = jet1['E_14'][i]
                        Jets1.pfc14_px        = jet1['PX_14'][i]
                        Jets1.pfc14_py        = jet1['PY_14'][i]
                        Jets1.pfc14_pz        = jet1['PZ_14'][i]
                        Jets1.pfc14_ifTrack   = jet1['C_14'][i]
                        Jets1.pfc15_energy    = jet1['E_15'][i]
                        Jets1.pfc15_px        = jet1['PX_15'][i]
                        Jets1.pfc15_py        = jet1['PY_15'][i]
                        Jets1.pfc15_pz        = jet1['PZ_15'][i]
                        Jets1.pfc15_ifTrack   = jet1['C_15'][i]
                        Jets1.pfc16_energy    = jet1['E_16'][i]
                        Jets1.pfc16_px        = jet1['PX_16'][i]
                        Jets1.pfc16_py        = jet1['PY_16'][i]
                        Jets1.pfc16_pz        = jet1['PZ_16'][i]
                        Jets1.pfc16_ifTrack   = jet1['C_16'][i]
                        Jets1.pfc17_energy    = jet1['E_17'][i]
                        Jets1.pfc17_px        = jet1['PX_17'][i]
                        Jets1.pfc17_py        = jet1['PY_17'][i]
                        Jets1.pfc17_pz        = jet1['PZ_17'][i]
                        Jets1.pfc17_ifTrack   = jet1['C_17'][i]
                        Jets1.pfc18_energy    = jet1['E_18'][i]
                        Jets1.pfc18_px        = jet1['PX_18'][i]
                        Jets1.pfc18_py        = jet1['PY_18'][i]
                        Jets1.pfc18_pz        = jet1['PZ_18'][i]
                        Jets1.pfc18_ifTrack   = jet1['C_18'][i]
                        Jets1.pfc19_energy    = jet1['E_19'][i]
                        Jets1.pfc19_px        = jet1['PX_19'][i]
                        Jets1.pfc19_py        = jet1['PY_19'][i]
                        Jets1.pfc19_pz        = jet1['PZ_19'][i]
                        Jets1.pfc19_ifTrack   = jet1['C_19'][i]
                        Jets1.pfc20_energy    = jet1['E_20'][i]
                        Jets1.pfc20_px        = jet1['PX_20'][i]
                        Jets1.pfc20_py        = jet1['PY_20'][i]
                        Jets1.pfc20_pz        = jet1['PZ_20'][i]
                        Jets1.pfc20_ifTrack   = jet1['C_20'][i]
                        Jets1.pfc21_energy    = jet1['E_21'][i]
                        Jets1.pfc21_px        = jet1['PX_21'][i]
                        Jets1.pfc21_py        = jet1['PY_21'][i]
                        Jets1.pfc21_pz        = jet1['PZ_21'][i]
                        Jets1.pfc21_ifTrack   = jet1['C_21'][i]
                        Jets1.pfc22_energy    = jet1['E_22'][i]
                        Jets1.pfc22_px        = jet1['PX_22'][i]
                        Jets1.pfc22_py        = jet1['PY_22'][i]
                        Jets1.pfc22_pz        = jet1['PZ_22'][i]
                        Jets1.pfc22_ifTrack   = jet1['C_22'][i]
                        Jets1.pfc23_energy    = jet1['E_23'][i]
                        Jets1.pfc23_px        = jet1['PX_23'][i]
                        Jets1.pfc23_py        = jet1['PY_23'][i]
                        Jets1.pfc23_pz        = jet1['PZ_23'][i]
                        Jets1.pfc23_ifTrack   = jet1['C_23'][i]
                        Jets1.pfc24_energy    = jet1['E_24'][i]
                        Jets1.pfc24_px        = jet1['PX_24'][i]
                        Jets1.pfc24_py        = jet1['PY_24'][i]
                        Jets1.pfc24_pz        = jet1['PZ_24'][i]
                        Jets1.pfc24_ifTrack   = jet1['C_24'][i]
                        Jets1.pfc25_energy    = jet1['E_25'][i]
                        Jets1.pfc25_px        = jet1['PX_25'][i]
                        Jets1.pfc25_py        = jet1['PY_25'][i]
                        Jets1.pfc25_pz        = jet1['PZ_25'][i]
                        Jets1.pfc25_ifTrack   = jet1['C_25'][i]
                        Jets1.pfc26_energy    = jet1['E_26'][i]
                        Jets1.pfc26_px        = jet1['PX_26'][i]
                        Jets1.pfc26_py        = jet1['PY_26'][i]
                        Jets1.pfc26_pz        = jet1['PZ_26'][i]
                        Jets1.pfc26_ifTrack   = jet1['C_26'][i]
                        Jets1.pfc27_energy    = jet1['E_27'][i]
                        Jets1.pfc27_px        = jet1['PX_27'][i]
                        Jets1.pfc27_py        = jet1['PY_27'][i]
                        Jets1.pfc27_pz        = jet1['PZ_27'][i]
                        Jets1.pfc27_ifTrack   = jet1['C_27'][i]
                        Jets1.pfc28_energy    = jet1['E_28'][i]
                        Jets1.pfc28_px        = jet1['PX_28'][i]
                        Jets1.pfc28_py        = jet1['PY_28'][i]
                        Jets1.pfc28_pz        = jet1['PZ_28'][i]
                        Jets1.pfc28_ifTrack   = jet1['C_28'][i]
                        Jets1.pfc29_energy    = jet1['E_29'][i]
                        Jets1.pfc29_px        = jet1['PX_29'][i]
                        Jets1.pfc29_py        = jet1['PY_29'][i]
                        Jets1.pfc29_pz        = jet1['PZ_29'][i]
                        Jets1.pfc29_ifTrack   = jet1['C_29'][i]
                        Jets1.pfc30_energy    = jet1['E_30'][i]
                        Jets1.pfc30_px        = jet1['PX_30'][i]
                        Jets1.pfc30_py        = jet1['PY_30'][i]
                        Jets1.pfc30_pz        = jet1['PZ_30'][i]
                        Jets1.pfc30_ifTrack   = jet1['C_30'][i]
                        Jets1.pfc31_energy    = jet1['E_31'][i]
                        Jets1.pfc31_px        = jet1['PX_31'][i]
                        Jets1.pfc31_py        = jet1['PY_31'][i]
                        Jets1.pfc31_pz        = jet1['PZ_31'][i]
                        Jets1.pfc31_ifTrack   = jet1['C_31'][i]
                        Jets1.pfc32_energy    = jet1['E_32'][i]
                        Jets1.pfc32_px        = jet1['PX_32'][i]
                        Jets1.pfc32_py        = jet1['PY_32'][i]
                        Jets1.pfc32_pz        = jet1['PZ_32'][i]
                        Jets1.pfc32_ifTrack   = jet1['C_32'][i]
                        Jets1.pfc33_energy    = jet1['E_33'][i]
                        Jets1.pfc33_px        = jet1['PX_33'][i]
                        Jets1.pfc33_py        = jet1['PY_33'][i]
                        Jets1.pfc33_pz        = jet1['PZ_33'][i]
                        Jets1.pfc33_ifTrack   = jet1['C_33'][i]
                        Jets1.pfc34_energy    = jet1['E_34'][i]
                        Jets1.pfc34_px        = jet1['PX_34'][i]
                        Jets1.pfc34_py        = jet1['PY_34'][i]
                        Jets1.pfc34_pz        = jet1['PZ_34'][i]
                        Jets1.pfc34_ifTrack   = jet1['C_34'][i]
                        Jets1.pfc35_energy    = jet1['E_35'][i]
                        Jets1.pfc35_px        = jet1['PX_35'][i]
                        Jets1.pfc35_py        = jet1['PY_35'][i]
                        Jets1.pfc35_pz        = jet1['PZ_35'][i]
                        Jets1.pfc35_ifTrack   = jet1['C_35'][i]
                        Jets1.pfc36_energy    = jet1['E_36'][i]
                        Jets1.pfc36_px        = jet1['PX_36'][i]
                        Jets1.pfc36_py        = jet1['PY_36'][i]
                        Jets1.pfc36_pz        = jet1['PZ_36'][i]
                        Jets1.pfc36_ifTrack   = jet1['C_36'][i]
                        Jets1.pfc37_energy    = jet1['E_37'][i]
                        Jets1.pfc37_px        = jet1['PX_37'][i]
                        Jets1.pfc37_py        = jet1['PY_37'][i]
                        Jets1.pfc37_pz        = jet1['PZ_37'][i]
                        Jets1.pfc37_ifTrack   = jet1['C_37'][i]
                        Jets1.pfc38_energy    = jet1['E_38'][i]
                        Jets1.pfc38_px        = jet1['PX_38'][i]
                        Jets1.pfc38_py        = jet1['PY_38'][i]
                        Jets1.pfc38_pz        = jet1['PZ_38'][i]
                        Jets1.pfc38_ifTrack   = jet1['C_38'][i]
                        Jets1.pfc39_energy    = jet1['E_39'][i]
                        Jets1.pfc39_px        = jet1['PX_39'][i]
                        Jets1.pfc39_py        = jet1['PY_39'][i]
                        Jets1.pfc39_pz        = jet1['PZ_39'][i]
                        Jets1.pfc39_ifTrack   = jet1['C_39'][i]
                        Jets1.pfc40_energy    = jet1['E_40'][i]
                        Jets1.pfc40_px        = jet1['PX_40'][i]
                        Jets1.pfc40_py        = jet1['PY_40'][i]
                        Jets1.pfc40_pz        = jet1['PZ_40'][i]
                        Jets1.pfc40_ifTrack   = jet1['C_40'][i]
                    elif NumOfVecEl == 6:
                        Jets1.pfc1_energy    = jet1['E_1'][i]
                        Jets1.pfc1_px        = jet1['PX_1'][i]
                        Jets1.pfc1_py        = jet1['PY_1'][i]
                        Jets1.pfc1_pz        = jet1['PZ_1'][i]
                        Jets1.pfc1_ifTrack   = jet1['C_1'][i]
                        Jets1.pfc1_pType     = jet1['PID_1'][i]
                        Jets1.pfc2_energy    = jet1['E_2'][i]
                        Jets1.pfc2_px        = jet1['PX_2'][i]
                        Jets1.pfc2_py        = jet1['PY_2'][i]
                        Jets1.pfc2_pz        = jet1['PZ_2'][i]
                        Jets1.pfc2_ifTrack   = jet1['C_2'][i]
                        Jets1.pfc2_pType     = jet1['PID_2'][i]
                        Jets1.pfc3_energy    = jet1['E_3'][i]
                        Jets1.pfc3_px        = jet1['PX_3'][i]
                        Jets1.pfc3_py        = jet1['PY_3'][i]
                        Jets1.pfc3_pz        = jet1['PZ_3'][i]
                        Jets1.pfc3_ifTrack   = jet1['C_3'][i]
                        Jets1.pfc3_pType     = jet1['PID_3'][i]
                        Jets1.pfc4_energy    = jet1['E_4'][i]
                        Jets1.pfc4_px        = jet1['PX_4'][i]
                        Jets1.pfc4_py        = jet1['PY_4'][i]
                        Jets1.pfc4_pz        = jet1['PZ_4'][i]
                        Jets1.pfc4_ifTrack   = jet1['C_4'][i]
                        Jets1.pfc4_pType     = jet1['PID_4'][i]
                        Jets1.pfc5_energy    = jet1['E_5'][i]
                        Jets1.pfc5_px        = jet1['PX_5'][i]
                        Jets1.pfc5_py        = jet1['PY_5'][i]
                        Jets1.pfc5_pz        = jet1['PZ_5'][i]
                        Jets1.pfc5_ifTrack   = jet1['C_5'][i]
                        Jets1.pfc5_pType     = jet1['PID_5'][i]
                        Jets1.pfc6_energy    = jet1['E_6'][i]
                        Jets1.pfc6_px        = jet1['PX_6'][i]
                        Jets1.pfc6_py        = jet1['PY_6'][i]
                        Jets1.pfc6_pz        = jet1['PZ_6'][i]
                        Jets1.pfc6_ifTrack   = jet1['C_6'][i]
                        Jets1.pfc6_pType     = jet1['PID_6'][i]
                        Jets1.pfc7_energy    = jet1['E_7'][i]
                        Jets1.pfc7_px        = jet1['PX_7'][i]
                        Jets1.pfc7_py        = jet1['PY_7'][i]
                        Jets1.pfc7_pz        = jet1['PZ_7'][i]
                        Jets1.pfc7_ifTrack   = jet1['C_7'][i]
                        Jets1.pfc7_pType     = jet1['PID_7'][i]
                        Jets1.pfc8_energy    = jet1['E_8'][i]
                        Jets1.pfc8_px        = jet1['PX_8'][i]
                        Jets1.pfc8_py        = jet1['PY_8'][i]
                        Jets1.pfc8_pz        = jet1['PZ_8'][i]
                        Jets1.pfc8_ifTrack   = jet1['C_8'][i]
                        Jets1.pfc8_pType     = jet1['PID_8'][i]
                        Jets1.pfc9_energy    = jet1['E_9'][i]
                        Jets1.pfc9_px        = jet1['PX_9'][i]
                        Jets1.pfc9_py        = jet1['PY_9'][i]
                        Jets1.pfc9_pz        = jet1['PZ_9'][i]
                        Jets1.pfc9_ifTrack   = jet1['C_9'][i]
                        Jets1.pfc9_pType     = jet1['PID_9'][i]
                        Jets1.pfc10_energy    = jet1['E_10'][i]
                        Jets1.pfc10_px        = jet1['PX_10'][i]
                        Jets1.pfc10_py        = jet1['PY_10'][i]
                        Jets1.pfc10_pz        = jet1['PZ_10'][i]
                        Jets1.pfc10_ifTrack   = jet1['C_10'][i]
                        Jets1.pfc10_pType     = jet1['PID_10'][i]
                        Jets1.pfc11_energy    = jet1['E_11'][i]
                        Jets1.pfc11_px        = jet1['PX_11'][i]
                        Jets1.pfc11_py        = jet1['PY_11'][i]
                        Jets1.pfc11_pz        = jet1['PZ_11'][i]
                        Jets1.pfc11_ifTrack   = jet1['C_11'][i]
                        Jets1.pfc11_pType     = jet1['PID_11'][i]
                        Jets1.pfc12_energy    = jet1['E_12'][i]
                        Jets1.pfc12_px        = jet1['PX_12'][i]
                        Jets1.pfc12_py        = jet1['PY_12'][i]
                        Jets1.pfc12_pz        = jet1['PZ_12'][i]
                        Jets1.pfc12_ifTrack   = jet1['C_12'][i]
                        Jets1.pfc12_pType     = jet1['PID_12'][i]
                        Jets1.pfc13_energy    = jet1['E_13'][i]
                        Jets1.pfc13_px        = jet1['PX_13'][i]
                        Jets1.pfc13_py        = jet1['PY_13'][i]
                        Jets1.pfc13_pz        = jet1['PZ_13'][i]
                        Jets1.pfc13_ifTrack   = jet1['C_13'][i]
                        Jets1.pfc13_pType     = jet1['PID_13'][i]
                        Jets1.pfc14_energy    = jet1['E_14'][i]
                        Jets1.pfc14_px        = jet1['PX_14'][i]
                        Jets1.pfc14_py        = jet1['PY_14'][i]
                        Jets1.pfc14_pz        = jet1['PZ_14'][i]
                        Jets1.pfc14_ifTrack   = jet1['C_14'][i]
                        Jets1.pfc14_pType     = jet1['PID_14'][i]
                        Jets1.pfc15_energy    = jet1['E_15'][i]
                        Jets1.pfc15_px        = jet1['PX_15'][i]
                        Jets1.pfc15_py        = jet1['PY_15'][i]
                        Jets1.pfc15_pz        = jet1['PZ_15'][i]
                        Jets1.pfc15_ifTrack   = jet1['C_15'][i]
                        Jets1.pfc15_pType     = jet1['PID_15'][i]
                        Jets1.pfc16_energy    = jet1['E_16'][i]
                        Jets1.pfc16_px        = jet1['PX_16'][i]
                        Jets1.pfc16_py        = jet1['PY_16'][i]
                        Jets1.pfc16_pz        = jet1['PZ_16'][i]
                        Jets1.pfc16_ifTrack   = jet1['C_16'][i]
                        Jets1.pfc16_pType     = jet1['PID_16'][i]
                        Jets1.pfc17_energy    = jet1['E_17'][i]
                        Jets1.pfc17_px        = jet1['PX_17'][i]
                        Jets1.pfc17_py        = jet1['PY_17'][i]
                        Jets1.pfc17_pz        = jet1['PZ_17'][i]
                        Jets1.pfc17_ifTrack   = jet1['C_17'][i]
                        Jets1.pfc17_pType     = jet1['PID_17'][i]
                        Jets1.pfc18_energy    = jet1['E_18'][i]
                        Jets1.pfc18_px        = jet1['PX_18'][i]
                        Jets1.pfc18_py        = jet1['PY_18'][i]
                        Jets1.pfc18_pz        = jet1['PZ_18'][i]
                        Jets1.pfc18_ifTrack   = jet1['C_18'][i]
                        Jets1.pfc18_pType     = jet1['PID_18'][i]
                        Jets1.pfc19_energy    = jet1['E_19'][i]
                        Jets1.pfc19_px        = jet1['PX_19'][i]
                        Jets1.pfc19_py        = jet1['PY_19'][i]
                        Jets1.pfc19_pz        = jet1['PZ_19'][i]
                        Jets1.pfc19_ifTrack   = jet1['C_19'][i]
                        Jets1.pfc19_pType     = jet1['PID_19'][i]
                        Jets1.pfc20_energy    = jet1['E_20'][i]
                        Jets1.pfc20_px        = jet1['PX_20'][i]
                        Jets1.pfc20_py        = jet1['PY_20'][i]
                        Jets1.pfc20_pz        = jet1['PZ_20'][i]
                        Jets1.pfc20_ifTrack   = jet1['C_20'][i]
                        Jets1.pfc20_pType     = jet1['PID_20'][i]
                        Jets1.pfc21_energy    = jet1['E_21'][i]
                        Jets1.pfc21_px        = jet1['PX_21'][i]
                        Jets1.pfc21_py        = jet1['PY_21'][i]
                        Jets1.pfc21_pz        = jet1['PZ_21'][i]
                        Jets1.pfc21_ifTrack   = jet1['C_21'][i]
                        Jets1.pfc21_pType     = jet1['PID_21'][i]
                        Jets1.pfc22_energy    = jet1['E_22'][i]
                        Jets1.pfc22_px        = jet1['PX_22'][i]
                        Jets1.pfc22_py        = jet1['PY_22'][i]
                        Jets1.pfc22_pz        = jet1['PZ_22'][i]
                        Jets1.pfc22_ifTrack   = jet1['C_22'][i]
                        Jets1.pfc22_pType     = jet1['PID_22'][i]
                        Jets1.pfc23_energy    = jet1['E_23'][i]
                        Jets1.pfc23_px        = jet1['PX_23'][i]
                        Jets1.pfc23_py        = jet1['PY_23'][i]
                        Jets1.pfc23_pz        = jet1['PZ_23'][i]
                        Jets1.pfc23_ifTrack   = jet1['C_23'][i]
                        Jets1.pfc23_pType     = jet1['PID_23'][i]
                        Jets1.pfc24_energy    = jet1['E_24'][i]
                        Jets1.pfc24_px        = jet1['PX_24'][i]
                        Jets1.pfc24_py        = jet1['PY_24'][i]
                        Jets1.pfc24_pz        = jet1['PZ_24'][i]
                        Jets1.pfc24_ifTrack   = jet1['C_24'][i]
                        Jets1.pfc24_pType     = jet1['PID_24'][i]
                        Jets1.pfc25_energy    = jet1['E_25'][i]
                        Jets1.pfc25_px        = jet1['PX_25'][i]
                        Jets1.pfc25_py        = jet1['PY_25'][i]
                        Jets1.pfc25_pz        = jet1['PZ_25'][i]
                        Jets1.pfc25_ifTrack   = jet1['C_25'][i]
                        Jets1.pfc25_pType     = jet1['PID_25'][i]
                        Jets1.pfc26_energy    = jet1['E_26'][i]
                        Jets1.pfc26_px        = jet1['PX_26'][i]
                        Jets1.pfc26_py        = jet1['PY_26'][i]
                        Jets1.pfc26_pz        = jet1['PZ_26'][i]
                        Jets1.pfc26_ifTrack   = jet1['C_26'][i]
                        Jets1.pfc26_pType     = jet1['PID_26'][i]
                        Jets1.pfc27_energy    = jet1['E_27'][i]
                        Jets1.pfc27_px        = jet1['PX_27'][i]
                        Jets1.pfc27_py        = jet1['PY_27'][i]
                        Jets1.pfc27_pz        = jet1['PZ_27'][i]
                        Jets1.pfc27_ifTrack   = jet1['C_27'][i]
                        Jets1.pfc27_pType     = jet1['PID_27'][i]
                        Jets1.pfc28_energy    = jet1['E_28'][i]
                        Jets1.pfc28_px        = jet1['PX_28'][i]
                        Jets1.pfc28_py        = jet1['PY_28'][i]
                        Jets1.pfc28_pz        = jet1['PZ_28'][i]
                        Jets1.pfc28_ifTrack   = jet1['C_28'][i]
                        Jets1.pfc28_pType     = jet1['PID_28'][i]
                        Jets1.pfc29_energy    = jet1['E_29'][i]
                        Jets1.pfc29_px        = jet1['PX_29'][i]
                        Jets1.pfc29_py        = jet1['PY_29'][i]
                        Jets1.pfc29_pz        = jet1['PZ_29'][i]
                        Jets1.pfc29_ifTrack   = jet1['C_29'][i]
                        Jets1.pfc29_pType     = jet1['PID_29'][i]
                        Jets1.pfc30_energy    = jet1['E_30'][i]
                        Jets1.pfc30_px        = jet1['PX_30'][i]
                        Jets1.pfc30_py        = jet1['PY_30'][i]
                        Jets1.pfc30_pz        = jet1['PZ_30'][i]
                        Jets1.pfc30_ifTrack   = jet1['C_30'][i]
                        Jets1.pfc30_pType     = jet1['PID_30'][i]
                        Jets1.pfc31_energy    = jet1['E_31'][i]
                        Jets1.pfc31_px        = jet1['PX_31'][i]
                        Jets1.pfc31_py        = jet1['PY_31'][i]
                        Jets1.pfc31_pz        = jet1['PZ_31'][i]
                        Jets1.pfc31_ifTrack   = jet1['C_31'][i]
                        Jets1.pfc31_pType     = jet1['PID_31'][i]
                        Jets1.pfc32_energy    = jet1['E_32'][i]
                        Jets1.pfc32_px        = jet1['PX_32'][i]
                        Jets1.pfc32_py        = jet1['PY_32'][i]
                        Jets1.pfc32_pz        = jet1['PZ_32'][i]
                        Jets1.pfc32_ifTrack   = jet1['C_32'][i]
                        Jets1.pfc32_pType     = jet1['PID_32'][i]
                        Jets1.pfc33_energy    = jet1['E_33'][i]
                        Jets1.pfc33_px        = jet1['PX_33'][i]
                        Jets1.pfc33_py        = jet1['PY_33'][i]
                        Jets1.pfc33_pz        = jet1['PZ_33'][i]
                        Jets1.pfc33_ifTrack   = jet1['C_33'][i]
                        Jets1.pfc33_pType     = jet1['PID_33'][i]
                        Jets1.pfc34_energy    = jet1['E_34'][i]
                        Jets1.pfc34_px        = jet1['PX_34'][i]
                        Jets1.pfc34_py        = jet1['PY_34'][i]
                        Jets1.pfc34_pz        = jet1['PZ_34'][i]
                        Jets1.pfc34_ifTrack   = jet1['C_34'][i]
                        Jets1.pfc34_pType     = jet1['PID_34'][i]
                        Jets1.pfc35_energy    = jet1['E_35'][i]
                        Jets1.pfc35_px        = jet1['PX_35'][i]
                        Jets1.pfc35_py        = jet1['PY_35'][i]
                        Jets1.pfc35_pz        = jet1['PZ_35'][i]
                        Jets1.pfc35_ifTrack   = jet1['C_35'][i]
                        Jets1.pfc35_pType     = jet1['PID_35'][i]
                        Jets1.pfc36_energy    = jet1['E_36'][i]
                        Jets1.pfc36_px        = jet1['PX_36'][i]
                        Jets1.pfc36_py        = jet1['PY_36'][i]
                        Jets1.pfc36_pz        = jet1['PZ_36'][i]
                        Jets1.pfc36_ifTrack   = jet1['C_36'][i]
                        Jets1.pfc36_pType     = jet1['PID_36'][i]
                        Jets1.pfc37_energy    = jet1['E_37'][i]
                        Jets1.pfc37_px        = jet1['PX_37'][i]
                        Jets1.pfc37_py        = jet1['PY_37'][i]
                        Jets1.pfc37_pz        = jet1['PZ_37'][i]
                        Jets1.pfc37_ifTrack   = jet1['C_37'][i]
                        Jets1.pfc37_pType     = jet1['PID_37'][i]
                        Jets1.pfc38_energy    = jet1['E_38'][i]
                        Jets1.pfc38_px        = jet1['PX_38'][i]
                        Jets1.pfc38_py        = jet1['PY_38'][i]
                        Jets1.pfc38_pz        = jet1['PZ_38'][i]
                        Jets1.pfc38_ifTrack   = jet1['C_38'][i]
                        Jets1.pfc38_pType     = jet1['PID_38'][i]
                        Jets1.pfc39_energy    = jet1['E_39'][i]
                        Jets1.pfc39_px        = jet1['PX_39'][i]
                        Jets1.pfc39_py        = jet1['PY_39'][i]
                        Jets1.pfc39_pz        = jet1['PZ_39'][i]
                        Jets1.pfc39_ifTrack   = jet1['C_39'][i]
                        Jets1.pfc39_pType     = jet1['PID_39'][i]
                        Jets1.pfc40_energy    = jet1['E_40'][i]
                        Jets1.pfc40_px        = jet1['PX_40'][i]
                        Jets1.pfc40_py        = jet1['PY_40'][i]
                        Jets1.pfc40_pz        = jet1['PZ_40'][i]
                        Jets1.pfc40_ifTrack   = jet1['C_40'][i]
                        Jets1.pfc40_pType     = jet1['PID_40'][i]


                newTree.Fill()

        #########################################################  
        if i%ti == 1 and i>ti:
            end = timer() 
            dt = end-start
            tl = int( ((NofEntries-i)/ti ) * dt )
            if tl > 60:
                sys.stdout.write("\r" + 'time left: ' + str( tl/60 ) + 'min' )
                sys.stdout.flush()
            else: 
                sys.stdout.write("\r" + 'time left: ' + 'less than 1 min')
                sys.stdout.flush() 
        #########################################################

    print 'produced skimmed file',newFile.GetName(),'\tevents =',newTree.GetEntries(),'\tweight =',newTree.GetWeight()
    newFile.cd()
    newFile.Write()
    newFile.Close() 
#-----------------------------------------------------------------------------------------------------------

#-----------===============================
def skim(names): 
    for cc in channel:
        if 'QCD' in channel[cc]:
            nFn = channel[cc].replace('.root','_' + str(num_of_jets) + 'j_skimed.root')
        elif 'ctauS' in channel[cc]:
            nFn = channel[cc].replace('.root','_' + str(num_of_jets) + 'j_skimed.root') #('.root','_4mj_skimed.root')
        ss = path + channel[cc]    
        skim_c(ss,nFn)
#-----------===============================

#=====================================================================================================
os.chdir(args1)
if not os.path.isdir('Skim'): os.mkdir('Skim')

p = mp.Process(target=skim, args=(fn,))
p.start()
#=====================================================================================================












"""
###################################################################################################################
fin = TFile( path + 'VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-500_pfc_jetOnly_bugged.root' , "r" )
tin = fin.Get('ntuple/tree')
print tin
entries = tin.GetEntriesFast()
print entries
for jentry in xrange(entries):
    ientry = tin.GetEntry(jentry)
    for j in xrange(tin.Jets.size()):
        print 'Jets.size: ' + str( tin.Jets.size() )
        print tin.Jets[j].pt
###################################################################################################################
"""
