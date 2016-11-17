

1) Goal:

This tutorial will teach you how to:

- generate signal and background samples with Pythia8 within FCCSW
- run a fast parametric detector simulation with Delphes within FCCSW
- apply a event selection on those samples with Heppy
- produce flat ntuples with observables of interest with Heppy
- produce pretty plots



Part I: Install FCCSW 
----------------------


The MC event generator Pythia8 and Delphes detector simulation programs are both included in the FCC software.

First, log into lxplus. Then download and install the FCC software: 

git clone git@github.com:HEP-FCC/FCCSW.git
cd FCCSW
source ./init.sh
make -j 12


Part II: Generate and simulate Events
--------------------------------------

For this tutorial we will consider the following physics processes: 

p p -> H -> 4 l
p p -> Z/gamma Z/gamma -> 4 l 

Pythia can be configured to hadronize previously generated hard scattering in the form of Les Houches event files (*.lhe),
or generate the hard process itself and then run the parton shower and hadronization. In either case, the FCCSW takes
as input a Pythia8 configuration file (*.cmd), and does not need to know which approach was used.

The following commands will run Pythia8/Delphes and produce the relevant signal sample and background samples:

./run fccrun.py Sim/SimDelphesInterface/options/PythiaDelphes_config.py --inputfile=Generation/data/Pythia_pp_h_4l.cmd --outputfile=pp_h_4l.root --nevents=1000
./run fccrun.py Sim/SimDelphesInterface/options/PythiaDelphes_config.py --inputfile=Generation/data/Pythia_pp_zgzg_4l.cmd --outputfile=pp_zgzg_4l.root --nevents=1000

The "--inputfile" , --outputfile and "--nevents" options simply overwrite parameters that are defined in the main configuration "Sim/SimDelphesInterface/options/PythiaDelphes_config.py"

The following information is specified in the configuration file:

- Pythia8 configuration file 
- Delphes detector card
- number of events
- name of output file
- collections to be stored in the output tree. 

For a complete discussion on the configuration file, see [this page](). Besides input/output and number of events (which can be specified through command line), 
for most cases as a user you won't need to apply any change to the config file. 

The output is ROOT file containing a tree in the FCC Event Data Model structure. It is browsable with ROOT:

root -l pp_h_4l.root 
TBrowser t;

Plotting some basic quantities directly on this output is possible, although not very practical:

events->Draw("sqrt(electrons[0].core.p4.px*electrons[0].core.p4.px + electrons[0].core.p4.py*electrons[0].core.p4.py)")

[plot]

Now overwrite the samples you just produced, with larger samples (10k events) that have been stored in eos.

eos cp ....


Part III: Analyze the output with Heppy
----------------------------------------


[Heppy](https://github.com/cbernet/heppy) is a python framework suitable for analyzing the FCCSW output.

First install HEPPY:

git clone git@github.com:cbernet/heppy.git
cd heppy
source init.sh
cd ..
 
Understand the configuration file for this H->4l analysis: "heppy/test/analysis_pp_hTo4l_simple_cfg.py"
This is where filters on input collections and event selection are defined.
The sequence is divided in two parts, a gen level analysis, and a reco level. 

The gen level part simply filters interesting leptons ("gen_leptons") and stores pT, eta in in flat tree ("gen_tree").
Have a look at the corresponding code in "heppy/analyzers/examples/hzz4l/HTo4lGenTreeProducer.py".

The reco level analysis first selects isolated leptons (selected_muons, selected_electrons), merges them into a single collection ("selected_leptons"),
builds Z candidates ("zeds") and finally builds higgs candidates  ("higgses"). After that an event selection is applied ("selection").
Open "heppy/analyzers/examples/hzz4l/selection.py" and understand the event selection. Finally another flat tree is produced "HTo4lTreeProducer".
This tree contains contains all relevant information for the two reconstructed Z bosons, the Higgs, and the four associated leptons. 
For comparison, also the MC level counterparts of the reconstructed quantities are plotted. 

To summarize, when designing a new analysis, you will have to define:

- a configuration file containing the analysis sequence
- an event selection
- one or several tree producer(s) where the variables to be stored in the output tree(s) are specified
- optionally, new modules that are specific to your analysis (e.g. "LeptonicZedBuilder" here)

Now run HEPPY:

heppy_loop.py pp_h_4l heppy/test/analysis_pp_hTo4l_simple_cfg.py -N 1000 -I pp_h_4l.root;
heppy_loop.py pp_zgzg_4l heppy/test/analysis_pp_hTo4l_simple_cfg.py -N 1000 -I pp_zgzg_4l.root;

The runs create two output directories "pp_h_4l" and "pp_zgzg_4l", with various subdirectories. The most important
outputs are:

"example/heppy.analyzers.examples.hzz4l.selection.Selection_cuts/cut_flow.txt"

The file above shows efficiencies for various stages of the event selections. The gen and reco output trees:

example/heppy.analyzers.examples.hzz4l.HTo4lGenTreeProducer.HTo4lGenTreeProducer_1/tree.root
example/heppy.analyzers.examples.hzz4l.HTo4lTreeProducer.HTo4lTreeProducer_1/tree.root


Part IV: Produce plots
-----------------------

Download the python code:

git clone git@github.com:selvaggi/tutorials.git

Produce Gen-level plots:











































