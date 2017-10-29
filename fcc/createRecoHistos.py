from ROOT import TFile, gROOT, TH1D, kRed, TLegend, THStack
from tools.drawCanvas import *
import os

gROOT.SetBatch()

treeName = "events"
FileS = "myTest/example/heppy.analyzers.examples.hzz4l.HTo4lTreeProducer.HTo4lTreeProducer_1/tree.root"
FileB = "pp_zgzg_4l/example/heppy.analyzers.examples.hzz4l.HTo4lTreeProducer.HTo4lTreeProducer_1/tree.root"

# number of generated events
nGenS = 10000
nGenB = 10000

# integrated luminosity
intLumi = 25000

kFactorS = 3.50
kFactorB = 1.80

# MG5 LO XS x BR in (pb)
sigmaS = 0.026
sigmaB = 1.04

weightS = kFactorS*sigmaS*intLumi/nGenS
weightB = kFactorB*sigmaB*intLumi/nGenB

Vars = {   
    "zed1_m":{"name":"zed1_m","title":"m_{ll}^{(1)} [GeV]","bin":36,"xmin":0,"xmax":100},
    "zed2_m":{"name":"zed2_m","title":"m_{ll}^{(2)} [GeV]","bin":36,"xmin":0,"xmax":100},
    "higgs_m":{"name":"higgs_m","title":"m_{4l} [GeV]","bin":36,"xmin":70,"xmax":170},
}


dict_histoS = {var:TH1D(var+"S",var+"S;"+Vars[var]["title"]+";",Vars[var]["bin"],Vars[var]["xmin"],Vars[var]["xmax"]) for var in Vars}
dict_histoB = {var:TH1D(var+"B",var+"B;"+Vars[var]["title"]+";",Vars[var]["bin"],Vars[var]["xmin"],Vars[var]["xmax"]) for var in Vars}

rootFileS = TFile(FileS,"read")
treeS = rootFileS.Get(treeName)
rootFileB = TFile(FileB,"read")
treeB = rootFileB.Get(treeName)


for entry in xrange(treeS.GetEntries()) :
    treeS.GetEntry(entry)

    for var in Vars.keys() :
        dict_histoS[var].Fill(getattr(treeS,Vars[var]["name"]))

for entry in xrange(treeB.GetEntries()) :
    treeB.GetEntry(entry)
    for var in Vars.keys() :
        dict_histoB[var].Fill(getattr(treeB,Vars[var]["name"]))

myBTGStyle()

yAxisLabel = "Events / 2.5 GeV"

rightText = "RECO: Delphes-3.4.0"
leftText = "#sqrt{s} = 100 TeV, L = 25 fb^{-1}"
format = "png"
outputDirectory = "plots" 
outFile = outputDirectory+"/plots.root"

if not os.path.exists(outputDirectory) :
    os.system("mkdir "+outputDirectory)

for var in Vars.keys() : 
     
    try : 
        
	# rescale by
        dict_histoS[var].Scale(weightS)
        dict_histoB[var].Scale(weightB)

    except ZeroDivisionError :
        print "Can not renormalize because of integral = 0." 
    
    leg = TLegend(0.69,0.75,0.88,0.88)
    leg.AddEntry(dict_histoB[var],"ZZ / Z #gamma^{*}","f")
    leg.AddEntry(dict_histoS[var],"H(125)","l")
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)

    hS = dict_histoS[var]
    hB = []
    hB.append(dict_histoB[var])

    drawStack(var,yAxisLabel,leg,leftText,rightText,format,outputDirectory,0,hS,hB)





