===============================================================================
                               BEGIN TRANSMISSION
===============================================================================

===============================================================================
===============================================================================
~ Repository for Verification of OpenMOC using BEAVRS Full-Core Reactor Model ~
===============================================================================
===============================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###############################################################################
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

===============================================================================
                          AUTHORS & CONTACT INFORMATION
===============================================================================

Undergraduate Contributors-----------------------------------------------------

    Davis Tran        -- dvtran@mit.edu
    Stephanie Pavlick -- spavlick@mit.edu
    Jasmeet Arora     -- jasmeet@mit.edu

Graduate Mentor----------------------------------------------------------------

    Will Boyd         -- wboyd@mit.edu

===============================================================================
                                 BRIEF OVERVIEW
===============================================================================

The BEAVRS-Openmoc repository contains files that use OpenMOC to develop
convergence studies of five different assembly types in the BEAVRS Full Core
reactor model.

===============================================================================
                               DETAILED OVERVIEW
===============================================================================

The BEAVRS-Openmoc repository uses the MIT Computational Reactor Physics
(MIT-CRPG) Open-source Method of Characteristics reactor simulation code to run
numerous simulations on reactor models. The specific models used were single
17x17 assemblies in the BEAVRS full-core reactor model. The BEAVRS full-core 
reactor model was also developed by the MIT-CRPG using real reactor data. 
Cross-sectional materials data for the assemblies were generated using CASMO.
The five assemblies contain various types of fuel enrichments and do or do not
contain burnable poisons. After running numerous simulations, results were
generated indicating errors in eigenvalues, max errors in pin powers, and mean
errors in pin powers, all comparing OpenMOC results to CASMO results. Running
matplotlib and OpenMOC plotter methods on these results gives the several graphs
generated and presented at the ANS 2014 Student Conference.

===============================================================================
                             DOWNLOAD & INSTALLATION
===============================================================================

Make sure numpy, hdf5, and matplotlib python modules are installed on your
Linux machine

Run the following command to download and install these modules in Debian
based Linux

    >$ sudo get-apt install python-h5py python-numpy python-matplotlib

Create a directory for the repository

Use the cd command to enter the new directory

Run the following code in the Linux terminal:
    
    >$ git clone https://github.com/spavlick/BEAVRS-openMOC.git

===============================================================================
                      RUNNING OPENMOC STUDIES SIMULATIONS
===============================================================================

Running a single simulation on your own machine will take very little time.
However, full convergence studies simulations using numerous test parameters 
will take much longer to run and it is recommended that you run the full studies
on a large cluster. One example using one assembly is given for each case. 
Running the studies for other assemblies follows similarly. All code is based
from the initial directory (BEAVRS-Openmoc).

Basic Simulation---------------------------------------------------------------

        To run one simulation for 1.6% enriched fuel w/o BP assembly:

        >$ cd studies/pwru160c00/
        >$ python pwru160c00.py

Cluster Single Simulation------------------------------------------------------

        To run one simulation for 1.6% enriched fuel w/o BP assembly on cluster:

        >$ cd/studies/pwru160c00/
        >$ qsub pwru160c00.pbs

        Where the user may designate other singular files by replacing
        pwru160c00.pbs with any other simulation file.

Cluster Full Simulation--------------------------------------------------------

        To run full study for 1.6% enriched fuel w/o BP assembly on nse-cluster:

        >$ cd studies/pwru160c00/
        >$ ./run.sh

Results from these simulations are located in the results directory within the
individual assembly directories.

===============================================================================
                 |KINF|, |MAX PIN|, and |MEAN PIN| ERROR PLOTS
===============================================================================

Once results have been generated for the desired assemblies, you can plot the
error data using the given python plotting files. In order to run the plotting
files, copy and paste your results files from the individual assembly results 
directories to the studies results directory. You need all 5 error results files
to run the plotting files correctly.

Plot Full Azimuthal Angles Error Data------------------------------------------

        To plot azimuthal angles errors for all five assemblies:

        >$ cd studies/
        >$ python azim-error-plotter.py

        Which generates three plots located in the studies directory.

Plot Full Track Spacing Error Data---------------------------------------------

        To plot track spacing errors for all five assemblies:

        >$ cd studies/
        >$ python trackspacing-error-plotter.py

        Which generates three plots located in the studies directory.

Plot Flat Source Regions Error Data--------------------------------------------

        To plot flat source region errors for all five assemblies:

        >$ cd studies/
        >$ python fsr-plotter.py

        Which generates fifteen grid plots located in the studies directory.
        WARNING: These results were not fully analyzed for meaning and were not
        presented at the conference. View these under your own descretion.

===============================================================================
                            PIN POWER ERROR PLOTS
===============================================================================

Running some simulations will also generate a 'fission-rates.h5' file located
in the pin-powers directory in each individual assembly directory. Again, you
must first move these plots out of the assembly directory into a pin-powers
directory in the studies directory. Instructions are given for this also.

Plot Pin Error Grid Plots -----------------------------------------------------

        To plot pin power error grid plots for a single (pwru160c00) assembly:

        >$ cd studies/pwru160c00/pin-powers/
        >$ cp fission-rates.h5 ../../pin-powers/pwru160c00-fission-rates.h5
        >$ cd ../..
        >$ python pin-error-plotter.py

        The file will throw errors for the other four files if you only copied
        one fission-rates.h5 file over. To run it for all five, simply use the
        cp function similarly on all 5 assemblies.

===============================================================================
                               PIN POWER PLOTS
===============================================================================

You can also plot just the normalized pin powers in a similar fashion.

Plot Pin Power Grid Plots -----------------------------------------------------

        To plot pin power grid plots for a single (pwru160c00) assembly:

        >$ cd studies/pwru160c00/pin-powers/
        >$ cp fission-rates.h5 ../../pin-powers/pwru160c00-fission-rates.h5
        >$ cd ../..
        >$ python pin-power-plotter.py

        The file will throw errors for the other four files if you only copied
        one fission-rates.h5 file over. To run it for all five, simply use the
        cp function similarly on all 5 assemblies.

===============================================================================
                               END TRANSMISSION
===============================================================================
