#import math
n = 40
ln = range(n)



s = ''
for i in range(n):
    s = s + "'E_" + str(i+1) + "'"
    if i+1 != n:
        s = s + ',' 
s = s + ',' 
for i in range(n):
    s = s + "'PX_" + str(i+1) + "'"
    if i+1 != n:
        s = s + ',' 
s = s + ',' 
for i in range(n):
    s = s + "'PY_" + str(i+1) + "'"
    if i+1 != n:
        s = s + ',' 
s = s + ',' 
for i in range(n):
    s = s + "'PZ_" + str(i+1) + "'"
    if i+1 != n:
        s = s + ',' 
s = s + ',' 
for i in range(n):
    s = s + "'C_" + str(i+1) + "'"
    if i+1 != n:
        s = s + ',' 
s = s + ',' 
for i in range(n):
    s = s + "'PID_" + str(i+1) + "'"
    if i+1 != n:
        s = s + ','        
print s



for i in ln:
    print("                    Jets1.pfc" + str(i+1) + "_energy    = jet1['E_" + str(i+1) + "'][i]")
    print("                    Jets1.pfc" + str(i+1) + "_px        = jet1['PX_" + str(i+1) + "'][i]")
    print("                    Jets1.pfc" + str(i+1) + "_py        = jet1['PY_" + str(i+1) + "'][i]")
    print("                    Jets1.pfc" + str(i+1) + "_pz        = jet1['PZ_" + str(i+1) + "'][i]")
    print("                    Jets1.pfc" + str(i+1) + "_ifTrack   = jet1['C_" + str(i+1) + "'][i]")
    print("                    Jets1.pfc" + str(i+1) + "_pType     = jet1['PID_" + str(i+1) + "'][i]")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



#"""
#~~~~~~~~~~~~~~ObjectsFormat.cc~~~~~~~~~~~~~~~~
for i in ln:
    print("         I.pfc" + str(i+1) + "_energy   = energyVect.at(" + str(i) + ");")
    print("         I.pfc" + str(i+1) + "_px       = pxVect.at(" + str(i) + ");") 
    print("         I.pfc" + str(i+1) + "_py       = pyVect.at(" + str(i) + ");")
    print("         I.pfc" + str(i+1) + "_pz       = pzVect.at(" + str(i) + ");")
    print("         I.pfc" + str(i+1) + "_ifTrack  = ifTrackVect.at(" + str(i) + ");")
    print("         I.pfc" + str(i+1) + "_pType    = pTypeVect.at(" + str(i) + ");")

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

for i in ln:
    print("         I.pfc" + str(i+1) + "_energy   = 0.;")
    print("         I.pfc" + str(i+1) + "_px       = 0.;")
    print("         I.pfc" + str(i+1) + "_py       = 0.;")
    print("         I.pfc" + str(i+1) + "_pz       = 0.;")
    print("         I.pfc" + str(i+1) + "_ifTrack  = -1;")
    print("         I.pfc" + str(i+1) + "_pType    = -1;")

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

ListJetType_str = ""
for i in ln:
    ListJetType_str = ListJetType_str + "pfc" + str(i+1) + "_energy/F:"
    ListJetType_str = ListJetType_str + "pfc" + str(i+1) + "_px/F:"
    ListJetType_str = ListJetType_str + "pfc" + str(i+1) + "_py/F:"
    ListJetType_str = ListJetType_str + "pfc" + str(i+1) + "_pz/F:"
    ListJetType_str = ListJetType_str + "pfc" + str(i+1) + "_ifTrack/I:"
    ListJetType_str = ListJetType_str + "pfc" + str(i+1) + "_pType/I:"

print ListJetType_str
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

#~~~~~~~~~~~~~~ObjectsFormat.cc~~~~~~~~~~~~~~~~



#~~~~~~~~~~~~~~Objects.h~~~~~~~~~~~~~~~~ 
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")   
JetType_str = ""
for i in ln:
    JetType_str = JetType_str + "pfc" + str(i+1) + "_energy(0.), "
    JetType_str = JetType_str + "pfc" + str(i+1) + "_px(0.), "
    JetType_str = JetType_str + "pfc" + str(i+1) + "_py(0.), "
    JetType_str = JetType_str + "pfc" + str(i+1) + "_pz(0.), "
    JetType_str = JetType_str + "pfc" + str(i+1) + "_ifTrack(-1), "
    JetType_str = JetType_str + "pfc" + str(i+1) + "_pType(-1), "
