from ROOT import TFile, gROOT, TH1D, kRed, TLegend
from tools.drawCanvas import *
import os

gROOT.SetBatch()

treeName = "events"
FileS = "pp_h_4l/example/heppy.analyzers.examples.hzz4l.HTo4lGenTreeProducer.HTo4lGenTreeProducer_1/tree.root"
FileB = "pp_zgzg_4l/example/heppy.analyzers.examples.hzz4l.HTo4lGenTreeProducer.HTo4lGenTreeProducer_1/tree.root"

Vars = {   
    "lep1vsPt_pt":{"name":"lep1vsPt_pt","title":"p_{T}^{(1)} [GeV]","bin":25,"xmin":0,"xmax":100},
    "lep2vsPt_pt":{"name":"lep2vsPt_pt","title":"p_{T}^{(2)} [GeV]","bin":25,"xmin":0,"xmax":100},
    "lep3vsPt_pt":{"name":"lep3vsPt_pt","title":"p_{T}^{(3)} [GeV]","bin":25,"xmin":0,"xmax":50},
    "lep4vsPt_pt":{"name":"lep4vsPt_pt","title":"p_{T}^{(4)} [GeV]","bin":25,"xmin":0,"xmax":50},

    "lep1vsEta_eta":{"name":"lep1vsEta_eta","title":"#eta^{(1)}","bin":25,"xmin":0,"xmax":10},
    "lep2vsEta_eta":{"name":"lep2vsEta_eta","title":"#eta^{(2)}","bin":25,"xmin":0,"xmax":10},
    "lep3vsEta_eta":{"name":"lep3vsEta_eta","title":"#eta^{(3)}","bin":25,"xmin":0,"xmax":10},
    "lep4vsEta_eta":{"name":"lep4vsEta_eta","title":"#eta^{(4)}","bin":25,"xmin":0,"xmax":10}
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

yAxisLabel = "a. u."

rightText = "GEN"
leftText = "#sqrt{s} = 100 TeV"
format = "png"
outputDirectory = "plots" 

if not os.path.exists(outputDirectory) :
    os.system("mkdir "+outputDirectory)

for var in Vars.keys() : 
    dict_histoS[var].SetLineWidth(3)
    dict_histoS[var].SetLineWidth(3)
    dict_histoB[var].SetLineColor(ROOT.kRed)
   
    try : 
        dict_histoS[var].Scale(1./float(dict_histoS[var].Integral()))
        dict_histoB[var].Scale(1./float(dict_histoB[var].Integral()))
    except ZeroDivisionError :
        print "Can not renormalize because of integral = 0." 
    
    leg = TLegend(0.50,0.76,0.89,0.89)
    leg.AddEntry(dict_histoS[var],"p p #rightarrow H #rightarrow 4l","l")
    leg.AddEntry(dict_histoB[var],"p p #rightarrow ZZ / Z #gamma^{*} #rightarrow 4l","l")
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)

    drawDoublehisto(dict_histoS[var],dict_histoB[var],var,yAxisLabel,leg,leftText,rightText,format,outputDirectory,0)





