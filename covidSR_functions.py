# functions used in the simulation
## indexFunction: indexing of compartments in the 'pop' list
## popsum: sum of individuals in compartment (over Erlang stages)
## varFunction: all variables to be computed in every time step (lambda...)
## parToString: generate file name from parameters (not used)

import numpy as np

# indexing of 'pop' by actual compartment names; varies because of number of Erlang stages (Nerls)
def indexFunction(Nerls):
    compartments = [
        ('S',  0, ''),
        ('E', Nerls['E'], '_'), ('E', Nerls['E'], 's'), ('E', Nerls['E'], 'm'),
        ('P', Nerls['P'], '_'), ('P', Nerls['P'], 's'), ('P', Nerls['P'], 'm'),
        ('I', Nerls['I'], '_'), ('I', Nerls['I'], 's'), ('I', Nerls['I'], 'm'),
        ('L', Nerls['L'], '_'), ('L', Nerls['L'], 's'), ('L', Nerls['L'], 'm'),
        ('D', 0, ''),
        ('R', 0, ''),
    ]
    index = dict()
    ind = 0
    for i in compartments:
        notation = i[0] + i[2]
        if i[1] == 0:
            index[notation] = ind
            ind += 1
        else:
            for k in np.arange(1, i[1] + 1):
                notation_k = notation + str(k)
                index[notation_k] = ind
                ind += 1

    return index

# sum of population in compartment (sum over Erlang stages)
# script:_,s,t for compartment type
def popsum(pop, compartment, script, Nerls, index):
    if compartment in {'S', 'D', 'R'}:
        Nerl = 0
    if compartment == 'E':
        Nerl = Nerls['E']
    if compartment == 'P':
        Nerl = Nerls['P']
    if compartment == 'I':
        Nerl = Nerls['I']
    if compartment == 'L':
        Nerl = Nerls['L']
    x = 0

    if Nerl == 0:
        x = x + pop[index[compartment]]
    else:
        for k in range(1, Nerl+1):
            x = x + pop[index[compartment + script + str(k)]]
    return float(x)

