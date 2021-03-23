from covidSR_plot_functions import plotSim
from covidSR_parameters_newUSA import par

names_fsick = ['USA_fsickt_00', 'USA_fsickt_10', 'USA_fsickt_20', 'USA_fsickt_30', 'USA_fsickt_40', 'USA_fsickt_50',]
names_fsick1= ['USA_fsickt_01', 'USA_fsickt_11', 'USA_fsickt_21', 'USA_fsickt_31', 'USA_fsickt_41', 'USA_fsickt_51',]
names_fdead = ['USA_fdeadt_00', 'USA_fdeadt_10', 'USA_fdeadt_20', 'USA_fdeadt_30', 'USA_fdeadt_40',]
names_fiso = ['USA_fisot_00', 'USA_fisot_10', 'USA_fisot_20', 'USA_fisot_30', 'USA_fisot_40',]
names_m = ['USA_mt_00', 'USA_mt_10', 'USA_mt_20', 'USA_mt_30', 'USA_mt_40','USA_mt_50',]
names_q = ['USA_qt_00', 'USA_qt_10', 'USA_qt_20', 'USA_qt_30', 'USA_qt_40',]
names_dist0 = ['USA_dist_00', 'USA_dist_10', 'USA_dist_20', 'USA_dist_30', 'USA_dist_40', 'USA_dist_50']
names_dist2 = ['USA_dist_02', 'USA_dist_12', 'USA_dist_22', 'USA_dist_32', 'USA_dist_42','USA_dist_52']


#plotSim(type='S', scenarios=names_fsick, par=par)
plotSim(type='I', scenarios=names_fsick1, par=par)
#plotSim(type='D', scenarios=names_dist0, par=par)