print JetType_str
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

for i in ln:
    print("    float pfc" + str(i+1) + "_energy;")
    print("    float pfc" + str(i+1) + "_px;")
    print("    float pfc" + str(i+1) + "_py;")
    print("    float pfc" + str(i+1) + "_pz;")
    print("    int   pfc" + str(i+1) + "_ifTrack;")
    print("    int   pfc" + str(i+1) + "_pType;")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

#~~~~~~~~~~~~~~Objects.h~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~RecoStudiesCalo.py~~~~~~~~~~~~~~~~
#for j in range(15):
#    print("        "+"'"+"/store/user/lbenato/VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-500_Summer16_MINIAODSIM_calojets/VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-500_TuneCUETP8M1_13TeV-powheg-pythia8_PRIVATE-MC/RunIISummer16-PU_premix-Moriond17_80X_mcRun2_2016_MINIAODSIM_calojets/180611_172219/0000/miniaod_calo_" + str(j+1) + ".root'"+",")
#~~~~~~~~~~~~~~RecoStudiesCalo.py~~~~~~~~~~~~~~~~




for i in ln:
    print("                    Jets1.pfc" + str(i+1) + "_energy    = Jet_old_dict[j+1].pfc" + str(i+1) + "_energy")
    print("                    Jets1.pfc" + str(i+1) + "_px        = Jet_old_dict[j+1].pfc" + str(i+1) + "_px")
    print("                    Jets1.pfc" + str(i+1) + "_py        = Jet_old_dict[j+1].pfc" + str(i+1) + "_py")
    print("                    Jets1.pfc" + str(i+1) + "_pz        = Jet_old_dict[j+1].pfc" + str(i+1) + "_pz")
    print("                    Jets1.pfc" + str(i+1) + "_ifTrack   = Jet_old_dict[j+1].pfc" + str(i+1) + "_ifTrack")
    print("                    Jets1.pfc" + str(i+1) + "_pType     = Jet_old_dict[j+1].pfc" + str(i+1) + "_pType")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


#for i in ln:
#    print("cs['pfc" + str(i+1) + "_ifTrack_L'] = 'pfc" + str(i+1) + "_ifTrack' + '>' + '-1' ")

#for i in ln:
#    print("                              a +\ ")
#    print("                              '(' + prs + cs['pfc" + str(i+1) + "_ifTrack_L'] + ')' +\ ")        
                     

#"""




str_jts = ''
jetTypeSmallStr = ['cHadE','nHadE','cHadEFrac','nHadEFrac','nEmE','nEmEFrac','cEmE','cEmEFrac','cmuE','cmuEFrac','muE','muEFrac','eleE','eleEFrac','eleMulti','photonE','photonEFrac','photonMulti','cHadMulti','npr','cMulti','nMulti']#,'FracCal']
for i in jetTypeSmallStr:
        str_jts += i
        str_jts += '/F:'  
print str_jts

print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'


jetTypeSmallStr2 = ['emEFrac','emEinEB','emEinEE','emEinHF','EFracHad','hadEinHB','hadEinHE','hadEinHF','hadEinHO']
for i in jetTypeSmallStr2:
    print("    I." + i + "   = 0.;")
  

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")




ListJetType_str2 = ""
jetTypeSmallStr3 = jetTypeSmallStr + jetTypeSmallStr2
for i in jetTypeSmallStr3:
    ListJetType_str2 = ListJetType_str2 + i + "/F:"


print ListJetType_str2
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



ListJetType_str3 = ""
jetTypeSmallStr4 = ['alphaMax','sigIP2DMedian','theta2DMedian','hcalE','ecalE','FracCal','flightDist2d','flightDist2dSig','flightDist3d','flightDist3dSig','nSV','nSVCand','nVertexTracks','nSelectedTracks','dRSVJet','SV_x','SV_y','SV_z','SV_dx','SV_dy','SV_dz','nTracksSV','SV_mass','indexSV']
for i in jetTypeSmallStr4:
    ListJetType_str3 = ListJetType_str3 + i + "/F:"


print ListJetType_str3
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")