# functions to compute the variables (lambda...) in each time step, not differential equations
# t (int): time
# pop: list of individuals in compartments
# par: parameters, see covidSR_parameters_newUSA
def varFunction(t, pop, par):
    var = dict()
    index = indexFunction(par['NErl'])

    # Number of indivuduals in compartment
    def popsumt(compartment, script):
        x= popsum(pop=pop, compartment=compartment, script=script, Nerls=par['NErl'], index=index)
        return(x)

    P_ = popsumt(compartment='P', script='_')
    Ps = popsumt(compartment='P', script='s')
    Pm = popsumt(compartment='P', script='m')
    I_ = popsumt(compartment='I', script='_')
    Is = popsumt(compartment='I', script='s')
    Im = popsumt(compartment='I', script='m')
    L_ = popsumt(compartment='L', script='_')
    Ls = popsumt(compartment='L', script='s')
    Lm = popsumt(compartment='L', script='m')

    #pGen
    pGen = par['dist']['p'][0]
    for i in range(len(par['dist']['t'])-1):
        if par['dist']['t'][i] <= t <= par['dist']['t'][i+1]:
            pGen = par['dist']['p'][i+1]

    # R0
    R0 =\
        par['R0']['R0bar'] * (
                1 + par['R0']['a'] * np.cos(2 * np.pi * (t - par['R0']['tR0max']) / 365)
        )

    # beta
    cD =par['c']['P'] * par['D']['P'] +\
        par['c']['I'] * par['D']['I'] +\
        par['c']['L'] * par['D']['L']
    cD = float(cD)

    betaP = par['c']['P'] * R0 / cD
    betaI = par['c']['I'] * R0 / cD
    betaL = par['c']['L'] * R0 / cD
    var['beta'] =[betaP, betaI, betaL]

    # isolation: compute factor how many of the I,L compartments are effective in causing infections
    ## depends on fiso, fisot (time dependent)
    fiso_s = par['iso']['f_'][0]
    fiso_m = par['iso']['fm'][0]
    for i in range(len(par['iso']['t'])-1):
        if par['iso']['t'][i] <= t <= par['iso']['t'][i+1]:
            fiso_s = par['iso']['f_'][i+1]
            fiso_m = par['iso']['fm'][i+1]

    # Eff (as result of iso)
    factor_s = fiso_s * par['fsick']['_']
    factor_m = fiso_m * par['fsick']['m']

    ## depends on how many of the ones that are to be isolated are in quarantine wards and how many are in home isolation
    # Q the individuals to be isolated
    Q = factor_s * (I_+ Is + L_ + Ls) + \
        factor_m * (Im + Lm)

    factorQ = 1
    if Q > par['Qmax']:  # if isolation wards are full, only those who find a place are isolated there
        factorQ = par['Qmax'] / Q
    var['fEff_'] = (1 - factor_s * (factorQ + (1 - factorQ) * par['phome']))
    var['fEffm'] = (1 - factor_m * (factorQ + (1 - factorQ) * par['phome']))

    # lambda
    # lambda s
    var['l_s'] = 1 / par['N'] * (
                    par['lExt']['_'] + \
                    (1 - pGen) * (
                        betaP * (P_+ (1 - par['m']['_']) * Ps + (1 - par['m']['m']) * Pm) + \
                        betaI * (var['fEff_'] * (I_ + (1 - par['m']['_']) * Is) + \
                                 var['fEffm'] * (1 - par['m']['m']) * Im) + \
                        betaL * (var['fEff_'] * (L_ + (1 - par['m']['_']) * Ls) + \
                                 var['fEffm'] * (1 - par['m']['m']) * Lm)))
    # lambda m
    var['l_m'] = 1 / par['N'] * (
                par['lExt']['m'] + \
                (1 - pGen) * (
                    betaP * (par['m']['_'] * Ps + \
                             par['m']['m'] * Pm) + \
                    betaI * (var['fEff_'] * par['m']['_'] * Is + \
                             var['fEffm'] * par['m']['m'] * Im) + \
                    betaL * (var['fEff_'] * par['m']['_'] * Ls + \
                             var['fEffm'] * par['m']['m'] * Lm)))

    var['l'] = var['l_s'] + var['l_m']

    var['rE'] = par['NErl']['E'] / par['D']['E'] # epsilon
    var['rP'] = par['NErl']['P'] / par['D']['P'] # delta
    var['rI'] = par['NErl']['I'] / par['D']['I'] # gamma
    var['rL'] = par['NErl']['L'] / par['D']['L'] # phi
    var['rs'] = par['NErl']['s'] / par['D']['s'] # alpha
    return var

# turn parameters into a string (not used at the moment)
# the string may be used as file name if it is short enough
def parToString(par):
    x = str(par['N'])                   + ';' + \
        str(par['days'])                + ';' + \
        ",".join(map(str, list(par['D'].values()))) + ';' + \
        ",".join(map(str, list(par['NErl'].values()))) + ';' + \
        ",".join(map(str, list(par['c'].values()))) + ';' + \
        ",".join(map(str, list(par['q'].values()))) + ';' + \
        ",".join(map(str, list(par['R0'].values()))) + ';' + \
        ",".join(map(str, list(par['m'].values()))) + ';' + \
        ",".join(map(str, list(par['lExt'].values()))) + ';' + \
        ",".join(map(str, list(par['fsick'].values()))) + ';' + \
        ",".join(map(str, list(par['fdead'].values()))) + ';' + \
        str(par['I1_0']) + ';' + \
        str(par['Qmax']) + ';' + \
        str(par['phome']) + ';' + \
        ",".join(map(str, list(par['iso']['t'])))  + ';' + \
        ",".join(map(str, list(par['iso']['f_']))) + ';' + \
        ",".join(map(str, list(par['iso']['fm']))) + ';' + \
        ",".join(map(str, list(par['dist']['t'])))  + ';' + \
        ",".join(map(str, list(par['dist']['p'])))

    return x

