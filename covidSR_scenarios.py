from covidSR_model import modelSuperinfection

from covidSR_parameters_newUSA import par_newUSA

# Parameter variants
# fsick
fsick = [0.580, 0.664, 0.748, 0.832, 0.916, 1.000]
# fiso
fiso = [0.5, 0.6, 0.7, 0.8, 0.9]
# fdead
fdead = [0.04, 0.045, 0.05, 0.055, 0.06]
# m
m = [0, 0.2, 0.4, 0.6, 0.8, 1]
# q
q = [[  1,   1,   1,   1],
     [  1,   1,   1, 3/4],
     [  1,   1, 3/4, 1/2],
     [  1, 3/4, 1/2, 1/4],
     [3/4, 1/2, 1/4,   0]]
# dist (p of general distancing between day 450 and end (900))
dist = [0, 0.15, 0.3, 0.45, 0.6, 0.75]


# Run simulations
j=0
par_j=par_newUSA

for i in range(len(fsick)):
    for j in [0,1]:
        par_j = par_newUSA
        if j==1:
            par_j['R0']['a'] = 0
        par_i = par_j
        par_i['fsick']['m'] = fsick[i]
        name_i = 'USA_fsickt_' + str(i) + str(j)
        print(modelSuperinfection(par=par_i, pathOut='covidSR_results', name = name_i))

for i in range(len(fdead)):
    par_i = par_j
    par_i['fdead']['m'] = fdead[i]
    name_i = 'USA_fdeadt_' + str(i) + str(j)
    print(modelSuperinfection(par=par_i, pathOut='covidSR_results', name = name_i))

for i in range(len(fiso)):
    par_i = par_j
    par_i['iso']['fm'][1] = fiso[i]
    name_i = 'USA_fisot_' + str(i) + str(j)
    print(modelSuperinfection(par=par_i, pathOut='covidSR_results', name = name_i))

for i in range(len(m)):
    par_i = par_j
    par_i['m']['fm'] = m[i]
    name_i = 'USA_mt_' + str(i) + str(j)
    print(modelSuperinfection(par=par_i, pathOut='covidSR_results', name = name_i))

for i in range(len(q)):
    par_i = par_j
    v = [10,100,1000,10000]
    par = par_newUSA
    par_i['q']['E'] = q[i][0]
    par_i['q']['P'] = q[i][1]
    par_i['q']['I'] = q[i][2]
    par_i['q']['L'] = q[i][3]
    name_i = 'USA_qt_' + str(i) + str(j)
    print(modelSuperinfection(par=par_i, pathOut='covidSR_results', name = name_i))

for i in range(len(dist)):
    for j in [0,2]:
        par_j = par_newUSA
        if j in [2]:
            par_j['m']['m'] = par_j['m']['_']
            par_j['fsick']['m'] = par_j['fsick']['_']
            par_j['fdead']['m'] = par_j['fdead']['_']
            par_j['iso']['fm'] = par_j['iso']['f_']
        par_i = par_j
        par_i['dist']['t'] = [   50,  115,  190,  255,  290,  309,  316,  325,  335,  354,  450, par_newUSA['days']]
        par_i['dist']['p'] = [    0, 0.55, 0.22, 0.55, 0.45, 0.65, 0.55, 0.60, 0.70, 0.55, 0.65, dist[i]]
        print(modelSuperinfection(par=par_i, pathOut='covidSR_results', name=name_i))
