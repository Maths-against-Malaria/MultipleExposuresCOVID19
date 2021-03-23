# differential equations for all compartments
## dS, dR, dD
## dE_1, dEs, dEm
## d_, ds, dm: for all other compartments; used rates
## rates: compartment 'before', rates

import numpy as np
from covidSR_functions import *
from covidSR_parameters_newUSA import par

def dS(pop, var, index):
    x = -var['l'] * pop[index['S']]
    return x

def dE1(pop, var, index):
    x = \
        -  var['rE'] * pop[index['E_1']] \
        +  var['l_s'] * pop[index['S']] \
        -  par['q']['E'] * var['l'] * pop[index['E_1']]
    return x

def dEs1(pop, var, index):
    x = \
        -  var['rE'] * pop[index['Es1']]\
        +  par['q']['E'] * var['l'] *  pop[index['E_1']] \
        -  var['rs'] * pop[index['Es1']]
    return x

def dEm1(pop, var, index):
    x = \
        -  var['rE'] * pop[index['Em1']]\
        +  var['l_m'] * pop[index['S']] \
        +  var['rs'] * pop[index['Es1']]
    return x

def rates(compartment, n, index, par, var):
    compartments = ['E', 'P', 'I', 'L']
    rateIn= var['r' + compartment]
    rateOut = var['r' + compartment]
    if n == 1:
        compIn = compartments[compartments.index(compartment)-1]
        rateIn = var['r' + compIn]
        nIn = par['NErl'][compIn]
    else:
        compIn = compartment
        nIn = n-1

    eff = 1
    if compartment in ['I', 'L']:
        eff = var['fEff_']

    rates = dict()
    rates['rIn'] = rateIn
    rates['rOut'] = rateOut
    rates['cIn'] = compIn
    rates['nIn'] = str(nIn)
    rates['eff'] = eff
    return rates

def d_(pop, var, compartment, n, rates, index, par):
    x =    rates['rIn'] *\
            pop[index[str(rates['cIn']) + '_' + str(rates['nIn'])]]\
        - (rates['rOut'] + par['q'][compartment] * var['l'] * rates['eff'])*\
            pop[index[compartment + '_' + str(n)]]
    return x

def ds(pop, var, compartment, n, rates, index, par):
    x =   rates['rIn'] *\
            pop[index[str(rates['cIn']) + 's' + str(rates['nIn'])]]\
        - rates['rOut']* \
            pop[index[compartment + 's' + str(n)]]\
        + par['q'][compartment] * var['l'] * rates['eff'] *\
                pop[index[compartment + '_' + str(n)]]+\
        - var['rs'] * pop[index[compartment + 's' + str(n)]]
    return x

def dm(pop, var, compartment, n, rates, index, par):
    x =   rates['rIn'] *\
            pop[index[str(rates['cIn']) + 'm' + str(rates['nIn'])]]\
        - rates['rOut']* \
            pop[index[compartment + 'm' + str(n)]]\
        + var['rs'] * pop[index[compartment + 's' + str(n)]]
    return x

def dD(pop, var, par, index):
    nL = par['NErl']['L']
    x = var['rL'] * (\
        par['fsick']['_'] * par['fdead']['_'] * \
            (pop[index['L_'+ str(nL)]] + pop[index['Ls' + str(nL)]]) + \
        par['fsick']['m'] * par['fdead']['m'] * \
             pop[index['Lm' + str(nL)]])
    return x

def dR(pop, var, par, index):
    nL = par['NErl']['L']
    x = var['rL'] * (\
        (1-par['fsick']['_'] * par['fdead']['_']) * \
            (pop[index['L_'+ str(nL)]] + pop[index['Ls' + str(nL)]]) + \
        (1-par['fsick']['m'] * par['fdead']['m']) * \
             pop[index['Lm' + str(nL)]])
    return x

