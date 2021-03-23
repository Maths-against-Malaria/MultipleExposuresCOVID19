 # MultipleExposuresCOVID19
 
 Code for the publication 'Is increased mortality by multiple exposures to COVID-19 an overseen factor when aiming for herd immunity?'
 by Kristina B. Helle, Arlinda Sadiku, Girma M. Zelleke, Aliou Bouba, Toheeb B. Ibrahim, H. Christian Jr. Tsoungui Obama, Vincent Appiah, Gideon A. Ngwa, Miranda I. Teboh-Ewungkem, Kristan A. Schneider

 the functions to run the model are in the following files that do not need to be changed unless there are fundamental changes to the model
 covidSR_functions, covidSR_differentialEquatins, covidSR_model

 the basic parameters are defined in the following files
 I suggest to use these files for basic parameter sets and change the parameters for different scenarios not by changing the files but by changing the parameter object only
 covidSR_parameters_newUSA

 to run the simulations of the scenarios in the publication the relevant functions can be called by covidSR_scenarios

 basic plotting functions are defined in covidSR_plot_functions

 -------------------- Install/Prepare -------------------------
 for use with PyCharm see: https://youtu.be/a8MckiothGc
 after downloading create the following directory (to save results - else the given local paths will not work):
 covidSR_results

 -------------------- Use -------------------------------------
 define the scenarios of interest in a file and run 'modelSuperinfection'
 it will generate files of the result, the parameters, the values of the variables at the time steps
 the 'name' will appear in all the filenames to identify them
 some examples for scenarios are in:
 covidSR_scenarios

 plot the scenarios of interest from the files by some plotting function
 some examples are in:
 covidSR_plot_results


 ---------------------- Background ----------------------------

 the model of differential equations is in covidSR_model
 the function modelSuperinfection runs the simulation
 inside of it function 'f' is defined, it contains the differential equations for all compartments
 the functions of the differential equations are defined in covidSR_differentialEquations
 all compartments of E_2, ...,E_nE, P_1, ..., L_nL are based on the same function of differential equation d_; similar ds (for transient), dm (for multiple infected);
 with help of 'rates' d_, ds, dm are adapted to the compartment by selecting the correct rates (by stage, if relevant also accounting for effective population)
 inside 'f' inside 'modelSuperinfection' dS, dE_1, dEs1, dEm1, d_, ds, dm are used for the compartments
 variables needed in each time step (lambda...) are computed by 'varFunction' (in covidSR_functions)
 (they are kept track of in par_rec and saved to a file; this could be turned off if not needed)
 'indexFunction' creates the references of the compartments in the 'pop' list, based on the number of Erlang stages
 'popsum' computes individuals in compartments (sum over Erlang stages)

 time is indicated by 't'
 the compartments are in the list 'pop';
 the stages are: S, (E, P, I, L), D, R
 each stage in (E, P, I, L) can be single infected '_', transient multi-infected 's', fully superinfected 'm'
 (all parameters, variables... are also marked with '_', 's', 'm' if there is a difference)


